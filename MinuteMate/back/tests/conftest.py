import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from typing import Generator

from app.main import app  # Adjust import path as needed

@pytest.fixture
def test_client() -> Generator:
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_weaviate_client():
    with patch('weaviate.connect_to_weaviate_cloud') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client

@pytest.fixture
def mock_openai_client():
    with patch('openai.OpenAI') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client