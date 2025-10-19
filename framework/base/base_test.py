import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from framework.utils.config_reader import get_config


@pytest.fixture(scope="session")
def config():
    """Configuration fixture."""
    return get_config()


@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser_name(request):
    """Browser name fixture."""
    return request.param


@pytest_asyncio.fixture(scope="function")
async def page(config, browser_name):
    """Page fixture."""
    async with async_playwright() as p:
        browser = getattr(p, browser_name)
        headless = config.get('headless', True)
        browser_instance = await browser.launch(headless=headless)
        context = await browser_instance.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser_instance.close()
