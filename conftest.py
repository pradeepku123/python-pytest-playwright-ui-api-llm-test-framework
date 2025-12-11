"""Global pytest configuration."""
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from framework.utils.config_reader import get_config
from framework.utils.logger import setup_logger

# Setup logging
setup_logger()

@pytest.fixture(scope="session")
def config():
    """Configuration fixture."""
    return get_config()

@pytest.fixture(scope="session")
def browser_type_launch_args(config, request):
    """
    Browser type launch arguments.
    Can be customized based on config and CLI arguments.
    """
    headless = config.get('headless', True)
    if request.config.getoption("--headed"):
        headless = False
        
    launch_args = {
        "headless": headless,
        "slow_mo": config.get('slow_mo', 0),
        "args": []
    }

    if not headless:
        launch_args["args"].append("--start-maximized")
        
    return launch_args

@pytest.fixture(scope="session")
def browser_context_args(request):
    """
    Browser context arguments.
    """
    if request.config.getoption("--headed"):
        return {"viewport": {"width": 1920, "height": 1080}}
    else:
        return {"viewport": {"width": 1920, "height": 1080}}

@pytest.fixture(scope="session")
def browser_name(request):
    """Browser name fixture (can be parameterized if needed via CLI)."""
    return request.config.getoption("--browser") if request.config.getoption("--browser") else "chromium"

def pytest_addoption(parser):
    """Add CLI options."""
    parser.addoption("--browser", action="store", default="chromium", help="Browser to run tests on")
    parser.addoption("--headed", action="store_true", help="Run tests in headed mode")

@pytest_asyncio.fixture(scope="function")
async def browser_instance(browser_name, browser_type_launch_args):
    """
    Function-scoped browser instance.
    Launches the browser for each test to ensure isolation and stability.
    """
    async with async_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = await browser_type.launch(**browser_type_launch_args)
        yield browser
        await browser.close()

@pytest_asyncio.fixture(scope="function")
async def context(browser_instance, browser_context_args):
    """
    Function-scoped browser context.
    Creates a new context for each test to ensure isolation.
    """
    context = await browser_instance.new_context(**browser_context_args)
    yield context
    await context.close()

@pytest_asyncio.fixture(scope="function")
async def page(context):
    """
    Function-scoped page fixture.
    Creates a new page within the context.
    """
    page = await context.new_page()
    yield page
    # Page is closed automatically when context closes
