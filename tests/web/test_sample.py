"""Sample web test."""
import pytest
from framework.pages.base_page import BasePage
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_page_title(page, config):
    """Test page title."""
    base_page = BasePage(page)
    await base_page.navigate_to(config['base_url'])
    # Use Playwright's expect on the page to check the title
    expected = (
        'Fast and reliable end-to-end testing for modern web apps | Playwright'
    )
    await expect(page).to_have_title(expected)
