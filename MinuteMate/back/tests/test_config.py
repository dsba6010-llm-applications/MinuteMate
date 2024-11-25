import pytest
import os
from unittest.mock import patch
from app.main import WeaviateConfig, PromptProcessor  # Adjust import path

def test_weaviate_config_initialization():
    test_url = "https://test-url"
    test_api_key = "test-key"
    
    with patch('weaviate.connect_to_weaviate_cloud') as mock_connect:
        WeaviateConfig.get_weaviate_client(test_url, test_api_key)
        mock_connect.assert_called_once()

def test_prompt_processor_env_vars():
    test_env_vars = {
        'OPENAI_API_KEY': 'test-openai-key',
        'WEAVIATE_URL': 'test-weaviate-url',
        'WEAVIATE_API_KEY': 'test-weaviate-key'
    }
    
    with patch.dict(os.environ, test_env_vars):
        processor = PromptProcessor()
        assert processor.OPENAI_API_KEY == 'test-openai-key'
        assert processor.WEAVIATE_URL == 'test-weaviate-url'
        assert processor.WEAVIATE_API_KEY == 'test-weaviate-key'

def test_prompt_processor_missing_env_vars():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            PromptProcessor()