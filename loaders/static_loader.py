from loaders.base_loader import BaseLoader
import requests

class StaticLoader(BaseLoader):
    @classmethod
    def can_load(cls) -> bool:
        return True

    async def load(self, url: str) -> str:
        response = requests.get(url)
        text = response.text
        return text
    
    async def load_with_context(self, url: str) -> str:
        return await self.load(url)
