import requests
import pytest

BASE_URL = "https://merp.intermesh.net"

def test_get_all_orders():
    # curl -X GET "https://merp.intermesh.net/api/v1/orders?limit=10&offset=0" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/v1/orders", params={"limit": 10, "offset": 0})
    assert response.status_code == 200

def test_create_order():
    # curl -X POST "https://merp.intermesh.net/api/v1/orders" -H "Content-Type: application/json" -d '{"customerId": "123", "items": [{"productId": "456", "quantity": 2, "price": 19.99}]}'
    data = {
        "customerId": "123",
        "items": [{"productId": "456", "quantity": 2, "price": 19.99}]
    }
    response = requests.post(f"{BASE_URL}/api/v1/orders", json=data)
    assert response.status_code == 201

def test_get_order_by_id():
    # curl -X GET "https://merp.intermesh.net/api/v1/orders/1" -H "Content-Type: application/json"
    response = requests.get(f"{BASE_URL}/api/v1/orders/1")
    assert response.status_code == 200

def test_update_order():
    # curl -X PUT "https://merp.intermesh.net/api/v1/orders/1" -H "Content-Type: application/json" -d '{"status": "shipped"}'
    data = {
        "status": "shipped"
    }
    response = requests.put(f"{BASE_URL}/api/v1/orders/1", json=data)
    assert response.status_code == 200

def test_delete_order():
    # curl -X DELETE "https://merp.intermesh.net/api/v1/orders/1" -H "Content-Type: application/json"
    response = requests.delete(f"{BASE_URL}/api/v1/orders/1")
    assert response.status_code == 204

if __name__ == "__main__":
    pytest.main()