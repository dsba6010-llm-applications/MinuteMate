import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust import path

def test_process_prompt_valid_request(test_client):
    response = test_client.post(
        "/process-prompt",
        json={"user_prompt_text": "Test prompt"}
    )
    assert response.status_code == 200
    assert "generated_response" in response.json()

def test_process_prompt_invalid_request(test_client):
    response = test_client.post(
        "/process-prompt",
        json={"user_prompt_text": ""}
    )
    assert response.status_code == 422

def test_process_prompt_long_text(test_client):
    response = test_client.post(
        "/process-prompt",
        json={"user_prompt_text": "a" * 1001}
    )
    assert response.status_code == 422