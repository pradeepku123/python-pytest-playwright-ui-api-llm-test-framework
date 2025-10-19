import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from framework.utils.config_reader import get_config


@pytest.fixture(scope="session")
def config():
    """Configuration fixture."""
    return get_config()


@pytest_asyncio.fixture(scope="function")
async def page(config):
    """Page fixture."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=config.get('headless', True))
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()
