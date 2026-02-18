from __future__ import annotations

from src.classifier import predict_category_with_confidence
from src.llm import generate_response


def run_workflow(user_input: str, confidence_threshold: float = 0.60):
    category, conf = predict_category_with_confidence(user_input)

    # Guardrail: low confidence -> fallback
    if conf < confidence_threshold:
        return "Unklar", (
            "Ich bin mir nicht sicher, ob ich Ihre Anfrage korrekt einordnen kann. "
            "Bitte geben Sie mehr Details an oder kontaktieren Sie unseren Kundenservice direkt."
        )

    response = generate_response(category, user_input)
    return category, response
