import pytest
import allure
from framework.pages.login_page import LoginPage

@allure.feature("Wealth App Login")
class TestWealthAppLogin:
    
    @allure.story("Login Page UI")
    @pytest.mark.asyncio
    async def test_login_page_elements(self, page):
        """Verify that all essential elements are present on the login page."""
        login_page = LoginPage(page)
        await login_page.navigate()
        
        # Verify title
        assert "WealthFrontend" in await login_page.get_title()
        
        # Verify inputs and buttons
        assert await login_page.is_visible(login_page.USERNAME_INPUT), "Username input not visible"
        assert await login_page.is_visible(login_page.PASSWORD_INPUT), "Password input not visible"
        assert await login_page.is_visible(login_page.LOGIN_BUTTON), "Login button not visible"
        assert await login_page.is_visible(login_page.SIGN_UP_LINK), "Sign up link not visible"

    @allure.story("Login Functionality")
    @pytest.mark.asyncio
    async def test_login_failure_invalid_creds(self, page):
        """Verify login failure with invalid credentials."""
        login_page = LoginPage(page)
        await login_page.navigate()
        
        await login_page.login("invalid_user", "wrong_password")
        
        # Taking a screenshot for debugging potentially (although allure does this on failure usually)
        # Check for error message or that we are still on the login page
        # Since I don't know the exact behavior, I'll check if the URL is still login
        # or if an error message appears. For now, asserting we are still on login page.
        assert "/login" in page.url
