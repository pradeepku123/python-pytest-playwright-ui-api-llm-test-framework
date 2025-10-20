import allure
import logging
import pytest

@allure.feature("Web Testing")
@allure.story("Page Navigation")
@pytest.mark.asyncio
async def test_page_title(page, config):
    logger = logging.getLogger(__name__)
    
    with allure.step("Navigate to homepage"):
        logger.info(f"Navigating to {config['base_url']}")
        await page.goto(config['base_url'])
    
    with allure.step("Verify page title"):
        title = await page.title()
        logger.info(f"Page title: {title}")
        assert title is not None
