from fastapi.testclient import TestClient
from tests.conftest import client, auth_headers

def test_create_chat_with_auth(client: TestClient, auth_headers, monkeypatch):
    async def mock_call_chat_completion(messages):
        return "This is a monkey assistant"

    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    first_message = {
        "content": "How do I deploy vLLM on HPC?"
    }

    res = client.post("/api/v1/chats", json=first_message, headers=auth_headers)
    assert res.status_code == 201

    chat = res.json()
    assert isinstance(chat["id"], int)
    assert chat["id"] > 0
    assert chat["title"] == "This is a monkey assistant"

def test_create_message_in_existing_chat(client: TestClient, auth_headers, monkeypatch):
    # ---- Mock LLM assistant responses ----
    async def mock_call_chat_completion(messages):
        # Simulate assistant replies
        return "This is a monkey assistant"

    # Apply monkeypatch
    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    # Create chat with first message
    first_message = {"content": "Hello LLM, how are you?"}
    res = client.post("/api/v1/chats", json=first_message, headers=auth_headers)
    assert res.status_code == 201

    chat = res.json()
    assert isinstance(chat["id"], int)
    chat_id = chat["id"]

    # Send follow-up user message
    second_message = {"content": "Can you tell me more?"}
    res = client.post(f"/api/v1/chats/{chat_id}/messages", json=second_message, headers=auth_headers)
    assert res.status_code == 201

    # Validate assistant response
    reply = res.json()
    assert reply["role"] == "assistant"
    assert reply["content"] == "This is a monkey assistant"

def test_get_all_message_in_existing_chat(client: TestClient, auth_headers, monkeypatch):
    # ---- Mock LLM assistant responses ----
    async def mock_call_chat_completion(messages):
        return "This is a monkey assistant"

    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    # Test messages
    messages = [
        {"content": "Hello LLM, how are you? 1"},
        {"content": "Hello LLM, how are you? 2"},
        {"content": "Hello LLM, how are you? 3"},
        {"content": "Hello LLM, how are you? 4"},
        {"content": "Hello LLM, how are you? 5"},
    ]

    # 1. Create chat with the first message
    res = client.post("/api/v1/chats", json=messages[0], headers=auth_headers)
    assert res.status_code == 201

    chat = res.json()
    chat_id = chat["id"]
    assert isinstance(chat_id, int)

    # 2. Send remaining user messages
    for msg in messages[1:]:
        res = client.post(f"/api/v1/chats/{chat_id}/messages", json=msg, headers=auth_headers)
        assert res.status_code == 201

    # 3. Fetch all messages for this chat
    res = client.get(f"/api/v1/chats/{chat_id}/messages", headers=auth_headers)
    assert res.status_code == 200

    all_messages = res.json()
    assert isinstance(all_messages, list)

    # There should be 10 messages: 5 user + 5 assistant
    assert len(all_messages) == 10

    # Optional: check ordering (assuming ascending by created_at)
    for i, msg in enumerate(all_messages):
        assert "id" in msg
        assert "role" in msg
        assert "content" in msg

    # Optional: verify alternating roles: user/assistant/user/assistant...
    for i in range(10):
        expected_role = "user" if i % 2 == 0 else "assistant"
        assert all_messages[i]["role"] == expected_role

    # Optional: verify assistant content mocked correctly
    assistant_msgs = [m for m in all_messages if m["role"] == "assistant"]
    for m in assistant_msgs:
        assert m["content"] == "This is a monkey assistant"

def test_get_chats_with_user(client: TestClient, auth_headers, monkeypatch):
    # Mock LLM title generator so POST /chats works
    async def mock_call_chat_completion(messages):
        return "mocked title"

    monkeypatch.setattr(
        "services.llm_service.llm_service.call_chat_completion",
        mock_call_chat_completion
    )

    # Create multiple chats for the authenticated user
    for i in range(3):
        res = client.post(
            "/api/v1/chats",
            json={"content": f"message {i}"},
            headers=auth_headers
        )
        assert res.status_code == 201

    # Now retrieve all chats for the user
    res = client.get("/api/v1/chats", headers=auth_headers)
    assert res.status_code == 200

    chats = res.json()
    assert isinstance(chats, list)
    assert len(chats) == 3

    # Validate chat fields
    for chat in chats:
        assert "id" in chat
        assert "title" in chat
        assert isinstance(chat["id"], int)
        assert isinstance(chat["title"], str)

