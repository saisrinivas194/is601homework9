import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import the FastAPI app from your app.main module

# Test: Login for Access Token
@pytest.mark.asyncio
async def test_login_for_access_token():
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/token", data=form_data)  # Ensure correct path '/token'
        
        # Print the response for debugging
        print(response.json())  # Check what the response body is
        # Ensure the token endpoint returns status 200
        assert response.status_code == 200
        assert "access_token" in response.json()

# Test: Create QR Code Unauthorized
@pytest.mark.asyncio
async def test_create_qr_code_unauthorized():
    qr_request = {
        "url": "https://example.com",
        "fill_color": "red",
        "back_color": "white",
        "size": 10,
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/qr-codes/", json=qr_request)  # Ensure correct path '/qr-codes/'
        
        # Print the response for debugging
        print(response.json())  # Check the error message returned
        assert response.status_code == 401  # Unauthorized if no token is provided

# Test: Create and Delete QR Code
@pytest.mark.asyncio
async def test_create_and_delete_qr_code():
    """
    Test the creation and deletion of a QR code using valid credentials.
    """
    form_data = {
        "username": "admin",  # Ensure this matches your app's expected credentials
        "password": "secret",  # Ensure this matches your app's expected credentials
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login and get the access token
        token_response = await ac.post("/token", data=form_data)
        
        # Print the response for debugging
        print(token_response.json())  # Check the token response
        
        assert token_response.status_code == 200, f"Unexpected status code: {token_response.status_code}"
        assert "access_token" in token_response.json(), "access_token not found in the response"
    
        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
    
        qr_request = {
            "url": "https://example.com",  # Ensure you're using 'url' here for the URL field
            "fill_color": "red",
            "back_color": "white",
            "size": 10,
        }
        
        # Create QR code
        create_response = await ac.post("/qr-codes/", json=qr_request, headers=headers)
        
        # Print the full response for debugging
        print(create_response.json())  # Check the error message returned

        assert create_response.status_code in [200, 201], f"Unexpected status code: {create_response.status_code}"

        # Extract QR code URL from the response to delete it
        qr_code_url = create_response.json().get("qr_code_url")
        assert qr_code_url, "QR code URL not found in the response"
        
        qr_filename = qr_code_url.split('/')[-1]  # Extract filename from the URL

        # Delete the created QR code
        delete_response = await ac.delete(f"/qr-codes/{qr_filename}", headers=headers)
        assert delete_response.status_code == 204, f"Unexpected status code: {delete_response.status_code}"  # Expect 204 No Content
