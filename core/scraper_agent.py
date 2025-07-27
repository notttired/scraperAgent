from core.loader_manager import LoaderManager
from core.parser_manager import ParserManager
from core.navigator_manager import NavigatorManager
from models.page_context import PageContext, create_page_context

class BaseScraper:
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
        self.url = ""
        self.title = ""
        self.elements = []
        self.navigation_history = []
        self.current_goal = ""

    async def run(self, url: str, current_goal: str):
        self.clear()
        self.url = url
        self.current_goal = current_goal

        loader = await self.loader_manager.get_loader()
        parser = self.parser_manager.get_parser()
        navigator = self.navigator_manager.get_navigator()

        while True:
            html_content = await loader.load(url)
            self.title = parser.get_title(html_content)
            relevant_elements = parser.parse(html_content)
            page_context = create_page_context({
                "url": self.url,
                "title": self.title,
                "elements": relevant_elements,
                "navigation_history": self.navigation_history,
                "current_goal": self.current_goal
            })
            next_action = navigator.plan(page_context)
            if next_action.action_type == "Complete":
                break
                # extract
            # execute page action

            self.navigation_history.append(self.title)
