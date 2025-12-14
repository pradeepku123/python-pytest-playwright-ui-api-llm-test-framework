import pytest
import allure
import uuid
from framework.pages.login_page import LoginPage
from framework.pages.goals_page import GoalsPage

@allure.feature("Goals Feature")
class TestGoalsFeature:
    
    @allure.story("Create Goal")
    @pytest.mark.asyncio
    async def test_create_goal(self, page):
        """
        Test flow:
        1. Login as admin/superadmin
        2. Navigate to Goals
        3. Create a new Goal
        4. Verify it appears in the list
        """
        login_page = LoginPage(page)
        goals_page = GoalsPage(page)
        
        # 1. Login
        await login_page.navigate()
        await login_page.login("admin", "superadmin")
        await page.wait_for_url("**/dashboard")
        
        # 2. Navigate to Goals
        await goals_page.navigate()
        await page.wait_for_url("**/goals")
        
        # 3. Create Goal
        unique_id = str(uuid.uuid4())[:8]
        goal_name = f"Test Goal {unique_id}"
        target_amount = "100000"
        target_date = "2030-12-31" # Format YYYY-MM-DD
        
        await goals_page.create_goal(goal_name, target_amount, target_date)
        
        # 4. Verify
        # Wait for list to update
        await page.wait_for_timeout(1000)
        
        goal_names_content = await goals_page.get_goal_names()
        found = any(goal_name in content for content in goal_names_content)
        assert found, f"Goal {goal_name} not found in goals list content: {goal_names_content}"
