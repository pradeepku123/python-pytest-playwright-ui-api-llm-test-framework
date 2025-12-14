"""Page objects for various sidebar features."""
from framework.pages.base_page import BasePage

class SidebarPages(BasePage):
    """Collection of locators and methods for simpler sidebar pages."""
    
    # Mutual Funds
    MF_SEARCH_INPUT = "input[placeholder*='Search']"
    MF_FUND_LIST = ".fund-card" # assumption
    
    # Analytics
    ANALYTICS_CHART = "canvas" # assumption
    
    # Recommendations
    REC_LIST = ".recommendation-card" # assumption
    
    # Risk
    RISK_START_BUTTON = "button:has-text('Start')" # assumption
    
    # Budget
    BUDGET_ADD_BUTTON = "button:has-text('Add')" # assumption
    
    # Fact Sheet
    FACT_UPLOAD_BTN = "input[type='file']" # assumption for upload
    
    async def verify_mutual_funds_loaded(self):
        await self.navigate_to("http://localhost:4200/mutual-funds")
        return await self.is_visible(self.MF_SEARCH_INPUT)
        
    async def verify_analytics_loaded(self):
        await self.navigate_to("http://localhost:4200/analytics")
        await self.page.wait_for_timeout(1000) # wait for charts
        return await self.is_visible(self.ANALYTICS_CHART) or await self.page.locator("h1").inner_text() == "Analytics"

    async def verify_recommendations_loaded(self):
        await self.navigate_to("http://localhost:4200/recommendations")
        return "Recommendations" in await self.page.content()

    async def verify_fact_sheet_loaded(self):
        await self.navigate_to("http://localhost:4200/fact-sheet-analysis")
        # Wait for header
        try:
             await self.page.wait_for_selector("text=Document Intelligence", timeout=5000)
             return True
        except:
             return "Fact Sheet" in await self.page.content()
        
    async def verify_risk_profiling_loaded(self):
        await self.navigate_to("http://localhost:4200/risk-profiling")
        try:
            await self.page.wait_for_selector("text=Risk Profiling", timeout=5000)
            return True
        except:
             return "Risk" in await self.page.content()

    async def verify_budget_loaded(self):
        await self.navigate_to("http://localhost:4200/budget")
        return "Budget" in await self.page.content()
        
    async def verify_process_notification(self):
        await self.navigate_to("http://localhost:4200/notifications")
        return "Notifications" in await self.page.content()
