from fastapi.testclient import TestClient

def test_create_chat_with_auth(client: TestClient, monkeypatch):
    async def mock_call_chat_completion(messages):
        return "This is a monkey assistant"

    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    # 1. Register new user
    register_data = {
        "full_name": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing"
    }
    res = client.post("/api/v1/users", json=register_data)
    assert res.status_code == 201

    # 2. Login (OAuth2PasswordRequestForm → must use form data)
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }
    res = client.post("/api/v1/token", data=login_data)
    assert res.status_code == 200

    token = res.json()["access_token"]
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create chat with first message
    first_message = {
        "content": "How do I deploy vLLM on HPC?"
    }

    res = client.post("/api/v1/chats", json=first_message, headers=headers)
    assert res.status_code == 201

    chat = res.json()
    assert isinstance(chat["id"], int)
    assert chat["id"] > 0
    assert chat["title"] == "This is a monkey assistant"

def test_create_message_in_existing_chat(client: TestClient, monkeypatch):
    # ---- Mock LLM assistant responses ----
    async def mock_call_chat_completion(messages):
        # Simulate assistant replies
        return "This is a monkey assistant"

    # Apply monkeypatch
    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    # 1. Register the user
    register_data = {
        "full_name": "testuser",
        "email": "testuser@gmail.com",
        "password": "testing"
    }
    res = client.post("/api/v1/users", json=register_data)
    assert res.status_code == 201

    # 2. Login and obtain token
    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }
    res = client.post("/api/v1/token", data=login_data)
    assert res.status_code == 200

    token = res.json()["access_token"]
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create chat with first message
    first_message = {"content": "Hello LLM, how are you?"}
    res = client.post("/api/v1/chats", json=first_message, headers=headers)
    assert res.status_code == 201

    chat = res.json()
    assert isinstance(chat["id"], int)
    chat_id = chat["id"]

    # 4. Send follow-up user message
    second_message = {"content": "Can you tell me more?"}
    res = client.post(f"/api/v1/chats/{chat_id}/messages", json=second_message, headers=headers)
    assert res.status_code == 201

    # 5. Validate assistant response
    reply = res.json()
    assert reply["role"] == "assistant"
    assert reply["content"] == "This is a monkey assistant"
