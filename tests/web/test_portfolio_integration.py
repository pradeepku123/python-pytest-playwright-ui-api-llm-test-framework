import pytest
import allure
import uuid
from framework.pages.login_page import LoginPage
from framework.pages.register_page import RegisterPage
from framework.pages.dashboard_page import DashboardPage
from framework.pages.portfolio_page import PortfolioPage

@allure.feature("Portfolio Integration")
class TestPortfolioIntegration:
    
    @allure.story("Add Investment and Verify Everywhere")
    @pytest.mark.asyncio
    async def test_add_investment_reflection(self, page):
        """
        Test flow:
        1. Register/Login
        2. Navigate to Portfolio
        3. Add Investment (Stock)
        4. Verify in Portfolio Table
        5. Navigate to Dashboard
        6. Verify Total Value updated (or at least contains some value)
        """
        register_page = RegisterPage(page)
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        portfolio_page = PortfolioPage(page)
        
        # 1. Login with Admin
        email = "admin" # User said username is admin
        password = "superadmin"
        
        await login_page.navigate()
        await login_page.login(email, password)
        await page.wait_for_url("**/dashboard")
        
        # 2. Navigate to Portfolio (via Dashboard link)
        await dashboard_page.navigate_to_portfolio()
        assert "/portfolio" in page.url
        
        # 3. Add Investment (Stock)
        stock_name = "Tech Corp"
        stock_amount = "1500" # 10 * 150
        await portfolio_page.add_investment("Stock", stock_name, stock_amount)
        
        # Add another investment (Gold)
        gold_name = "Gold ETF"
        gold_amount = "25000" # 5 * 5000
        # We need to wait for modal to disappear/reappear if we reuse the button
        # Assuming add_investment handles waiting for table update which implies modal closed
        await portfolio_page.add_investment("Gold", gold_name, gold_amount)

        # 4. Verify in Portfolio Table
        # Wait a bit for table update
        await page.wait_for_timeout(1000)
        names = await portfolio_page.get_investment_names()
        assert stock_name in names, f"Investment {stock_name} not found in portfolio table: {names}"
        assert gold_name in names, f"Investment {gold_name} not found in portfolio table: {names}"
        
        # 5. Navigate to Dashboard
        await dashboard_page.page.goto("http://localhost:4200/dashboard") # Or use menu
        
        # 6. Verify Dashboard Reflection
        # Value = (10*150) + (5*5000) = 1500 + 25000 = 26500
        await page.wait_for_timeout(1000)
        content = await page.content()
        # flexible check for comma or check for partial match
        assert "26,500" in content or "26500" in content, "Expected total value 26,500 not found in dashboard content"
