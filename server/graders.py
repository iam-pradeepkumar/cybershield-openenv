from typing import Any
from models import CyberState


# =========================
# HELPER
# =========================
def _has_action(actions, action_type):
    return any(a.get("action_type") == action_type for a in actions)


# =========================
# TASK 1 — EASY
# =========================
def grade_task1(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "scan_logs"):
        score += 0.3

    if _has_action(state.actions_taken, "block_ip"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# TASK 2 — MEDIUM
# =========================
def grade_task2(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "scan_logs"):
        score += 0.2

    if _has_action(state.actions_taken, "isolate_host"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    # penalty for wrong action
    if _has_action(state.actions_taken, "block_ip"):
        score -= 0.1

    # bonus for multi-step reasoning
    if len(state.actions_taken) >= 3:
        score += 0.1

    return max(0.0, min(score, 1.0))


# =========================
# TASK 3 — MEDIUM
# =========================
def grade_task3(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "scan_logs"):
        score += 0.2

    if _has_action(state.actions_taken, "revoke_access"):
        score += 0.4

    if state.system_secured:
        score += 0.4

    return min(score, 1.0)


# =========================
# TASK 4 — HARD
# =========================
def grade_task4(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "scan_logs"):
        score += 0.2

    if _has_action(state.actions_taken, "block_ip"):
        score += 0.3

    if len(state.actions_taken) >= 3:
        score += 0.2

    if state.system_secured:
        score += 0.3

    # penalty
    if _has_action(state.actions_taken, "patch_system"):
        score -= 0.2

    return max(0.0, min(score, 1.0))


# =========================
# TASK 5 — HARD
# =========================
def grade_task5(state: CyberState) -> float:
    score = 0.0

    if _has_action(state.actions_taken, "scan_logs"):
        score += 0.2

    if _has_action(state.actions_taken, "patch_system"):
        score += 0.4

    if len(state.actions_taken) >= 3:
        score += 0.2

    if state.system_secured:
        score += 0.3

    return min(score, 1.0)


# =========================
# DISPATCH
# =========================
GRADER_MAP = {
    "task_1_bruteforce": grade_task1,
    "task_2_malware": grade_task2,
    "task_3_phishing": grade_task3,
    "task_4_ddos": grade_task4,
    "task_5_zero_day": grade_task5,
}


# =========================
# MAIN GRADE FUNCTION
# =========================
def grade(state: CyberState) -> float:
    if state.task_id not in GRADER_MAP:
        raise ValueError(f"Unknown task: {state.task_id}")

    raw = GRADER_MAP[state.task_id](state)

    # penalty for too fast solving
    if len(state.actions_taken) <= 2:
        score -= 0.1

    # clamp (IMPORTANT for hackathon)
    return max(0.01, min(raw, 0.99))