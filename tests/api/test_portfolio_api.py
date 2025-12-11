
import pytest
import uuid

@pytest.mark.asyncio
async def test_portfolio_crud(new_user_client):
    """Test full CRUD lifecycle for Portfolio."""
    api = new_user_client
    
    # 1. Create Investment
    fund_name = f"API Fund {str(uuid.uuid4())[:8]}"
    create_data = {
        "investment_type": "Stock", 
        "fund_name": fund_name,
        "invested_amount": 10000.0,
        "current_value": 12000.0
    }
    
    resp = await api.post("/api/v1/portfolio/funds", json=create_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    # 2. Read Investments
    resp = await api.get("/api/v1/portfolio/funds")
    assert resp.status_code == 200
    funds = resp.json().get("data", [])
    
    target_fund = None
    for f in funds:
        if f.get("fund_name") == fund_name:
            target_fund = f
            break
            
    assert target_fund is not None, f"Created fund {fund_name} not found."
    fund_id = target_fund.get("id") # Assuming ID is in the response object
    
    # Note: If ID is not in the list response, we might have a problem for Update/Delete.
    # Looking at the openapi spec, the schema for InvestmentCreate doesn't include ID, 
    # but the response usually includes the created object or at least ID.
    # If not, let's assume the list response has it.
    
    if not fund_id:
        # Fallback: maybe DB schema has it as 'id' or 'fund_id' or 'investment_id'
        # Let's inspect the target_fund dict in a debug print if needed, but for now generic check
        fund_id = target_fund.get("investment_id") or target_fund.get("id")

    assert fund_id is not None, "Could not extract Fund ID for update/delete."

    # 3. Update Investment
    update_data = {
        "investment_type": "Stock",
        "fund_name": f"{fund_name} Updated",
        "invested_amount": 15000.0,
        "current_value": 16000.0
    }
    resp = await api.put(f"/api/v1/portfolio/funds/{fund_id}", json=update_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    # Verify Update
    resp = await api.get("/api/v1/portfolio/funds")
    funds = resp.json().get("data", [])
    updated_found = False
    for f in funds:
        if f.get("fund_name") == f"{fund_name} Updated" and f.get("invested_amount") == 15000.0:
            updated_found = True
            break
    assert updated_found, "Fund update not reflected in list."

    # 4. Summary & Breakdown
    resp = await api.get("/api/v1/portfolio/summary")
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    resp = await api.get("/api/v1/portfolio/asset-breakdown")
    assert resp.status_code == 200
    assert resp.json()["success"] is True

    # 5. Delete Investment
    resp = await api.delete(f"/api/v1/portfolio/funds/{fund_id}")
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    
    # Verify Deletion
    resp = await api.get("/api/v1/portfolio/funds")
    funds = resp.json().get("data", [])
    deleted_found = False
    for f in funds:
        if f.get("id") == fund_id:
            deleted_found = True
            break
    assert not deleted_found, "Fund still exists after deletion."
