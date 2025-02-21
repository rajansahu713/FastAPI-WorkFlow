import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_create_item(client, sample_item):
    response = client.post("/items/", json=sample_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert data["description"] == sample_item["description"]
    assert "id" in data

def test_read_items(client, sample_item):
    # Create a test item first
    client.post("/items/", json=sample_item)
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == sample_item["name"]

def test_read_item(client, sample_item):
    # Create a test item first
    create_response = client.post("/items/", json=sample_item)
    created_item = create_response.json()
    
    response = client.get(f"/items/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert data["description"] == sample_item["description"]

def test_read_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item(client, sample_item):
    # Create a test item first
    create_response = client.post("/items/", json=sample_item)
    created_item = create_response.json()
    
    updated_item = {
        "name": "Updated Test Item",
        "description": "This is an updated test item"
    }
    
    response = client.put(f"/items/{created_item['id']}", json=updated_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_item["name"]
    assert data["description"] == updated_item["description"]

def test_update_item_not_found(client, sample_item):
    response = client.put("/items/999", json=sample_item)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item(client, sample_item):
    # Create a test item first
    create_response = client.post("/items/", json=sample_item)
    created_item = create_response.json()
    
    # Delete the item
    response = client.delete(f"/items/{created_item['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"
    
    # Verify item is deleted
    get_response = client.get(f"/items/{created_item['id']}")
    assert get_response.status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_read_items_pagination(client, sample_item):
    # Create multiple items
    for i in range(5):
        modified_item = sample_item.copy()
        modified_item["name"] = f"Test Item {i}"
        client.post("/items/", json=modified_item)
    
    # Test pagination
    response = client.get("/items/?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2