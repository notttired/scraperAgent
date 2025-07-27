from abc import ABC, abstractmethod
from playwright.async_api import Page

class BaseLoader(ABC):

    @classmethod
    @abstractmethod
    def can_load(cls, url: str) -> bool:
        pass

    @abstractmethod
    async def get_url_content(self, url: str) -> str:
        """Fetch raw HTML from site URL"""
        pass

    @abstractmethod
    async def load_with_context(self, url: str) -> Page:
        """Keeps current session and loads link"""
        pass
