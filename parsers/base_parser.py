from models.page_element import PageElement
from abc import ABC, abstractmethod
from playwright.async_api import Page
from typing import List

class BaseParser(ABC):
    @abstractmethod
    def __init__(self, important_tags: List[str], content_tags: List[str]):
        pass

    @abstractmethod
    async def parse(self, page: Page, base_url: str = "") -> List[PageElement]:
        pass

    @abstractmethod
    async def get_title(self, page: Page) -> str:
        pass
