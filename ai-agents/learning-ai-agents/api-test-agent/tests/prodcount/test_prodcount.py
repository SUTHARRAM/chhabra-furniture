import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

def test_get_productDetailsCounts_success():
    # curl -X GET "https://merp.intermesh.net/api/production/v1/productDetailsCounts?empid=114697&glid=valid_value&modid=valid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/production/v1/productDetailsCounts", params={'empid': '114697', 'glid': 'valid_value', 'modid': 'valid_value'})
    assert response.status_code == 200
    response_data = response.json()
    # Validate response for status 200 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        assert item['status'] == '200'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        assert response_data['status'] == '200'

def test_get_productDetailsCounts_error_400():
    # curl -X GET "https://merp.intermesh.net/api/production/v1/productDetailsCounts?empid=invalid_id&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/production/v1/productDetailsCounts", params={'empid': 'invalid_id', 'glid': 'invalid_value', 'modid': 'invalid_value'})
    assert response.status_code == 200
    response_data = response.json()
    # Validate response for status 400 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        assert item['status'] == '400'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        assert response_data['status'] == '400'

def test_get_productDetailsCounts_error_401():
    # curl -X GET "https://merp.intermesh.net/api/production/v1/productDetailsCounts?empid=invalid_id&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/production/v1/productDetailsCounts", params={'empid': 'invalid_id', 'glid': 'invalid_value', 'modid': 'invalid_value'})
    assert response.status_code == 200
    response_data = response.json()
    # Validate response for status 401 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        assert item['status'] == '401'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        assert response_data['status'] == '401'

def test_get_productDetailsCounts_error_422():
    # curl -X GET "https://merp.intermesh.net/api/production/v1/productDetailsCounts?empid=invalid_id&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/production/v1/productDetailsCounts", params={'empid': 'invalid_id', 'glid': 'invalid_value', 'modid': 'invalid_value'})
    assert response.status_code == 200
    response_data = response.json()
    # Validate response for status 422 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        assert item['status'] == '422'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        assert response_data['status'] == '422'

def test_get_productDetailsCounts_error_500():
    # curl -X GET "https://merp.intermesh.net/api/production/v1/productDetailsCounts?empid=invalid_id&glid=invalid_value&modid=invalid_value" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/production/v1/productDetailsCounts", params={'empid': 'invalid_id', 'glid': 'invalid_value', 'modid': 'invalid_value'})
    assert response.status_code == 200
    response_data = response.json()
    # Validate response for status 500 in response body
    # Check status in response body
    if isinstance(response_data, list) and response_data:
        item = response_data[0]
        assert 'status' in item
        assert item['status'] == '500'
        assert 'data' in item
    else:
        # Handle direct response
        assert 'status' in response_data
        assert response_data['status'] == '500'
