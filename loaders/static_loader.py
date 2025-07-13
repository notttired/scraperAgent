from loaders.base_loader import BaseLoader
import requests

class StaticLoader(BaseLoader):
    def __init__(self, link: str):
        super().__init__(link)

    async def load_site(self) -> str:
        response = requests.get(self.link)
        text = response.text
        return text

    async def load_link(self, link: str) -> str:
        response = requests.get(link)
        text = response.text
        return text

    async def close(self):
        pass
