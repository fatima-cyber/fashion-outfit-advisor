import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_session_id():
    response = client.post("/create-session-id")
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_chat():
    session_id = 1  # Use a valid session ID
    response = client.post("/chat", json={"message": "Hello"}, params={"session_id": session_id})
    assert response.status_code == 200
    assert "response" in response.json()

def test_clear_chat():
    response = client.post("/clear-chat")
    assert response.status_code == 200
    assert response.content is None

def test_upload_image():
    with open("path/to/your/test/image.jpg", "rb") as image_file:
        response = client.post("/upload-image", files={"file": image_file})
    assert response.status_code == 200
    assert "image" in response.json()
