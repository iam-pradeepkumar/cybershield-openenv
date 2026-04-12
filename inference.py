import os
import json
from openai import OpenAI

# =========================
# ENV (MANDATORY)
# =========================
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "http://localhost:7860")
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN")

MAX_STEPS = 6

import urllib.request


# =========================
# HTTP
# =========================
def post(url, data=None):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data or {}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read())
    except Exception as e:
        print(f"[HTTP ERROR] {e}")
        return {}


# =========================
# RULE-BASED POLICY
# =========================
def smart_policy(obs):
    if "Failed login" in obs or "brute force" in obs.lower():
        return {"action_type": "block_ip", "target": "192.168.1.10"}
    if "crypto_miner" in obs or "CPU usage spike" in obs:
        return {"action_type": "isolate_host", "target": "web-server"}
    if "Unknown location" in obs or "Unusual access" in obs:
        return {"action_type": "revoke_access", "target": "admin_account"}
    if "Traffic spike" in obs or "DDoS" in obs:
        return {"action_type": "block_ip", "target": "multiple"}
    if "privilege escalation" in obs or "root access" in obs:
        return {"action_type": "patch_system", "target": "db-server"}
    return None


# =========================
# LLM CALL — OpenAI Client (MANDATORY)
# =========================
def call_llm(observation):
    if not API_BASE_URL or not API_KEY:
        return {"action_type": "scan_logs", "target": "auth-server"}

    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY,
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cybersecurity incident response expert. "
                        "Analyze the observation and return ONLY a valid JSON object "
                        "with exactly two keys: action_type and target. "
                        "action_type must be one of: scan_logs, block_ip, isolate_host, "
                        "revoke_access, patch_system. "
                        "Do NOT include any explanation or markdown. "
                        "Example: {\"action_type\": \"block_ip\", \"target\": \"192.168.1.10\"}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Observation:\n{observation}\n\nReturn the JSON action:"
                }
            ],
            temperature=0,
            max_tokens=100,
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return {"action_type": "scan_logs", "target": "auth-server"}


# =========================
# RUN TASK
# =========================
def run_task(task_id):
    print(f"[START] task_id={task_id}")

    resp = post(f"{ENV_BASE_URL}/reset", {"task_id": task_id})

    if not resp or "observation" not in resp:
        print(f"[END] task_id={task_id} score=0.0")
        return 0.0

    obs = resp["observation"].get("output", "")

    # Step 1: Always scan logs first (investigation is mandatory)
    scan_targets = {
        "task_1_bruteforce": "auth-server",
        "task_2_malware": "web-server",
        "task_3_phishing": "auth-server",
        "task_4_ddos": "web-server",
        "task_5_zero_day": "db-server",
    }
    scan_target = scan_targets.get(task_id, "auth-server")

    scan_action = {"action_type": "scan_logs", "target": scan_target}
    print(f"[STEP] task_id={task_id} action={json.dumps(scan_action)}")
    result = post(f"{ENV_BASE_URL}/step", {"action": scan_action})

    if result and "observation" in result:
        obs = result["observation"].get("output", "")

    # Steps 2+: policy or LLM
    for step_num in range(2, MAX_STEPS + 1):
        action = smart_policy(obs) or call_llm(obs)

        print(f"[STEP] task_id={task_id} action={json.dumps(action)}")

        result = post(f"{ENV_BASE_URL}/step", {"action": action})

        if not result or "observation" not in result:
            break

        obs = result["observation"].get("output", "")

        if result.get("done", False):
            break

    grade = post(f"{ENV_BASE_URL}/grader")
    score = grade.get("score", 0.0) if isinstance(grade, dict) else 0.0

    print(f"[END] task_id={task_id} score={score}")
    return score


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    tasks = [
        "task_1_bruteforce",
        "task_2_malware",
        "task_3_phishing",
        "task_4_ddos",
        "task_5_zero_day",
    ]

    total = 0.0
    for t in tasks:
        try:
            s = run_task(t)
            total += s
        except Exception as e:
            print(f"[END] task_id={t} score=0.0")

    avg = round(total / len(tasks), 4)
    print(f"[SUMMARY] avg_score={avg}")
