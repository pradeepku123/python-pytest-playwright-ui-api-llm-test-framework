"""Sample web test."""
import pytest
from playwright.async_api import expect
from framework.pages.home_page import HomePage

@pytest.mark.asyncio
async def test_page_obj_interactions(page, config):
    """
    Test using Page Object Model.
    Verifies navigation, title, and "Get started" link interaction.
    """
    home_page = HomePage(page)
    
    # Navigation
    await home_page.navigate_to(config['base_url'])
    
    # Title Verification
    title = await home_page.get_title()
    assert "Playwright" in title
    
    # Interaction
    await home_page.click_get_started()
    await expect(page).to_have_url(f"{config['base_url']}/docs/intro")
