from models.page_element import PageElement
from abc import ABC, abstractmethod
from typing import List

class BaseExtractor(ABC):
    @abstractmethod
    def __init__(self, important_tags: List[str], content_tags: List[str]):
        pass

    @abstractmethod
    def extract(self, html_content: str, base_url: str = "") -> List[PageElement]:
        pass
