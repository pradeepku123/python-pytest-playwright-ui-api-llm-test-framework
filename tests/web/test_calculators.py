import pytest
import allure
from framework.pages.login_page import LoginPage
from framework.pages.calculators_page import CalculatorsPage

@allure.feature("Financial Calculators")
class TestCalculators:
    
    @allure.story("SIP Calculator")
    @allure.story("SIP Calculator")
    @pytest.mark.asyncio
    async def test_sip_calculator(self, page):
        login_page = LoginPage(page)
        calc_page = CalculatorsPage(page)
        
        await login_page.navigate()
        await login_page.login("admin", "superadmin")
        await page.wait_for_url("**/dashboard")
        
        await calc_page.navigate_sip()
        # await page.wait_for_url("**/sip") # Remove explicit wait if flaky
        await page.wait_for_selector("input[name='amount']") # Wait for element instead
        
        # Test Calculation
        await calc_page.calculate_sip("5000", "12", "10")
        
        # Verify Key Result
        content = await page.content()
        assert "Total Value" in content or "Est. Returns" in content

    @allure.story("SWP Calculator")
    @pytest.mark.asyncio
    async def test_swp_calculator(self, page):
        # Assuming login session persists or we relogin if fixture not used
        # Better to reuse login fixture if available, but for now specific flow
        calc_page = CalculatorsPage(page)
        # If not logged in, login again? Or rely on session cookie if sequential?
        # Let's ensure navigation works
        await calc_page.navigate_swp()
        # Simple check if redirected to login
        if "login" in page.url:
             login_page = LoginPage(page)
             await login_page.login("admin", "superadmin")
             await page.wait_for_url("**/dashboard")
             await calc_page.navigate_swp()
             
        await page.wait_for_selector("input[name='totalInvestment']")
        await calc_page.calculate_swp("1000000", "5000", "8", "10")
        content = await page.content()
        assert "Final Balance" in content or "Total Withdrawal" in content

    @allure.story("Inflation Calculator")
    @pytest.mark.asyncio
    async def test_inflation_calculator(self, page):
        calc_page = CalculatorsPage(page)
        await calc_page.navigate_inflation()
        if "login" in page.url:
             login_page = LoginPage(page)
             await login_page.login("admin", "superadmin")
             await page.wait_for_url("**/dashboard")
             await calc_page.navigate_inflation()

        await page.wait_for_selector("input[name='salary']")
        await calc_page.calculate_inflation("100000", "50000", "30", "60")
        content = await page.content()
        assert "Corpus" in content or "Monthly Expense" in content
