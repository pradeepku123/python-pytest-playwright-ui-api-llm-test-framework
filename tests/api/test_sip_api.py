
import pytest

@pytest.mark.asyncio
async def test_sip_crud(new_user_client):
    """Test full CRUD lifecycle for SIP Estimation."""
    api = new_user_client
    
    # 1. Create SIP Estimation
    create_data = {
        "name": "Dream Car",
        "sip_type": "Monthly",
        "amount": 5000.0,
        "return_rate": 12.0,
        "time_period": 5,
        "total_invested": 300000.0, # 5000 * 12 * 5
        "estimated_returns": 100000.0, # Dummy
        "total_value": 400000.0 # Dummy
    }
    
    resp = await api.post("/api/v1/sip/save", json=create_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    created_sip = resp.json().get("data")
    sip_id = created_sip['id']
    
    # 2. Read SIPs
    resp = await api.get("/api/v1/sip/list")
    assert resp.status_code == 200
    sips = resp.json().get("data", [])
    
    found = next((s for s in sips if s['id'] == sip_id), None)
    assert found is not None
    assert found['name'] == "Dream Car"
    
    # 3. Delete SIP
    resp = await api.delete(f"/api/v1/sip/{sip_id}")
    assert resp.status_code == 200
    
    # Verify Deletion
    resp = await api.get("/api/v1/sip/list")
    sips = resp.json().get("data", [])
    found = next((s for s in sips if s['id'] == sip_id), None)
    assert found is None
