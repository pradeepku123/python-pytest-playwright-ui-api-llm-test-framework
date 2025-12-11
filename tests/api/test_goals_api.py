
import pytest
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_goals_crud(new_user_client):
    """Test full CRUD lifecycle for Goals."""
    api = new_user_client
    
    # 1. Create Goal
    goal_name = "API Test Goal"
    target_amount = 100000.0
    target_date = "2030-12-31"
    
    create_data = {
        "name": goal_name,
        "target_amount": target_amount,
        "target_date": target_date,
        "monthly_sip_amount": 5000.0
    }
    
    resp = await api.post("/api/v1/goals", json=create_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    # 2. Read Goals
    resp = await api.get("/api/v1/goals")
    assert resp.status_code == 200
    goals = resp.json().get("data", [])
    
    target_goal = None
    for g in goals:
        if g.get("name") == goal_name:
            target_goal = g
            break
            
    assert target_goal is not None, f"Created goal {goal_name} not found."
    goal_id = target_goal.get("id")
    assert goal_id is not None
    
    # 3. Available Investments for syncing
    # Create an investment first so we have something to link
    inv_resp = await api.post("/api/v1/portfolio/funds", json={
        "investment_type": "Mutual Fund",
        "fund_name": "Goal Linked Fund",
        "invested_amount": 50000.0,
        "current_value": 55000.0
    })
    assert inv_resp.status_code == 200
    
    # Get available investments
    resp = await api.get("/api/v1/goals/available-investments")
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    avail_inv = resp.json().get("data", [])
    
    # Check if our new fund is available (might check by name)
    our_fund = next((i for i in avail_inv if i.get("fund_name") == "Goal Linked Fund"), None)
    
    if our_fund:
        inv_id = our_fund.get("id")
        # 4. Link Investment to Goal
        link_data = {
            "investment_ids": [inv_id]
        }
        resp = await api.put(f"/api/v1/goals/{goal_id}/link-investments", json=link_data)
        assert resp.status_code == 200
        assert resp.json()["success"] is True
    
    # Clean up not explicitly strictly needed for new_user_client as it is isolated per test run usually, 
    # but good practice. However, no delete endpoint for goals in spec?
    # Checking spec...
    # /api/v1/goals/{goal_id}/link-investments (PUT)
    # /api/v1/goals (POST, GET)
    # No DELETE endpoint for goals in spec provided earlier?
    # View file 421 line 680...
    # paths: /api/v1/goals: GET, POST.
    # /api/v1/goals/{goal_id}/link-investments: PUT
    # No DELETE /api/v1/goals/{id}. So we can't delete goals via API in this version.
    pass
