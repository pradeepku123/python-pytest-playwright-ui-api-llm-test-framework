"""Portfolio page object."""
from framework.pages.base_page import BasePage

class PortfolioPage(BasePage):
    """Portfolio page object."""
    
    URL = "http://localhost:4200/portfolio"
    
    # Locators
    # Using a more specific selector if possible, or forcing click
    ADD_INVESTMENT_BUTTON = "button.btn-primary:has-text('Add Investment')"
    
    # Modal Locators
    MODAL_CONTENT = "#addInvestmentModal .modal-content"
    MODAL_TYPE_SELECT = "#investmentType"
    MODAL_NAME_INPUT = "#investmentName"
    MODAL_AMOUNT_INPUT = "#investedAmount"
    MODAL_CURRENT_VALUE_INPUT = "#currentValue"
    MODAL_ADD_BUTTON = ".modal-footer button.btn-primary"
    
    # Table Locators
    PORTFOLIO_TABLE = "table"
    
    async def navigate(self):
        """Navigate to portfolio page."""
        await self.navigate_to(self.URL)
        
    async def add_investment(self, type: str, name: str, amount: str):
        """Add a new investment."""
        # Wait for button to be available first!
        await self.page.wait_for_selector("button:has-text('Add Investment')")
        
        # Click Add Investment using JS as it is most robust for this button
        await self.page.evaluate("""() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const target = buttons.find(b => b.textContent.includes('Add Investment'));
            if (target) target.click();
        }""")

        # Wait for modal
        await self.wait_for_element(self.MODAL_NAME_INPUT)
        
        await self.page.select_option(self.MODAL_TYPE_SELECT, label=type)
        await self.fill(self.MODAL_NAME_INPUT, name)
        await self.fill(self.MODAL_AMOUNT_INPUT, str(amount))
        # Fill current value same as amount for simplicity
        await self.fill(self.MODAL_CURRENT_VALUE_INPUT, str(amount))
        
        await self.click(self.MODAL_ADD_BUTTON)
        # Wait for modal to close or table to update
        await self.page.wait_for_selector(self.PORTFOLIO_TABLE)

    async def get_investment_names(self) -> list[str]:
        """Get names of all investments in the table."""
        # Assuming name is in the first column or similar. 
        # We might need to inspect the table structure, but usually text content of rows helps.
        rows = await self.page.locator("table tbody tr").all()
        names = []
        for row in rows:
            # Name is in the second column (index 1), often with status below it
            # We use inner_text to preserve newlines and split
            cell_text = await row.locator("td").nth(1).inner_text()
            # unique name is the first line
            name = cell_text.split('\n')[0].strip()
            names.append(name)
        return names
