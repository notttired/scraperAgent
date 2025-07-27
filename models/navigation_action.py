from models.action_type import ActionType
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class NavigationAction:
    action_type: ActionType
    target: str
    reasoning: str
    confidence: float
    metadata: Dict[str, str | List[str]] = {}
