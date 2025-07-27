from models.navigation_action import NavigationAction

from abc import ABC, abstractmethod

class BaseAction(ABC):
    def __init__(self, action: NavigationAction):
        self.action = action

    @abstractmethod
    def execute_action(self):
        pass
