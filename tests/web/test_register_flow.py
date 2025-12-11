import pytest
import allure
import uuid
from framework.pages.login_page import LoginPage
from framework.pages.register_page import RegisterPage
from framework.pages.dashboard_page import DashboardPage

@allure.feature("User Registration and Login Flow")
class TestUserRegistration:
    
    @allure.story("Register and Login")
    @pytest.mark.asyncio
    async def test_register_and_login_new_user(self, page):
        """
        Test flow:
        1. Navigate to Register Page
        2. Register a new user
        3. Verify redirect to Login Page
        4. Login with new credentials
        5. Verify redirect to Dashboard
        """
        register_page = RegisterPage(page)
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # Generate unique user data
        unique_id = str(uuid.uuid4())[:8]
        username = f"user_{unique_id}"
        email = f"user_{unique_id}@example.com"
        password = "Password123!"
        full_name = f"Test User {unique_id}"
        
        # 1. Navigate to Register
        await register_page.navigate()
        
        # 2. Register
        await register_page.register_user(full_name, email, username, password)
        
        # 3. Verify Redirect to Login (assuming this behavior)
        # We might need to wait for URL change
        await page.wait_for_url("**/login")
        assert "/login" in page.url
        
        # 4. Login
        await page.wait_for_timeout(1000) # Wait for animation/load
        await login_page.login(email, password)
        
        # 5. Verify Dashboard
        try:
            await page.wait_for_url("**/dashboard", timeout=10000)
            assert await dashboard_page.is_loaded()
        except Exception as e:
            # Capture screenshot on failure
            await page.screenshot(path="reports/login_failure.png")
            current_url = page.url
            content = await page.content()
            pytest.fail(f"Login failed. Current URL: {current_url}. Error: {e}")
