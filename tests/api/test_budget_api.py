
import pytest

@pytest.mark.asyncio
async def test_budget_crud(new_user_client):
    """Test full CRUD lifecycle for Budget."""
    api = new_user_client
    
    # 1. Create Budget Plan
    plan_name = "Monthly Plan"
    income = 100000.0
    items = [
        {"category_name": "Rent", "amount": 20000.0},
        {"category_name": "Food", "amount": 10000.0}
    ]
    
    create_data = {
        "name": plan_name,
        "monthly_income": income,
        "items": items
    }
    
    resp = await api.post("/api/v1/budget/save", json=create_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    # The response data should have the created object
    created_budget = resp.json().get("data")
    assert created_budget['name'] == plan_name
    budget_id = created_budget['id']
    
    # 2. Read Budgets
    resp = await api.get("/api/v1/budget/list")
    assert resp.status_code == 200
    budgets = resp.json().get("data", [])
    
    # Verify our budget is in the list
    found = next((b for b in budgets if b['id'] == budget_id), None)
    assert found is not None
    assert found['monthly_income'] == income
    
    # 3. Update Budget
    # Endpoint: PUT /api/v1/budget/{id}
    update_data = {
        "name": "Updated Plan",
        "monthly_income": 120000.0,
        "items": [
             {"category_name": "Rent", "amount": 22000.0}, # increased
             {"category_name": "Food", "amount": 12000.0}
        ]
    }
    resp = await api.put(f"/api/v1/budget/{budget_id}", json=update_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    # Verify Update
    resp = await api.get("/api/v1/budget/list")
    budgets = resp.json().get("data", [])
    updated = next((b for b in budgets if b['id'] == budget_id), None)
    assert updated['name'] == "Updated Plan"
    assert updated['monthly_income'] == 120000.0
    
    # 4. Delete Budget
    resp = await api.delete(f"/api/v1/budget/{budget_id}")
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    # Verify Deletion
    resp = await api.get("/api/v1/budget/list")
    budgets = resp.json().get("data", [])
    deleted = next((b for b in budgets if b['id'] == budget_id), None)
    assert deleted is None
