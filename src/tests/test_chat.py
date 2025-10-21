from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_chat_endpoint():
    response = client.post("/api/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_endpoint_empty_message():
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Message cannot be empty."}