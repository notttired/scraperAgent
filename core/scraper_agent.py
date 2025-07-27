from core.loader_manager import LoaderManager
from core.parser_manager import ParserManager
from core.navigator_manager import NavigatorManager
from actions.base_action import BaseAction
from actions.navigate_to import NavigateTo
from actions.no_action import NoAction
from models.action_type import ActionType
from models.navigation_action import NavigationAction
from models.page_context import PageContext, create_page_context

from playwright.async_api import Page
from typing import List

class BaseScraper:
    page = None
    url = ""
    title = ""
    elements = []
    navigation_history = []
    current_goal = ""

    async def __init__(self, loader_manager: LoaderManager, parser_manager: ParserManager, navigator_manager: NavigatorManager):
        self.loader_manager = loader_manager # May take browser as argument
        self.parser_manager = parser_manager
        self.navigator_manager = navigator_manager

    def clear(self):
        self.page = None
        self.url = ""
        self.title = ""
        self.elements = []
        self.navigation_history = []
        self.current_goal = ""

    def decide_action(self, action: NavigationAction) -> BaseAction:
        if NavigationAction.action_type == ActionType.NAVIGATE_TO:
            return NavigateTo(action, self.loader)
        else:
            return NoAction(action)

    async def run(self, url: str, current_goal: str):
        self.clear()
        self.url = url
        self.current_goal = current_goal

        self.loader = await self.loader_manager.get_loader() 
        self.parser = self.parser_manager.get_parser()
        self.navigator = self.navigator_manager.get_navigator()

        self.page = await self.loader.load_with_context(url)

        while True:
            self.title = self.parser.get_title(self.page)
            relevant_elements = self.parser.parse(self.page, self.url)
            page_context = create_page_context({
                "url": self.url,
                "title": self.title,
                "elements": relevant_elements,
                "navigation_history": self.navigation_history,
                "current_goal": self.current_goal
            })
            next_action = self.navigator.plan(page_context)
            if next_action.action_type == "Complete":
                return await self.page.screenshot(path='fullpage.png', full_page=True)
                break
                
            action_results = self.decide_action(next_action).execute_action()
            if type(action_results) == str: # Avoids linter error
                return await self.page.screenshot(path='fullpage.png', full_page=True)
            elif type(action_results) == Page:
                self.page = action_results
                
            if (self.title != self.navigation_history[-1]):
                self.navigation_history.append(self.title)
