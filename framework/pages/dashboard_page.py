"""Dashboard page object."""
from framework.pages.base_page import BasePage

class DashboardPage(BasePage):
    """Dashboard page object."""
    
    URL = "http://localhost:4200/dashboard"
    
    # Sidebar/Menu Locators
    MENU_DASHBOARD = "a[href='/dashboard']"
    MENU_MUTUAL_FUNDS = "a[href='/mutual-funds']"
    MENU_PORTFOLIO = "a[href='/portfolio']"
    MENU_GOALS = "a[href='/goals']"
    MENU_BUDGET = "a[href='/budget']"
    MENU_ANALYTICS = "a[href='/analytics']"
    MENU_PROFILE = "a[href='/profile']"
    MENU_RECOMMENDATIONS = "a[href='/recommendations']"
    MENU_FACT_SHEET = "a[href='/fact-sheet-analysis']"
    MENU_RISK = "a[href='/risk-profiling']"
    MENU_SIP = "a[href='/sip']"
    MENU_SWP = "a[href='/swp']"
    MENU_INFLATION = "a[href='/inflation']"
    MENU_NOTIFICATIONS = "a[href='/notifications']"
    MENU_DB_ADMIN = "a[href='/database-admin']"

    async def is_loaded(self):
        """Check if dashboard is loaded."""
        return "/dashboard" in self.page.url

    async def navigate_to_mutual_funds(self):
        await self.click(self.MENU_MUTUAL_FUNDS)
    
    async def navigate_to_portfolio(self):
        await self.click(self.MENU_PORTFOLIO)

    async def navigate_to_goals(self):
        await self.click(self.MENU_GOALS)
    
    async def navigate_to_budget(self):
        await self.click(self.MENU_BUDGET)

    async def navigate_to_analytics(self):
        await self.click(self.MENU_ANALYTICS)

    async def navigate_to_recommendations(self):
        await self.click(self.MENU_RECOMMENDATIONS)

    async def navigate_to_fact_sheet(self):
        await self.click(self.MENU_FACT_SHEET)

    async def navigate_to_risk(self):
        await self.click(self.MENU_RISK)

    async def navigate_to_sip(self):
        await self.click(self.MENU_SIP)

    async def navigate_to_swp(self):
        await self.click(self.MENU_SWP)

    async def navigate_to_inflation(self):
        await self.click(self.MENU_INFLATION)

    async def navigate_to_notifications(self):
        await self.click(self.MENU_NOTIFICATIONS)

    async def navigate_to_db_admin(self):
        await self.click(self.MENU_DB_ADMIN)
    
    async def get_total_portfolio_value(self) -> str:
        """Get the total portfolio value displayed on dashboard."""
        # Assuming there is a card showing total portfolio value
        # We need a selector for it. Based on typical dash:
        # It might be in a card with "Total Value" or similar.
        # Let's try to find it by text or class.
        # Assuming the first card-body h3 or similar holds the value.
        # For now, let's look for a generic currency formatted element or specific ID if known.
        # Since we don't know exact selector, let's use a text locator that finds "Total Portfolio Value" and gets sibling/child.
        # But for robustness, let's assume there's a specific widget.
        # Let's try to match text containing "$" or "₹"
        return await self.get_text("app-dashboard .card-title:has-text('Total Value') + .card-text") # Guessing structure

    async def get_recent_transactions(self) -> list[str]:
         """Get text of recent transactions/investments if shown."""
         return await self.page.locator(".list-group-item").all_text_contents()
