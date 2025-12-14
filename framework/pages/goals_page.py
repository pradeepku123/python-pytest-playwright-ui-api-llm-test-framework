"""Goals page object."""
from framework.pages.base_page import BasePage

class GoalsPage(BasePage):
    """Goals page object."""
    
    URL = "http://localhost:4200/goals"
    
    # Locators
    # Assuming similar structure to Portfolio page
    ADD_GOAL_BUTTON = "button:has-text('New Goal')"
    
    # Modal
    MODAL_CONTENT = "app-goals .modal-content" # or just .modal-content
    GOAL_NAME_INPUT = "#name" # or formControlName="name"
    TARGET_AMOUNT_INPUT = "#target_amount"
    TARGET_DATE_INPUT = "#target_date"
    EXPECTED_RETURN_INPUT = "#expected_return"
    MONTHLY_SIP_INPUT = "#monthly_sip_amount"
    
    MODAL_SUBMIT_BUTTON = "button:has-text('Save Goal')"
    
    # List
    GOALS_LIST = ".goal-card" # assumption
    
    async def navigate(self):
        """Navigate to goals page."""
        await self.navigate_to(self.URL)
        
    async def create_goal(self, name: str, amount: str, date: str, expected_return: str = "10"):
        """Create a new financial goal."""
        await self.click(self.ADD_GOAL_BUTTON)
        
        await self.wait_for_element(self.GOAL_NAME_INPUT)
        
        await self.fill(self.GOAL_NAME_INPUT, name)
        await self.fill(self.TARGET_AMOUNT_INPUT, str(amount))
        await self.fill(self.TARGET_DATE_INPUT, date)
        await self.fill(self.EXPECTED_RETURN_INPUT, str(expected_return))
        
        await self.click(self.MODAL_SUBMIT_BUTTON)
        # Wait for modal to close
        await self.page.wait_for_function("document.querySelectorAll('.modal-backdrop').length === 0")

    async def get_goal_names(self) -> list[str]:
        """Get names of all goals."""
        await self.page.wait_for_selector(".card")
        # Get all h5 elements inside cards which contain the goal name
        elements = await self.page.locator(".card h5").all()
        names = []
        for el in elements:
            text = await el.text_content()
            names.append(text.strip())
        return names
