"""Calculators page object."""
from framework.pages.base_page import BasePage

class CalculatorsPage(BasePage):
    """Page object for SIP, SWP, and Inflation calculators."""
    
    # SIP Locators
    SIP_MONTHLY_INVESTMENT = "#monthlyInvestment" # guessing ID
    SIP_RATE = "#expectedreturn" # guessing ID, might need adjustment
    SIP_YEARS = "#timeperiod" # guessing ID
    SIP_TOTAL_VALUE = ".sip-result-value" # guessing class
    
    # SWP Locators
    SWP_TOTAL_INVESTMENT = "#totalInvestment"
    SWP_WITHDRAWAL = "#monthlyWithdrawal"
    SWP_RATE = "#expectedReturn"
    SWP_YEARS = "#timePeriod"
    
    # Inflation Locators
    INF_SALARY = "#currentSalary" # guess
    INF_EXPENSE = "#currentExpense"
    INF_AGE = "#currentAge"
    INF_RETIREMENT_AGE = "#retirementAge"
    
    async def navigate_sip(self):
        await self.navigate_to("http://localhost:4200/sip")

    async def navigate_swp(self):
        await self.navigate_to("http://localhost:4200/swp")

    async def navigate_inflation(self):
        await self.navigate_to("http://localhost:4200/inflation")
        
    async def calculate_sip(self, monthly: str, rate: str, years: str):
        # Using specific name attributes found in DOM
        await self.fill("input[name='amount']", str(monthly))
        await self.fill("input[name='expectedReturn']", str(rate))
        await self.fill("input[name='timePeriod']", str(years))
        
        await self.page.wait_for_timeout(500)

    async def get_sip_result(self) -> str:
        # Look for "Expected Amount" or similar text and get the value
        # Adjust selector if needed based on result DOM, but try generic text match first
        return await self.page.locator("text=Expected Amount").locator("xpath=..").inner_text()

    async def calculate_swp(self, investment: str, withdrawal: str, rate: str, years: str):
        await self.fill("input[name='totalInvestment']", str(investment))
        await self.fill("input[name='withdrawalPerMonth']", str(withdrawal))
        await self.fill("input[name='expectedReturn']", str(rate))
        await self.fill("input[name='timePeriod']", str(years))
        await self.page.wait_for_timeout(500)
    
    async def calculate_inflation(self, salary: str, expense: str, age: str, retirement: str):
        await self.fill("input[name='salary']", str(salary))
        await self.fill("input[name='expense']", str(expense))
        await self.fill("input[name='age']", str(age))
        await self.fill("input[name='retireAge']", str(retirement))
        
        # Ranges require special handling if fill doesn't work, but usually fill is fine for range in Playwright
        # If default test fails, we might need to use evaluatejs to set value
        await self.page.wait_for_timeout(500)

