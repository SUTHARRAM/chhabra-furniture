import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

def test_get__success():
    # curl -X GET "https://merp.intermesh.net/index.php/Employee/Employeelist/?empid=114697&AK=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw&keyword=test" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/index.php/Employee/Employeelist/", params={'empid': '114697', 'AK': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMTQ2OTciLCJleHAiOjE3NTg1MjgwNTAsImlhdCI6MTc1ODQ0MTY1MCwiaXNzIjoiRU1QTE9ZRUUifQ.GdIm-wnuSsLNEccHQ13qxvJKPw8CS1fmmLj7RM9UFjw', 'keyword': 'test'})
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

def test_get__error_500():
    # curl -X GET "https://merp.intermesh.net/index.php/Employee/Employeelist/?empid=invalid_id&AK=invalid_token&keyword=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/index.php/Employee/Employeelist/", params={'empid': 'invalid_id', 'AK': 'invalid_token', 'keyword': 'invalid_value'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 500 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 500 or item['status'] == '500'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 500 or response_data['status'] == '500'
