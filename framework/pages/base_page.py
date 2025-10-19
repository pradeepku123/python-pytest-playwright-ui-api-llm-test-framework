"""Base page class for all page objects."""


class BasePage:
    """Base page class."""
    
    def __init__(self, page):
        """Initialize base page."""
        self.page = page
    
    async def navigate_to(self, url):
        """Navigate to URL."""
        await self.page.goto(url)
    
    async def get_title(self):
        """Get page title."""
        return await self.page.title()