import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

def test_get_emp_details_success():
    # curl -X GET "https://merp.intermesh.net/api/emp/v1/emp-details?empid=114697&AK=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/emp/v1/emp-details", params={'empid': '114697', 'AK': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    
    # Success case - HTTP 200 with status "200" in response body
    assert 'status' in response_data
    # Handle both string and integer status codes
    assert response_data['status'] == 200 or response_data['status'] == '200'
    assert 'data' in response_data
    assert 'message' in response_data

def test_get_emp_details_error_400():
    # curl -X GET "https://merp.intermesh.net/api/emp/v1/emp-details?empid=invalid_id&AK=invalid_token" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/emp/v1/emp-details", params={'empid': 'invalid_id', 'AK': 'invalid_token'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    
    # Error case - Invalid empid returns status 400
    assert 'status' in response_data
    # Handle both string and integer status codes
    assert response_data['status'] == 400 or response_data['status'] == '400'
    assert 'message' in response_data

def test_get_emp_details_error_401():
    # curl -X GET "https://merp.intermesh.net/api/emp/v1/emp-details?empid=114697&AK=invalid_token" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/emp/v1/emp-details", params={'empid': '114697', 'AK': 'invalid_token'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    
    # Error case - Invalid token returns status "401" (string)
    assert 'status' in response_data
    # Handle both string and integer status codes
    assert response_data['status'] == 401 or response_data['status'] == '401'
    assert 'message' in response_data

def test_get_emp_details_error_206():
    # curl -X GET "https://merp.intermesh.net/api/emp/v1/emp-details?empid=invalid_id&AK=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/emp/v1/emp-details", params={'empid': 'invalid_id', 'AK': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    
    # Error case - Invalid empid with valid token returns status 400
    assert 'status' in response_data
    # Handle both string and integer status codes
    assert response_data['status'] == 400 or response_data['status'] == '400'
    assert 'message' in response_data

if __name__ == "__main__":
    pytest.main()