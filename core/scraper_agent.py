from core.loader_manager import LoaderManager
from core.extractor_manager import ExtractorManager

class BaseScraper:
    async def __init__(self, loader_manager: LoaderManager, extractor_manager: ExtractorManager):
        self.loader_manager = loader_manager # May take browser as argument
        self.extractor_manager = extractor_manager

    async def run(self):
        loader = await self.loader_manager.get_loader()
        extractor = self.extractor_manager.get_extractor()
        while not self.navigator.should_stop():
            
            extracted = self.extractors.extract(html)
            action = self.navigator.decide_next_action(extracted)
            self.scraper.execute_action(action)
