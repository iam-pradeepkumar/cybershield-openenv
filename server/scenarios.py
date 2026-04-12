from typing import Any

# =============================
# BASE HEALTHY SYSTEM TEMPLATE
# =============================

BASE_SYSTEM = {
    "auth-server": {"status": "healthy", "cpu": 10, "memory": 30, "alerts": 0},
    "db-server":   {"status": "healthy", "cpu": 20, "memory": 40, "alerts": 0},
    "web-server":  {"status": "healthy", "cpu": 15, "memory": 35, "alerts": 0},
    "firewall":    {"status": "healthy", "cpu": 5,  "memory": 20, "alerts": 0},
}

# =============================
# TASK 1 — BRUTE FORCE (EASY)
# =============================

TASK1 = {
    "task_id": "task_1_bruteforce",
    "difficulty": "easy",
    "description": "Multiple failed login attempts detected. Investigate and secure the system.",
    "max_steps": 10,

    "systems": {
        **BASE_SYSTEM,
        "auth-server": {"status": "under_attack", "cpu": 40, "memory": 50, "alerts": 25},
    },

    "logs": {
        "auth-server": [
            "Failed login attempt from IP 192.168.1.10",
            "Failed login attempt from IP 192.168.1.10",
            "Failed login attempt from IP 192.168.1.10",
            "WARNING: Possible brute force attack detected",
        ]
    },

    "solution": {
        "action_type": "block_ip",
        "target": "192.168.1.10"
    }
}

# =============================
# TASK 2 — MALWARE (MEDIUM)
# =============================

TASK2 = {
    "task_id": "task_2_malware",
    "difficulty": "medium",
    "description": "System performance degraded. Investigate possible malware infection.",
    "max_steps": 12,

    "systems": {
        **BASE_SYSTEM,
        "web-server": {"status": "compromised", "cpu": 95, "memory": 85, "alerts": 40},
    },

    "logs": {
        "web-server": [
            "Unknown process running: crypto_miner.exe",
            "CPU usage spike detected",
            "Suspicious outbound traffic to 45.33.32.156",
        ],
        "db-server": [
            "Normal database activity"
        ]
    },

    "solution": {
        "action_type": "isolate_host",
        "target": "web-server"
    }
}

# =============================
# TASK 3 — PHISHING (MEDIUM)
# =============================

TASK3 = {
    "task_id": "task_3_phishing",
    "difficulty": "medium",
    "description": "Suspicious login from unknown location. Possible credential compromise.",
    "max_steps": 12,

    "systems": {
        **BASE_SYSTEM,
        "auth-server": {"status": "breached", "cpu": 30, "memory": 40, "alerts": 15},
    },

    "logs": {
        "auth-server": [
            "Login from IP 203.0.113.5 (Unknown location)",
            "User admin logged in successfully",
            "Unusual access pattern detected",
        ]
    },

    "solution": {
        "action_type": "revoke_access",
        "target": "admin_account"
    }
}

# =============================
# TASK 4 — DDOS (HARD)
# Fixed: solution now uses block_ip to match the grader check
# =============================

TASK4 = {
    "task_id": "task_4_ddos",
    "difficulty": "hard",
    "description": "Massive traffic spike detected. Identify and mitigate the DDoS attack.",
    "max_steps": 15,

    "systems": {
        **BASE_SYSTEM,
        "web-server": {"status": "overloaded", "cpu": 99, "memory": 90, "alerts": 100},
    },

    "logs": {
        "web-server": [
            "Traffic spike: 10000 requests/sec from multiple IPs",
            "Multiple IPs flooding /api endpoint",
            "Possible DDoS attack from IP range 198.51.100.0/24",
            # Red herring
            "Disk space warning from last week",
        ]
    },

    "solution": {
        "action_type": "block_ip",
        "target": "multiple"
    }
}

# =============================
# TASK 5 — ZERO DAY (HARD)
# =============================

TASK5 = {
    "task_id": "task_5_zero_day",
    "difficulty": "hard",
    "description": "Subtle system anomaly detected. No obvious errors. Investigate carefully.",
    "max_steps": 15,

    "systems": {
        **BASE_SYSTEM,
        "db-server": {"status": "compromised", "cpu": 60, "memory": 70, "alerts": 10},
    },

    "logs": {
        "db-server": [
            "Unusual query execution pattern",
            "Hidden privilege escalation detected",
            "Unknown root access granted silently",
        ]
    },

    "solution": {
        "action_type": "patch_system",
        "target": "db-server"
    }
}

# =============================
# TASK MAP
# =============================

TASK_MAP = {
    "task_1_bruteforce": TASK1,
    "task_2_malware":    TASK2,
    "task_3_phishing":   TASK3,
    "task_4_ddos":       TASK4,
    "task_5_zero_day":   TASK5,
}

ALL_TASKS = list(TASK_MAP.values())
