import pytest
from app.main import PromptProcessor, PromptRequest  # Adjust import path

def test_extract_keywords(mock_weaviate_client):
    processor = PromptProcessor()
    text = "This is a test meeting about project planning and team coordination"
    keywords = processor.extract_keywords(text)
    assert isinstance(keywords, list)
    assert len(keywords) <= 3

def test_search_weaviate(mock_weaviate_client):
    processor = PromptProcessor()
    
    # Mock the collection query response
    mock_result = Mock()
    mock_result.objects = []
    mock_weaviate_client.collections.get().query.bm25.return_value = mock_result
    
    context_segments, keywords = processor.search_weaviate("test query")
    assert isinstance(context_segments, list)
    assert isinstance(keywords, list)

@pytest.mark.asyncio
async def test_process_prompt_endpoint(test_client):
    test_prompt = "Test prompt"
    response = test_client.post(
        "/process-prompt",
        json={"user_prompt_text": test_prompt}
    )
    
    assert response.status_code == 200
    assert "generated_response" in response.json()
    assert "context_segments" in response.json()
    assert "keywords" in response.json()