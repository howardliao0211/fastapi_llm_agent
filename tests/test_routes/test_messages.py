from fastapi.testclient import TestClient
from database.models.message import Role

def test_create_message_with_user_and_chat(client: TestClient, monkeypatch):
    # ---- Monkeypatch async LLM ----
    async def mock_call_chat_completion(messages):
        return "mocked assistant reply"

    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    # ---- Create User ----
    data = {
        "full_name": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing"
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # ---- Create Chat ----
    chat = {"user_id": user_id}
    response = client.post("/api/v1/chats", json=chat)
    assert response.status_code == 201
    chat_id = response.json()["id"]

    # ---- Send Message ----
    message = {
        "role": Role.USER,
        "content": "test is a test message"
    }
    response = client.post(f"/api/v1/chats/{chat_id}/messages", json=message)
    assert response.status_code == 201

    body = response.json()

    # ---- Validate Output ----
    assert body["role"] == Role.ASSISTANT
    assert body["content"] == "mocked assistant reply"
