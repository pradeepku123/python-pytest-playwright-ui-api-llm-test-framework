"""Sample web test."""
import pytest
from framework.pages.base_page import BasePage
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_page_title(page, config):
    """Test page title."""
    base_page = BasePage(page)
    await base_page.navigate_to(config['base_url'])
    title = await base_page.get_title()
    await expect(title).to_be('Fast and reliable end-to-end testing for modern web apps | Playwright')