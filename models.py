from typing import Any, Dict, List, Optional
from openenv.core.env_server import Action, Observation, State
from pydantic import Field


# ACTIONS (what the agent can do)
class CyberAction(Action):
    action_type: str = ""
    target: str = ""
    parameters: Dict[str, Any] = Field(default_factory=dict)


# OBSERVATION (what the agent sees after each step)
class CyberObservation(Observation):
    output: str = ""
    systems: Dict[str, Any] = Field(default_factory=dict)
    alerts: List[str] = Field(default_factory=list)

    success: bool = True
    error: str = ""

    steps_remaining: Optional[int] = None
    partial_score: float = 0.0


# STATE (internal tracking used by graders)
class CyberState(State):
    task_id: str = ""

    actions_taken: List[Dict[str, Any]] = Field(default_factory=list)

    attack_identified: bool = False
    fix_applied: bool = False
    system_secured: bool = False

    current_score: float = 0.0
