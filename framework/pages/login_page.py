"""Login page object."""
from framework.pages.base_page import BasePage

class LoginPage(BasePage):
    """Login page object."""
    
    URL = "http://localhost:4200/login"
    
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button:has-text('Sign In')"
    SIGN_UP_LINK = "a[href='/register']"
    
    async def navigate(self):
        """Navigate to login page."""
        await self.navigate_to(self.URL)
        
    async def login(self, username, password):
        """Perform login."""
        await self.fill(self.USERNAME_INPUT, username)
        await self.fill(self.PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)
