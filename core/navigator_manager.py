from navigators.base_navigator import BaseNavigator
from navigators.complex_navigator import ComplexNavigator

from openai import OpenAI

class NavigatorManager:
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client

    def get_navigator(self) -> BaseNavigator:
        return ComplexNavigator(self.llm_client)
