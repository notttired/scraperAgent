from abc import ABC, abstractmethod

class BaseLoader(ABC):

    @classmethod
    @abstractmethod
    def can_load(cls, url: str) -> bool:
        pass

    @abstractmethod
    async def load(self, url: str) -> str:
        """Fetch raw HTML from site URL"""
        pass

    @abstractmethod
    async def load_with_context(self, url: str) -> str:
        """Keeps current session and loads link"""
        pass
