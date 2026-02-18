from __future__ import annotations

from src.classifier import predict_category_with_confidence
from src.llm import generate_response


def run_workflow(user_input: str):
    category, conf = predict_category_with_confidence(user_input)
    print(f"[debug] category={category}, confidence={conf:.2f}")

    # Tier 1: High confidence
    if conf >= 0.60:
        return category, generate_response(category, user_input)

    # Tier 2: Medium confidence -> answer + ask one clarifying question
    if conf >= 0.40:
        response = generate_response(category, user_input)
        follow_up = {
            "Rechnung": "Können Sie mir bitte den Abrechnungsmonat und den aktuellen Zählerstand nennen?",
            "Vertrag": "Geht es um Kündigung, Tarifwechsel oder eine Adressänderung?",
            "Technik": "Können Sie bitte Ihre Adresse und (falls vorhanden) die Zählernummer angeben?",
            "Abschlag": "Möchten Sie den Abschlag erhöhen oder senken – und wie hoch ist Ihr aktueller Abschlag?",
        }.get(category, "Können Sie bitte ein paar zusätzliche Details nennen?")

        return category, f"{response}\n\nRückfrage: {follow_up}"

    # Tier 3: Low confidence -> fallback
    return "Unklar", (
        "Ich bin mir nicht sicher, ob ich Ihre Anfrage korrekt einordnen kann. "
        "Bitte geben Sie mehr Details an oder kontaktieren Sie unseren Kundenservice direkt."
    )

