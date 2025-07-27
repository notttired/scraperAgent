from core.loader_manager import LoaderManager
from core.parser_manager import ParserManager
from core.navigator_manager import NavigatorManager

class BaseScraper:
    async def __init__(self, loader_manager: LoaderManager, parser_manager: ParserManager, navigator_manager: NavigatorManager):
        self.loader_manager = loader_manager # May take browser as argument
        self.parser_manager = parser_manager
        self.navigator_manager = navigator_manager

    async def run(self, url):
        loader = await self.loader_manager.get_loader()
        parser = self.parser_manager.get_parser()
        navigator = self.navigator_manager.get_navigator()

        while True:
            html_content = await loader.load(url)
            relevant_elements = parser.parse(html_content)
            # page_context = ...
            # next_action = navigator.plan(page_context)
            # if next_action.action.action_type == "Complete":
            #     extract && break
        while not self.navigator.should_stop():
            
            extracted = self.extractors.extract(html)
            action = self.navigator.decide_next_action(extracted)
            self.scraper.execute_action(action)
