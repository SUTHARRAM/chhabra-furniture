import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

def test_get__success():
    # curl -X GET "https://merp.intermesh.net/index.php/Userlist/GlidDetails/?empid=114697&AK=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/index.php/Userlist/GlidDetails/", params={'empid': '114697', 'AK': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 200 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 200 or item['status'] == '200'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 200 or response_data['status'] == '200'

def test_get__error_204():
    # curl -X GET "https://merp.intermesh.net/index.php/Userlist/GlidDetails/?empid=invalid_id&AK=invalid_token" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/index.php/Userlist/GlidDetails/", params={'empid': 'invalid_id', 'AK': 'invalid_token'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 204 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 204 or item['status'] == '204'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 204 or response_data['status'] == '204'

def test_get__error_401():
    # curl -X GET "https://merp.intermesh.net/index.php/Userlist/GlidDetails/?empid=invalid_id&AK=invalid_token" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/index.php/Userlist/GlidDetails/", params={'empid': 'invalid_id', 'AK': 'invalid_token'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 401 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 401 or item['status'] == '401'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 401 or response_data['status'] == '401'

def test_get__error_402():
    # curl -X GET "https://merp.intermesh.net/index.php/Userlist/GlidDetails/?empid=invalid_id&AK=invalid_token" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/index.php/Userlist/GlidDetails/", params={'empid': 'invalid_id', 'AK': 'invalid_token'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 402 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 402 or item['status'] == '402'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 402 or response_data['status'] == '402'
