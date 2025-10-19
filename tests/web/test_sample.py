"""Sample web test."""
import pytest
from framework.pages.base_page import BasePage


@pytest.mark.asyncio
async def test_page_title(page, config):
    """Test page title."""
    base_page = BasePage(page)
    await base_page.navigate_to(config['base_url'])
    title = await base_page.get_title()
    assert title is not None