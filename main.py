from core.scraper_agent import ScraperAgent
from core.loader_manager import LoaderManager
from core.parser_manager import ParserManager
from core.navigator_manager import NavigatorManager
from config.scraper_config import url, goal, important_tags, content_tags, concurrency_limit, browser_args, llm_client_args

from playwright.async_api import async_playwright
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(**browser_args) # type: ignore
        llm_client = OpenAI()
        loader_manager = LoaderManager(browser, concurrency_limit)
        parser_manager = ParserManager(important_tags, content_tags)
        navigator_manager = NavigatorManager(**llm_client_args)

        scraper_agent = ScraperAgent(loader_manager, parser_manager, navigator_manager)
        await scraper_agent.run(url, goal)
