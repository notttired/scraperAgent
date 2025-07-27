from contextlib import contextmanager
import asyncio

class ContextPool:
    def __init__(self, browser, limit: int):
        self.count = 0
        self.browser = browser
        self.context_pool = {} # single operation => thread safe
        self.semaphore = asyncio.Semaphore(limit)

    @contextmanager
    def session(self):
        context = self.browser.new_context()
        page = context.new_page()
        try:
            yield page
        finally:
            page.close()
            context.close()

    def generate_id(self) -> int:
        self.count += 1
        return self.count

    async def acquire_context(self):
        await self.semaphore.acquire()
        context = self.browser.new_context()
        id = self.generate_id()
        self.context_pool[id] = context
        return (self.generate_id(), context)
    
    async def release_context(self, id: int):
        await self.context_pool[id].close()
        del self.context_pool[id]
        self.semaphore.release()
    
    async def release_page(self, key: int):
        await self.context_pool[key].close()

    async def __del__(self):
        self.browser.close()
        for context_key in self.context_pool.keys():
            await self.context_pool[context_key].close()
