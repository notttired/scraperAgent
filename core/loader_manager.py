from loaders.base_loader import BaseLoader
from loaders.static_loader import StaticLoader
from loaders.js_loader import JSLoader
from loaders.context_pool import ContextPool
from playwright.async_api import Browser
from typing import Optional

class LoaderManager:
    def __init__(self, browser: Optional[Browser] = None, concurrency_limit: int = 10):
        self.browser = browser
        self.concurrency_limit = 10
        self.context_pool = None
        if self.browser:
            self.context_pool = ContextPool(browser, concurrency_limit)

    async def get_loader(self) -> BaseLoader:
        if self.context_pool:
            return JSLoader(self.context_pool)
        else:
            return StaticLoader()
