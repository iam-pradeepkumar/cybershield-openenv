---
title: CyberShield RL Environment
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 🛡️ CyberShield RL — AI Cybersecurity Defense Environment

CyberShield RL is a **real-world inspired reinforcement learning environment** designed to train and evaluate AI agents for **cybersecurity incident response**.

Agents must **analyze logs, detect threats, and apply correct mitigation strategies** under uncertainty, limited steps, and misleading signals.

---

# 🚨 Problem Statement

Modern systems face continuous cyber threats such as:

* Brute force attacks
* Malware infections
* Phishing-based credential compromise
* Distributed Denial of Service (DDoS)
* Zero-day vulnerabilities

Traditional rule-based systems fail to adapt dynamically.

👉 CyberShield introduces an **agent-based RL environment** where AI learns to:

* Investigate system anomalies
* Identify attack patterns
* Take correct defensive actions
* Optimize decisions under constraints

---

# 🧠 Key Innovations

### 🔥 1. Multi-Step Reasoning Environment

Agents must follow:

```text
Investigate → Diagnose → Mitigate → Secure
```

---

### 🔥 2. Realistic Cyber Signals

* System metrics (CPU, memory)
* Logs with hidden clues
* Alerts and anomalies
* Red herrings (misleading signals)

---

### 🔥 3. Hybrid Agent Design

* Rule-based reasoning (fast + reliable)
* LLM-based reasoning (adaptive + contextual)
* Optimized for real-world deployment

---

### 🔥 4. Deterministic Evaluation

* Reproducible scoring
* No randomness in grading
* Hackathon-compliant evaluation logic

---

# 📋 Task Design

| Task               | Difficulty | Core Challenge                     |
| ------------------ | ---------- | ---------------------------------- |
| Brute Force Attack | Easy       | Detect repeated login attempts     |
| Malware Infection  | Medium     | Identify compromised host          |
| Phishing Attack    | Medium     | Detect credential misuse           |
| DDoS Attack        | Hard       | Handle traffic anomalies           |
| Zero-Day Exploit   | Hard       | Detect subtle privilege escalation |

---

# ⚙️ Action Space

Agents can perform:

* `scan_logs` → Investigate system logs
* `block_ip` → Stop malicious IP
* `isolate_host` → Contain infected system
* `revoke_access` → Disable compromised account
* `patch_system` → Fix vulnerabilities

---

# 👁️ Observation Space

Each step returns:

* System state (services, CPU, memory)
* Logs and alerts
* Reward signal
* Steps remaining
* Partial score

---

# 🧠 Reward Design (Core RL Logic)

The environment uses **dense reward shaping**:

```text
reward = score(t) - score(t-1)
```

### Score Components:

* +0.3 → Attack correctly identified
* +0.3 → Correct mitigation applied
* +0.4 → System secured

### Penalties:

* −0.1 → Premature or incorrect actions
* −0.1 → Inefficient step usage

👉 Encourages **efficient and correct decision-making**

---

# 📊 Evaluation & Grading

* Score range: **0.01 – 0.99**
* Deterministic grading via task-specific functions
* Partial credit for intermediate reasoning
* Hard tasks require **multi-step solutions**

---

# 🤖 Baseline Agent

The baseline agent:

* Performs initial investigation
* Applies limited actions
* Makes imperfect decisions intentionally

👉 Ensures:

* Non-trivial benchmark
* Meaningful comparison for advanced agents

---

# 🚀 API Endpoints

| Method | Endpoint    | Description               |
| ------ | ----------- | ------------------------- |
| POST   | `/reset`    | Start new episode         |
| POST   | `/step`     | Execute action            |
| GET    | `/state`    | Current environment state |
| GET    | `/tasks`    | List all tasks            |
| POST   | `/grader`   | Evaluate performance      |
| POST   | `/baseline` | Run baseline agent        |
| GET    | `/health`   | Service status            |

---

# 🧪 Example Usage

```bash
BASE="https://huggingface.co/spaces/iam-pradeepkumar/cybershield-env"

curl -X POST "$BASE/reset" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_1_bruteforce"}'

curl -X POST "$BASE/step" \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "action_type": "scan_logs",
      "target": "auth-server"
    }
  }'
```

---

# 🧠 Agent Strategy

The agent uses a **hybrid architecture**:

1. Rule-based detection for known attack patterns
2. LLM-based reasoning for complex scenarios
3. Multi-step decision loop
4. Reward-aware optimization

---

# 🏗️ System Architecture

```text
Agent (LLM + Rules)
        ↓
OpenEnv API (FastAPI)
        ↓
CyberShield Environment
        ↓
Scenario Engine + Grader
```

---

# 🌍 Deployment

* Hosted on HuggingFace Spaces
* Docker-based deployment
* FastAPI backend
* OpenEnv compatible

---

# 🏆 Why This Project Stands Out

* Real-world cybersecurity application
* Strong RL environment design
* Multi-step reasoning tasks
* Deterministic evaluation
* Hybrid AI agent architecture
* Clean API + UI dashboard

---

# 🧪 Why This Environment is Challenging

- Partial observability: agents must infer attacks from incomplete logs  
- Misleading signals (red herrings) included intentionally  
- Multi-step dependencies: actions fail without proper investigation  
- Stochastic noise injection in logs and system metrics  
- Requires reasoning, not simple action guessing  

👉 Designed to simulate real-world cybersecurity decision-making

# 📌 Future Improvements

* Multi-agent attacker vs defender simulation
* Real-time monitoring dashboard
* Integration with real security logs
* Adaptive adversarial scenarios

---

# 👨‍💻 Author

**Pradeep Kumar S**
AI Developer | Reinforcement Learning | Agent Systems

