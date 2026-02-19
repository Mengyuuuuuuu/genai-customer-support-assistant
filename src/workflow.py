from __future__ import annotations

from src.classifier import predict_category_with_confidence
from src.llm import generate_response


def run_workflow(user_input: str):
    category, conf = predict_category_with_confidence(user_input)
    print(f"[debug] category={category}, confidence={conf:.2f}")

    # Tier 1: High confidence -> answer only
    if conf >= 0.60:
        return category, generate_response(category, user_input, mode="answer_only")

    # Tier 2: Medium confidence -> answer + exactly one clarifying question
    if conf >= 0.40:
        return category, generate_response(category, user_input, mode="answer_plus_question")

    # Tier 3: Low confidence -> fallback
    return "Unklar", (
        "Ich bin mir nicht sicher, ob ich Ihre Anfrage korrekt einordnen kann. "
        "Bitte geben Sie mehr Details an oder kontaktieren Sie unseren Kundenservice direkt."
    )
