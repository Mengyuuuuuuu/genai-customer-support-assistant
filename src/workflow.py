from src.classifier import predict_category
from src.llm import generate_response

def run_workflow(user_input: str):
    category = predict_category(user_input)
    response = generate_response(user_input)
    return category, response
