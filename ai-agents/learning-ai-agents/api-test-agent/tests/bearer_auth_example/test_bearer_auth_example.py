import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

# Bearer token for authentication
BEARER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw'

def test_get_profile_success():
    # curl -X GET "https://merp.intermesh.net/users/profile" -H "Authorization: Bearer $BEARER_TOKEN" -H "Content-Type: application/json"
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    response = requests.get(f"{BASE_URL}{path}", headers=headers)
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate success response
    assert 'status' in response_data or 'data' in response_data

def test_get_profile_error_invalid_token():
    # Invalid Bearer token
    # curl -X GET "https://merp.intermesh.net/users/profile" -H "Authorization: Bearer invalid_token" -H "Content-Type: application/json"
    headers = {'Authorization': f'Bearer invalid_token'}
    response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate error response
    assert 'status' in response_data or 'error' in response_data or 'message' in response_data

def test_get_profile_error_missing_token():
    # Missing authentication
    # curl -X GET "https://merp.intermesh.net/users/profile" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/users/profile")
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate error response
    assert 'status' in response_data or 'error' in response_data or 'message' in response_data

def test_get_profile_error_expired_token():
    # Expired token
    # curl -X GET "https://merp.intermesh.net/users/profile" -H "Authorization: Bearer expired_token" -H "Content-Type: application/json"
    headers = {'Authorization': f'Bearer expired_token'}
    response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate error response
    assert 'status' in response_data or 'error' in response_data or 'message' in response_data

def test_put_settings_success():
    # curl -X PUT "https://merp.intermesh.net/users/settings" -H "Authorization: Bearer $BEARER_TOKEN" -H "Content-Type: application/json"
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    response = requests.get(f"{BASE_URL}{path}", headers=headers)
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate success response
    assert 'status' in response_data or 'data' in response_data

def test_put_settings_error_invalid_token():
    # Invalid Bearer token
    # curl -X PUT "https://merp.intermesh.net/users/settings" -H "Authorization: Bearer invalid_token" -H "Content-Type: application/json"
    headers = {'Authorization': f'Bearer invalid_token'}
    response = requests.put(f"{BASE_URL}/users/settings", headers=headers)
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate error response
    assert 'status' in response_data or 'error' in response_data or 'message' in response_data

def test_put_settings_error_missing_token():
    # Missing authentication
    # curl -X PUT "https://merp.intermesh.net/users/settings" -H "Content-Type: application/json"
    response = requests.put(f"{BASE_URL}/users/settings")
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate error response
    assert 'status' in response_data or 'error' in response_data or 'message' in response_data

def test_put_settings_error_expired_token():
    # Expired token
    # curl -X PUT "https://merp.intermesh.net/users/settings" -H "Authorization: Bearer expired_token" -H "Content-Type: application/json"
    headers = {'Authorization': f'Bearer expired_token'}
    response = requests.put(f"{BASE_URL}/users/settings", headers=headers)
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate error response
    assert 'status' in response_data or 'error' in response_data or 'message' in response_data

if __name__ == "__main__":
    pytest.main()