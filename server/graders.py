from typing import Any
from models import CyberState


# =========================
# HELPER
# =========================
def _has_action(actions, action_type):
    return any(a.get("action_type") == action_type for a in actions)


def _correct_target(actions, expected_target):
    return any(a.get("target") == expected_target for a in actions)


def _correct_sequence(actions, expected_sequence):
    seq = [a.get("action_type") for a in actions]
    return seq[:len(expected_sequence)] == expected_sequence


def _has_repeated_same_target(actions):
    """Penalize only if the exact same (action_type, target) pair is repeated."""
    seen = set()
    for a in actions:
        key = (a.get("action_type"), a.get("target"))
        if key in seen:
            return True
        seen.add(key)
    return False


# =========================
# TASK 1 — EASY (brute force)
# =========================
def grade_task1(state: CyberState) -> float:
    score = 0.0
    actions = state.actions_taken

    if _has_action(actions, "scan_logs"):
        score += 0.3

    if _correct_target(actions, "192.168.1.10"):
        score += 0.3

    if _correct_sequence(actions, ["scan_logs", "block_ip"]):
        score += 0.2

    if state.system_secured:
        score += 0.4

    if _has_repeated_same_target(actions):
        score -= 0.1

    return min(score, 1.0)


# =========================
# TASK 2 — MEDIUM (malware)
# =========================
def grade_task2(state: CyberState) -> float:
    score = 0.0
    actions = state.actions_taken

    if _has_action(actions, "scan_logs"):
        score += 0.2

    if _has_action(actions, "isolate_host"):
        score += 0.3

    if state.system_secured:
        score += 0.4

    if _has_action(actions, "block_ip"):
        score -= 0.1

    if len(actions) >= 3:
        score += 0.1

    if _has_repeated_same_target(actions):
        score -= 0.1

    return max(0.0, min(score, 1.0))


# =========================
# TASK 3 — MEDIUM (phishing)
# =========================
def grade_task3(state: CyberState) -> float:
    score = 0.0
    actions = state.actions_taken

    if _has_action(actions, "scan_logs"):
        score += 0.2

    if _has_action(actions, "revoke_access"):
        score += 0.4

    if state.system_secured:
        score += 0.4

    if _has_repeated_same_target(actions):
        score -= 0.1

    return min(score, 1.0)


# =========================
# TASK 4 — HARD (DDoS)
# Fixed: solution and grader now both use block_ip consistently
# =========================
def grade_task4(state: CyberState) -> float:
    score = 0.0
    actions = state.actions_taken

    if _has_action(actions, "scan_logs"):
        score += 0.2

    if _has_action(actions, "block_ip"):
        score += 0.3

    if len(actions) >= 3:
        score += 0.2

    if state.system_secured:
        score += 0.3

    if _has_action(actions, "patch_system"):
        score -= 0.2

    if _has_repeated_same_target(actions):
        score -= 0.1

    return max(0.0, min(score, 1.0))


# =========================
# TASK 5 — HARD (zero-day)
# =========================
def grade_task5(state: CyberState) -> float:
    score = 0.0
    actions = state.actions_taken

    if _has_action(actions, "scan_logs"):
        score += 0.2

    if _has_action(actions, "patch_system"):
        score += 0.4

    if len(actions) >= 3:
        score += 0.2

    if state.system_secured:
        score += 0.3

    if _has_repeated_same_target(actions):
        score -= 0.1

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

    # Penalty for solving too fast (rushing without investigation)
    if len(state.actions_taken) <= 2:
        raw -= 0.1

    # Clamp to hackathon range (IMPORTANT)
    return max(0.01, min(raw, 0.99))
