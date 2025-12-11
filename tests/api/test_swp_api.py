
import pytest

@pytest.mark.asyncio
async def test_swp_crud(new_user_client):
    """Test full CRUD lifecycle for SWP Estimation."""
    api = new_user_client
    
    # 1. Create SWP Estimation
    create_data = {
        "name": "Retirement Plan",
        "total_investment": 5000000.0,
        "withdrawal_per_month": 25000.0,
        "return_rate": 8.5,
        "time_period": 20,
        "total_withdrawn": 6000000.0, # Dummy
        "final_value": 1000000.0 # Dummy
    }
    
    resp = await api.post("/api/v1/swp/save", json=create_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    created_swp = resp.json().get("data")
    swp_id = created_swp['id']
    
    # 2. Read SWPs
    resp = await api.get("/api/v1/swp/list")
    assert resp.status_code == 200
    swps = resp.json().get("data", [])
    
    found = next((s for s in swps if s['id'] == swp_id), None)
    assert found is not None
    assert found['name'] == "Retirement Plan"
    
    # 3. Delete SWP
    resp = await api.delete(f"/api/v1/swp/{swp_id}")
    assert resp.status_code == 200
    
    # Verify Deletion
    resp = await api.get("/api/v1/swp/list")
    swps = resp.json().get("data", [])
    found = next((s for s in swps if s['id'] == swp_id), None)
    assert found is None
