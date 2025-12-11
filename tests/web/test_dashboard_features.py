import pytest
import allure
import uuid
from framework.pages.login_page import LoginPage
from framework.pages.register_page import RegisterPage
from framework.pages.dashboard_page import DashboardPage

@allure.feature("Dashboard Features")
class TestDashboardNavigation:
    
    @pytest.fixture(scope="function")
    async def dashboard(self, page):
        """Helper to register, login, and return dashboard page."""
        register_page = RegisterPage(page)
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # Register
        unique_id = str(uuid.uuid4())[:8]
        username = f"user_{unique_id}"
        email = f"user_{unique_id}@example.com"
        password = "Password123!"
        full_name = f"Test User {unique_id}"
        
        await register_page.navigate()
        await register_page.register_user(full_name, email, username, password)
        await page.wait_for_url("**/login")
        
        # Login
        await page.wait_for_timeout(1000)
        await login_page.login(email, password)
        await page.wait_for_url("**/dashboard")
        
        return dashboard_page

    @allure.story("Navigation to Main Features")
    @pytest.mark.asyncio
    async def test_navigation_menu(self, dashboard, page):
        """Verify navigation to all main features."""
        
        # 1. Mutual Funds
        await dashboard.navigate_to_mutual_funds()
        await page.wait_for_url("**/mutual-funds")
        assert "/mutual-funds" in page.url
        
        # 2. Portfolio
        await dashboard.navigate_to_portfolio()
        await page.wait_for_url("**/portfolio")
        assert "/portfolio" in page.url
        
        # 3. Goals
        await dashboard.navigate_to_goals()
        await page.wait_for_url("**/goals")
        assert "/goals" in page.url
        
        # 4. Budget
        await dashboard.navigate_to_budget()
        await page.wait_for_url("**/budget")
        assert "/budget" in page.url

        # 5. Analytics
        await dashboard.navigate_to_analytics()
        await page.wait_for_url("**/analytics")
        assert "/analytics" in page.url
