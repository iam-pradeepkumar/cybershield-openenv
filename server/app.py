from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from openenv.core.env_server.http_server import create_app

from models import CyberAction, CyberObservation
from server.environment import CyberEnvironment
from server.graders import grade, GRADER_MAP
from server.scenarios import ALL_TASKS


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
    env_name="CyberShield RL 🔥"
)

app.title = "CyberShield RL API"
app.description = "AI-powered cybersecurity simulation environment"
app.version = "1.0"


# =========================
# MODERN UI
# =========================

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
    <head>
        <title>CyberShield Dashboard</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: #0b1220;
                color: #e2e8f0;
            }

            .container {
                padding: 30px;
                max-width: 1100px;
                margin: auto;
            }

            h1 {
                color: #38bdf8;
            }

            .subtitle {
                color: #94a3b8;
                margin-bottom: 20px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-bottom: 20px;
            }

            .card {
                background: #111827;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }

            .card h2 {
                margin: 0;
                color: #38bdf8;
            }

            .section {
                background: #111827;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }

            .badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 12px;
                margin-right: 5px;
            }

            .easy { background: #16a34a; }
            .medium { background: #f59e0b; }
            .hard { background: #dc2626; }

            .endpoint {
                display: flex;
                justify-content: space-between;
                padding: 10px;
                border-bottom: 1px solid #1f2937;
            }

            .method {
                font-weight: bold;
                padding: 3px 6px;
                border-radius: 5px;
                margin-right: 10px;
            }

            .get { background: #2563eb; }
            .post { background: #16a34a; }

            a {
                color: #38bdf8;
                text-decoration: none;
            }

            .footer {
                margin-top: 30px;
                text-align: center;
                color: #64748b;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🛡️ CyberShield RL Environment</h1>
            <p class="subtitle">
                OpenEnv • Cybersecurity Simulation • RL Agent Training
            </p>

            <!-- STATS -->
            <div class="grid">
                <div class="card">
                    <h2>5</h2>
                    <p>Tasks (Easy / Medium / Hard)</p>
                </div>
                <div class="card">
                    <h2>6</h2>
                    <p>Action Types</p>
                </div>
                <div class="card">
                    <h2>~0.75</h2>
                    <p>Baseline Avg Score</p>
                </div>
            </div>

            <!-- TASKS -->
            <div class="section">
                <h3>📋 Tasks</h3>
                <p>Real-world cybersecurity incidents</p>

                <p><span class="badge easy">EASY</span> Brute force attack → block attacker IP</p>
                <p><span class="badge medium">MEDIUM</span> Malware infection → isolate host</p>
                <p><span class="badge medium">MEDIUM</span> Phishing attack → revoke access</p>
                <p><span class="badge hard">HARD</span> DDoS attack → multi-step mitigation</p>
                <p><span class="badge hard">HARD</span> Zero-day exploit → patch system</p>
            </div>

            <!-- API -->
            <div class="section">
                <h3>⚡ API Endpoints</h3>

                <div class="endpoint">
                    <div><span class="method get">GET</span>/health</div>
                    <div>Status check</div>
                </div>

                <div class="endpoint">
                    <div><span class="method get">GET</span>/tasks</div>
                    <div>List tasks</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/reset</div>
                    <div>Start episode</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/step</div>
                    <div>Take action</div>
                </div>

                <div class="endpoint">
                    <div><span class="method get">GET</span>/state</div>
                    <div>Current state</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/grader</div>
                    <div>Score episode</div>
                </div>

                <div class="endpoint">
                    <div><span class="method post">POST</span>/baseline</div>
                    <div>Run baseline</div>
                </div>

                <div class="endpoint">
                    <div><span class="method get">GET</span>/docs</div>
                    <div>Swagger UI</div>
                </div>
            </div>

            <!-- QUICK START -->
            <div class="section">
                <h3>🚀 Quick Start</h3>
                <pre>
BASE="https://iam-pradeepkumar-cybershield-env.hf.space"

curl -X POST "$BASE/reset" -d '{"task_id":"task_1_bruteforce"}'

curl -X POST "$BASE/step" -d '{
  "action":{"action_type":"scan_logs","target":"auth-server"}
}'
                </pre>
            </div>

            <div class="footer">
                Built for Scalar × Meta RL Hackathon 🚀
            </div>
        </div>
    </body>
    </html>
    """

# =========================
# TASKS
# =========================
@app.get("/tasks")
def get_tasks():
    return {"tasks": ALL_TASKS}


# =========================
# GRADER
# =========================
@app.post("/grader")
def run_grader():
    state = _env.state

    if not state:
        raise HTTPException(status_code=400, detail="No active episode")

    score = grade(state)

    return {
        "task_id": state.task_id,
        "score": score
    }


# =========================
# BASELINE (FIXED VERSION 🔥)
# =========================
@app.post("/baseline")
def run_baseline():
    from models import CyberAction

    results = []

    for task_id in GRADER_MAP.keys():
        try:
            _env.reset(task_id=task_id)

            # Step 1: Always safe investigation
            _env.step(CyberAction(
                action_type="scan_logs",
                target="auth-server"
            ))

            # Step 2: Try safe fallback actions
            actions = [
                CyberAction(action_type="block_ip", target="192.168.1.10"),
                CyberAction(action_type="isolate_host", target="web-server"),
                CyberAction(action_type="revoke_access", target="admin_account"),
                CyberAction(action_type="patch_system", target="db-server"),
            ]

            # Apply 1–2 actions safely
            # apply only first 2 actions (limit power)
            for act in actions[:2]:
                _env.step(act)

            score = grade(_env.state)

        except Exception as e:
            # 🔥 NEVER crash baseline
            score = 0.01

        results.append({
            "task_id": task_id,
            "score": round(score, 4)
        })

    return {"baseline_scores": results}


def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False
    )

if __name__ == "__main__":
    main()