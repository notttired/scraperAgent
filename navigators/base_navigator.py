from models.navigation_action import NavigationAction
from models.page_context import PageContext

from openai import OpenAI
from abc import ABC, abstractmethod

class BaseNavigator(ABC):
    @abstractmethod
    def __init__(self, llm_client: OpenAI):
        pass

    @abstractmethod
    def plan(self, page_context: PageContext) -> NavigationAction:
        pass
