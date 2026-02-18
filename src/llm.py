from __future__ import annotations


def generate_response(category: str, user_input: str) -> str:
    """
    Stub LLM response (offline).
    Replace later with a real LLM call.
    """
    templates = {
        "Rechnung": "Ich verstehe. Bitte prüfen Sie Ihre Rechnung im Kundenportal und senden Sie uns ggf. den Zählerstand. Wir schauen uns das gerne an.",
        "Vertrag": "Gerne. Für Vertragsänderungen oder Kündigung finden Sie die Optionen im Kundenportal. Wenn Sie möchten, kann ich die nächsten Schritte kurz erklären.",
        "Technik": "Das klingt nach einem technischen Problem. Bitte prüfen Sie zuerst Sicherungen. Falls die Störung bleibt, melden Sie die Störung mit Adresse und Zählernummer.",
        "Abschlag": "Kein Problem. Den Abschlag können Sie meist im Kundenportal anpassen. Auf Wunsch berechnen wir ihn auf Basis Ihres aktuellen Verbrauchs neu.",
    }
    base = templates.get(category, "Danke für Ihre Anfrage. Können Sie bitte noch ein paar Details nennen?")
    return f"{base}\n\n(Anfrage: {user_input})"
