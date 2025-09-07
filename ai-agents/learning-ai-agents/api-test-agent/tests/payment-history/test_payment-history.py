import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

def test_get_payment_history_success():
    # curl -X GET "https://merp.intermesh.net/api/csd/v1/payment-history?empid=114697&screen_name=valid_value&glid=valid_value&modid=valid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/csd/v1/payment-history", params={'empid': '114697', 'screen_name': 'valid_value', 'glid': 'valid_value', 'modid': 'valid_value'})
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

def test_get_payment_history_error_400():
    # curl -X GET "https://merp.intermesh.net/api/csd/v1/payment-history?empid=invalid_id&screen_name=invalid_value&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/csd/v1/payment-history", params={'empid': 'invalid_id', 'screen_name': 'invalid_value', 'glid': 'invalid_value', 'modid': 'invalid_value'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 400 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 400 or item['status'] == '400'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 400 or response_data['status'] == '400'

def test_get_payment_history_error_401():
    # curl -X GET "https://merp.intermesh.net/api/csd/v1/payment-history?empid=invalid_id&screen_name=invalid_value&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/csd/v1/payment-history", params={'empid': 'invalid_id', 'screen_name': 'invalid_value', 'glid': 'invalid_value', 'modid': 'invalid_value'})
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

def test_get_payment_history_error_422():
    # curl -X GET "https://merp.intermesh.net/api/csd/v1/payment-history?empid=invalid_id&screen_name=invalid_value&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/csd/v1/payment-history", params={'empid': 'invalid_id', 'screen_name': 'invalid_value', 'glid': 'invalid_value', 'modid': 'invalid_value'})
    # Skip HTTP status check - focus on response body status
    response_data = response.json()
    # Validate response for status 422 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        # Handle both string and integer status codes
        assert item['status'] == 422 or item['status'] == '422'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        # Handle both string and integer status codes
        assert response_data['status'] == 422 or response_data['status'] == '422'

def test_get_payment_history_error_500():
    # curl -X GET "https://merp.intermesh.net/api/csd/v1/payment-history?empid=invalid_id&screen_name=invalid_value&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/csd/v1/payment-history", params={'empid': 'invalid_id', 'screen_name': 'invalid_value', 'glid': 'invalid_value', 'modid': 'invalid_value'})
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
