from loaders.base_loader import BaseLoader
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from loaders.context_pool import ContextPool

class JSLoader(BaseLoader):
    def __init__(self, context_pool):
        self.context_pool: ContextPool = context_pool
        self.context_id = 0
        self.context = None

    @classmethod
    def can_load(cls, url: str) -> bool:
        return True
    
    async def load(self, url: str) -> str:
        with self.context_pool.session() as page:
            await page.goto(url)
            html_content = await page.content()
        return html_content

    async def load_with_context(self, url: str) -> str:
        if not self.context:
            self.context_id, self.context = await self.context_pool.acquire_context()
        page = await self.context.new_page()
        await page.goto(url)
        html_content = await page.content()
        return html_content
