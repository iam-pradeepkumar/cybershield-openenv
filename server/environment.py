from __future__ import annotations
import copy
import uuid
from typing import Any

from openenv.core.env_server import Environment
from models import CyberAction, CyberObservation, CyberState
from server.scenarios import TASK_MAP


class CyberEnvironment(Environment):
    def __init__(self) -> None:
        super().__init__()
        self._state: CyberState = CyberState()
        self._scenario: dict[str, Any] = {}
        self._systems: dict[str, Any] = {}
        self._logs: dict[str, list[str]] = {}

    def reset(self, task_id: str | None = None, **kwargs: Any) -> CyberObservation:
        if not task_id:
            task_id = "task_1_bruteforce"

        if task_id not in TASK_MAP:
            raise ValueError(f"Unknown task_id: {task_id}")

        scenario = TASK_MAP[task_id]

        self._scenario = scenario
        self._systems = copy.deepcopy(scenario["systems"])
        self._logs = copy.deepcopy(scenario["logs"])

        self._state = CyberState(
            episode_id=str(uuid.uuid4()),
            task_id=scenario["task_id"],
            step_count=0,
            actions_taken=[],
            attack_identified=False,
            fix_applied=False,
            system_secured=False,
            current_score=0.0,
        )

        return CyberObservation(
            output=f"🚨 {scenario['description']}",
            systems=self._systems,
            done=False,
            success=True,
            steps_remaining=scenario["max_steps"],
            partial_score=0.0,
        )

    def step(self, action: CyberAction, **kwargs: Any) -> CyberObservation:
        self._state.step_count += 1
        max_steps = self._scenario["max_steps"]

        self._state.actions_taken.append({
            "action_type": action.action_type,
            "target": action.target
        })

        obs = self._dispatch(action)

        # done logic
        if self._state.system_secured:
            obs.done = True
            obs.output += "\n✅ System secured!"
        elif self._state.step_count >= max_steps:
            obs.done = True
            obs.output += "\n❌ Max steps reached"

        prev_score = self._state.current_score
        self._state.current_score = self._calculate_score()

        obs.reward = round(self._state.current_score - prev_score, 4)
        obs.steps_remaining = max_steps - self._state.step_count
        obs.partial_score = self._state.current_score
        obs.systems = self._systems

        return obs

    def _dispatch(self, action: CyberAction) -> CyberObservation:
        handlers = {
            "scan_logs": self._handle_scan_logs,
            "block_ip": self._handle_block_ip,
            "isolate_host": self._handle_isolate,
            "patch_system": self._handle_patch,
            "revoke_access": self._handle_revoke,
        }

        handler = handlers.get(action.action_type)

        if not handler:
            return CyberObservation(
                output="Invalid action",
                systems=self._systems,
                success=False,
                error="Unknown action"
            )

        return handler(action)

    # ===== ACTIONS =====

    def _handle_scan_logs(self, action: CyberAction):
        self._state.attack_identified = True
        logs = self._logs.get(action.target, [])

        return CyberObservation(
            output="\n".join(logs),
            systems=self._systems
        )

    def _handle_block_ip(self, action: CyberAction):
        # requires investigation first
        if (
            self._state.attack_identified and
            self._scenario["solution"]["action_type"] == "block_ip"
        ):
            self._state.fix_applied = True
            self._state.system_secured = True

        return CyberObservation(output="IP blocked", systems=self._systems)

    def _handle_isolate(self, action: CyberAction):
        if (
            self._state.attack_identified and
            self._scenario["solution"]["action_type"] == "isolate_host"
        ):
            self._state.fix_applied = True
            self._state.system_secured = True

        return CyberObservation(output="Host isolated", systems=self._systems)

    def _handle_patch(self, action: CyberAction):
        if (
            self._state.attack_identified and
            self._scenario["solution"]["action_type"] == "patch_system"
        ):
            self._state.fix_applied = True
            self._state.system_secured = True

        return CyberObservation(output="System patched", systems=self._systems)

    def _handle_revoke(self, action: CyberAction):
        if (
            self._state.attack_identified and
            self._scenario["solution"]["action_type"] == "revoke_access"
        ):
            self._state.fix_applied = True
            self._state.system_secured = True

        return CyberObservation(output="Access revoked", systems=self._systems)

    # ===== SCORING =====

    def _calculate_score(self):
        score = 0.0

        if self._state.attack_identified:
            score += 0.3

        if self._state.fix_applied:
            score += 0.3

        if self._state.system_secured:
            score += 0.4

        # penalty for rushing
        if self._state.step_count <= 2:
            score -= 0.1

        return max(0.0, min(score, 1.0))

    @property
    def state(self):
        return self._state