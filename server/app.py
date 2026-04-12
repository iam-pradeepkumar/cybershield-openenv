from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from openenv.core.env_server.http_server import create_app

# These imports work because PYTHONPATH includes /app/server
from models import CyberAction, CyberObservation
from environment import CyberEnvironment
from graders import grade, GRADER_MAP
from scenarios import ALL_TASKS

import uvicorn

# =========================
# ENV INSTANCE
# =========================
_env = CyberEnvironment()


def _env_factory():
    return _env


# =========================
# CREATE APP
# =========================
app = create_app(
    _env_factory,
    CyberAction,
    CyberObservation,
    env_name="CyberShield RL"
)

app.title = "CyberShield RL API"
app.description = "AI-powered cybersecurity simulation environment for RL agent training"
app.version = "1.0"


# =========================
# DASHBOARD UI
# =========================

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>CyberShield Dashboard</title>
        <style>
            body { margin: 0; font-family: 'Segoe UI', sans-serif; background: #0b1220; color: #e2e8f0; }
            .container { padding: 30px; max-width: 1100px; margin: auto; }
            h1 { color: #38bdf8; }
            .subtitle { color: #94a3b8; margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
            .card { background: #111827; padding: 20px; border-radius: 10px; }
            .card h2 { margin: 0; color: #38bdf8; }
            .section { background: #111827; padding: 20px; border-radius: 10px; margin-top: 20px; }
            .badge { display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 12px; margin-right: 5px; }
            .easy { background: #16a34a; } .medium { background: #f59e0b; } .hard { background: #dc2626; }
            .endpoint { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #1f2937; }
            .method { font-weight: bold; padding: 3px 6px; border-radius: 5px; margin-right: 10px; }
            .get { background: #2563eb; } .post { background: #16a34a; }
            a { color: #38bdf8; text-decoration: none; }
            .footer { margin-top: 30px; text-align: center; color: #64748b; }
            pre { background: #0f172a; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 13px; color: #7dd3fc; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>&#x1F6E1;&#xFE0F; CyberShield RL Environment</h1>
            <p class="subtitle">OpenEnv &bull; Cybersecurity Simulation &bull; RL Agent Training</p>
            <div class="grid">
                <div class="card"><h2>5</h2><p>Tasks (Easy / Medium / Hard)</p></div>
                <div class="card"><h2>5</h2><p>Action Types</p></div>
                <div class="card"><h2>0.01&ndash;0.99</h2><p>Score Range</p></div>
            </div>
            <div class="section">
                <h3>&#x1F4CB; Tasks</h3>
                <p><span class="badge easy">EASY</span> Brute force attack &rarr; block attacker IP</p>
                <p><span class="badge medium">MEDIUM</span> Malware infection &rarr; isolate host</p>
                <p><span class="badge medium">MEDIUM</span> Phishing attack &rarr; revoke access</p>
                <p><span class="badge hard">HARD</span> DDoS attack &rarr; block IP range</p>
                <p><span class="badge hard">HARD</span> Zero-day exploit &rarr; patch system</p>
            </div>
            <div class="section">
                <h3>&#x26A1; API Endpoints</h3>
                <div class="endpoint"><div><span class="method get">GET</span>/health</div><div>Status check</div></div>
                <div class="endpoint"><div><span class="method get">GET</span>/tasks</div><div>List all tasks</div></div>
                <div class="endpoint"><div><span class="method post">POST</span>/reset</div><div>Start episode</div></div>
                <div class="endpoint"><div><span class="method post">POST</span>/step</div><div>Take action</div></div>
                <div class="endpoint"><div><span class="method get">GET</span>/state</div><div>Current state</div></div>
                <div class="endpoint"><div><span class="method post">POST</span>/grader</div><div>Score episode</div></div>
                <div class="endpoint"><div><span class="method post">POST</span>/baseline</div><div>Run baseline agent</div></div>
                <div class="endpoint"><div><span class="method get">GET</span>/docs</div><div>Swagger UI</div></div>
            </div>
            <div class="section">
                <h3>&#x1F680; Quick Start</h3>
                <pre>BASE="https://huggingface.co/spaces/iam-pradeepkumar/cybershield-env.hf.space"

curl -X POST "$BASE/reset" \\
  -H "Content-Type: application/json" \\
  -d '{"task_id": "task_1_bruteforce"}'

curl -X POST "$BASE/step" \\
  -H "Content-Type: application/json" \\
  -d '{"action": {"action_type": "scan_logs", "target": "auth-server"}}'</pre>
            </div>
            <div class="footer">Built for Scalar &times; Meta RL Hackathon &#x1F680;</div>
        </div>
    </body>
    </html>
    """


@app.get("/tasks")
def get_tasks():
    return {"tasks": ALL_TASKS}


@app.post("/grader")
def run_grader():
    state = _env.state
    if not state or not state.task_id:
        raise HTTPException(status_code=400, detail="No active episode. Call /reset first.")
    score = grade(state)
    return {
        "task_id": state.task_id,
        "score": score,
        "actions_taken": len(state.actions_taken),
        "system_secured": state.system_secured,
    }


@app.post("/baseline")
def run_baseline():
    results = []
    task_actions = {
        "task_1_bruteforce": [
            CyberAction(action_type="scan_logs",    target="auth-server"),
            CyberAction(action_type="block_ip",     target="192.168.1.10"),
            CyberAction(action_type="scan_logs",    target="firewall"),
        ],
        "task_2_malware": [
            CyberAction(action_type="scan_logs",    target="web-server"),
            CyberAction(action_type="isolate_host", target="web-server"),
            CyberAction(action_type="scan_logs",    target="db-server"),
        ],
        "task_3_phishing": [
            CyberAction(action_type="scan_logs",    target="auth-server"),
            CyberAction(action_type="revoke_access",target="admin_account"),
            CyberAction(action_type="scan_logs",    target="firewall"),
        ],
        "task_4_ddos": [
            CyberAction(action_type="scan_logs",    target="web-server"),
            CyberAction(action_type="block_ip",     target="multiple"),
            CyberAction(action_type="scan_logs",    target="firewall"),
        ],
        "task_5_zero_day": [
            CyberAction(action_type="scan_logs",    target="db-server"),
            CyberAction(action_type="patch_system", target="db-server"),
            CyberAction(action_type="scan_logs",    target="auth-server"),
        ],
    }
    for task_id in GRADER_MAP.keys():
        try:
            _env.reset(task_id=task_id)
            for act in task_actions.get(task_id, []):
                _env.step(act)
            score = grade(_env.state)
        except Exception:
            score = 0.01
        results.append({"task_id": task_id, "score": round(score, 4)})
    return {"baseline_scores": results}


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)


if __name__ == "__main__":
    main()
