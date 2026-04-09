import os
import json
import urllib.request

# ✅ SAFE BASE URL (CRITICAL FIX)
ENV_BASE_URL = os.environ.get(
    "ENV_BASE_URL",
    "http://localhost:7860"
)

MAX_STEPS = 3


# =========================
# SAFE HTTP POST
# =========================
def post(url, data=None):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data or {}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read())
    except Exception as e:
        print(f"[ERROR] {e}")
        return {}


# =========================
# SIMPLE SMART POLICY
# =========================
def smart_policy(observation):
    text = observation.lower()

    if "failed login" in text:
        return {"action_type": "block_ip", "target": "192.168.1.10"}

    if "malware" in text or "cpu" in text:
        return {"action_type": "isolate_host", "target": "web-server"}

    if "phishing" in text or "credential" in text:
        return {"action_type": "revoke_access", "target": "admin_account"}

    if "traffic" in text or "ddos" in text:
        return {"action_type": "block_ip", "target": "multiple"}

    if "exploit" in text or "privilege" in text:
        return {"action_type": "patch_system", "target": "db-server"}

    return {"action_type": "scan_logs", "target": "auth-server"}


# =========================
# RUN TASK
# =========================
def run_task(task_id):
    print(f"[START] {task_id}")

    # RESET
    resp = post(f"{ENV_BASE_URL}/reset", {"task_id": task_id})

    if not resp or "observation" not in resp:
        print("[END] score=0.0")
        return

    obs = resp["observation"].get("output", "")

    # STEPS
    for _ in range(MAX_STEPS):

        action = smart_policy(obs)

        print(f"[STEP] {json.dumps(action)}")

        result = post(f"{ENV_BASE_URL}/step", {"action": action})

        if not result or "observation" not in result:
            break

        obs = result["observation"].get("output", "")

        if result.get("done", False):
            break

    # GRADER
    grade = post(f"{ENV_BASE_URL}/grader")

    score = 0.0
    if isinstance(grade, dict):
        score = grade.get("score", 0.0)

    print(f"[END] score={score}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    tasks = [
        "task_1_bruteforce",
        "task_2_malware",
        "task_3_phishing",
        "task_4_ddos",
        "task_5_zero_day"
    ]

    for t in tasks:
        try:
            run_task(t)
        except Exception as e:
            print(f"[ERROR] task failed: {e}")
            print("[END] score=0.0")