from loaders.base_loader import BaseLoader
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

class JSLoader(BaseLoader):
    def __init__(self, link: str, browser: Browser, context: BrowserContext, page: Page):
        super().__init__(link)
        self.browser = browser
        self.context = context
        self.page = page

    @classmethod
    async def create(cls, link: str, browser: Browser):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            return cls(link, browser, context, page)

    async def load_site(self) -> str:
        await self.page.goto(self.link)
        html: str = await self.page.content()
        return html
        
    
    async def load_link(self, link: str) -> str:
        await self.page.goto(self.link)
        html: str = await self.page.content()
        return html
    
    async def close(self):
        pass
