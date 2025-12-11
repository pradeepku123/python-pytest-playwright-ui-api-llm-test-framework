
import pytest
import uuid
from tests.api.api_client import APIClient

@pytest.fixture(scope="function")
async def api_client():
    """Returns an unauthenticated API client."""
    client = APIClient("http://localhost:8000")
    yield client
    await client.close()

@pytest.fixture(scope="function")
async def auth_client(api_client):
    """Returns an authenticated API client (Admin)."""
    await api_client.login("admin", "superadmin")
    return api_client

@pytest.fixture(scope="function")
async def new_user_client():
    """Creates a new user and returns a client authenticated as that user."""
    client = APIClient("http://localhost:8000")
    unique_id = str(uuid.uuid4())[:8]
    username = f"api_user_{unique_id}"
    email = f"api_{unique_id}@example.com"
    password = "Password123!"
    full_name = f"API Test User {unique_id}"
    
    # Register
    reg_data = {
        "user_id": username,
        "email": email,
        "password": password,
        "full_name": full_name
    }
    
    # We need to register first. 
    # Since client is not logged in, we can use it to register.
    # Note: openapi spec says POST /api/v1/auth/register
    resp = await client.post("/api/v1/auth/register", json=reg_data)
    assert resp.status_code == 200
    
    # Login
    # The application seems to use email for login (based on UI tests)
    # even though the field is named 'username' in OAuth2 form.
    await client.login(email, password)
    
    yield client
    await client.close()
