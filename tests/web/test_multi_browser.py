"""Multi-browser test example."""
import pytest
from framework.pages.base_page import BasePage


@pytest.mark.asyncio
async def test_page_title_all_browsers(page, config, browser_name):
    """Test page title across all browsers."""
    base_page = BasePage(page)
    await base_page.navigate_to(config['base_url'])
    title = await base_page.get_title()
    print(f"Browser: {browser_name}, Title: {title}")
    assert title is not None


@pytest.mark.parametrize("browser_name", ["chromium"])
@pytest.mark.asyncio
async def test_single_browser(page, config, browser_name):
    """Test with specific browser only."""
    base_page = BasePage(page)
    await base_page.navigate_to(config['base_url'])
    title = await base_page.get_title()
    assert "Playwright" in title