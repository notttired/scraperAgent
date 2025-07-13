from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def __init__(self, link: str):
        self.link = link

    @abstractmethod
    async def load_site(self) -> str:
        """Fetch raw HTML from site URL"""
        pass

    @abstractmethod
    async def load_link(self, link: str) -> str:
        """Fetch raw HTML from given site URL"""
        pass

    @abstractmethod
    async def close(self):
        """Releases resources for termination"""
        pass
