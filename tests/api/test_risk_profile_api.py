
import pytest

@pytest.mark.asyncio
async def test_risk_profile_lifecycle(new_user_client):
    """Test Risk Profile lifecycle."""
    api = new_user_client
    
    # 1. Get initial profile (should be empty or default)
    resp = await api.get("/api/v1/risk-profile")
    assert resp.status_code == 200
    # Data might be null if not created
    # Check creation
    
    # 2. Create/Update Risk Profile
    # Answers usually follow a structure like {"q1": "a1", ...}
    answers = {
        "q1": "High",
        "q2": "Long Term",
        "q3": "Growth"
    }
    create_data = {
        "answers": answers
    }
    
    resp = await api.post("/api/v1/risk-profile", json=create_data)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    data = resp.json().get("data")
    assert data['risk_score'] is not None 
    assert data['risk_category'] is not None
    
    # 3. Verify Read
    resp = await api.get("/api/v1/risk-profile")
    assert resp.status_code == 200
    data = resp.json().get("data")
    assert data['answers'] == answers
