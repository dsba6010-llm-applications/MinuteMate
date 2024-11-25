from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualPrecisionMetric, ToxicityMetric, HallucinationMetric, ContextualRecallMetric
from deepeval import evaluate
import requests
import json


def test_cases():
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.8)
    answer_faithfulness_metric = FaithfulnessMetric(threshold=0.5)
    answer_precision_metric = ContextualPrecisionMetric(threshold=0.7)
    answer_toxicity_metric = ToxicityMetric(threshold=0.5)
    answer_hallucination_metric = HallucinationMetric(threshold=0.5)
    answer_contexualrecall_metric = ContextualRecallMetric(threshold=0.7)

    with open('MinuteMate\\test\\test_data.json', 'r') as file:
        data = json.load(file)
    
    for item in data:
        input=item["prompt"]
        retrieval_context = item["retrieval_context"]
        expected_output = item["expected_output"]
        print (input) 
        response = requests.post(
                "http://127.0.0.1:8000/process-prompt",  # Adjust URL as needed
                json={"user_prompt_text": input}
            )
        generated_response = response.json().get('generated_response', 'No response generated')
        print(generated_response)
        test_case_1 = LLMTestCase(
            input=input,
            # Replace this with the actual output of your LLM application
            actual_output=generated_response,
            retrieval_context = [retrieval_context]
        )
        test_case_2 = LLMTestCase(
            input=input,
            # Replace this with the actual output of your LLM application
            actual_output=generated_response,
            expected_output=expected_output,
            retrieval_context = [retrieval_context]
        )

        assert_test(test_case_1, [answer_relevancy_metric, answer_faithfulness_metric, answer_toxicity_metric])
        assert_test(test_case_2, [answer_precision_metric, answer_contexualrecall_metric])


def test_case_hallucination():
    answer_hallucination_metric = HallucinationMetric(threshold=0.5)
    with open('MinuteMate\\test\\test_data_hallucination.json', 'r') as file:
        data = json.load(file)
    
    for item in data:
        input=item["prompt"]
        retrieval_context = item["retrieval_context"]
        expected_output = item["expected_output"]
        print (input) 
        response = requests.post(
                "http://127.0.0.1:8000/process-prompt",  # Adjust URL as needed
                json={"user_prompt_text": input}
            )
        generated_response = response.json().get('generated_response', 'No response generated')
        print(generated_response)

        test_case_3 = LLMTestCase(
            input=input,
            # Replace this with the actual output of your LLM application
            actual_output=generated_response,
            context = [retrieval_context]
        )

        assert_test(test_case_3, [answer_hallucination_metric])