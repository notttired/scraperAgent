from models.action_type import ActionType
from dataclasses import dataclass
from typing import Dict, List, cast

@dataclass
class NavigationAction:
    action_type: ActionType
    target: str
    reasoning: str
    confidence: float
    metadata: Dict[str, str | List[str]] = {}

def create_navigation_action(action: Dict[str, str | float]):
    return NavigationAction(
        action_type = ActionType["action_type"],
        target = cast(str, action["target"]),
        reasoning = cast(str, action["reasoning"]),
        confidence = cast(float, action["confidence"])
    )
