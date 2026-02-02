from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    data = {
        "full_name": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing"
    }
    response = client.post("/api/v1/users", json=data)
    print(response)
    assert response.status_code == 201
    assert response.json()["full_name"] == data["full_name"]
    assert response.json()["email"] == data["email"]
    assert isinstance(response.json()["id"], int)
