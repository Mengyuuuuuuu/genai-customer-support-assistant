from __future__ import annotations

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

QWEN_API_KEY = os.getenv("QWEN_API_KEY")

# Qwen OpenAI-compatible endpoint
client = OpenAI(
    api_key=QWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def generate_response(category: str, user_input: str, mode: str = "answer_only") -> str:
    system_msg = (
        "Du bist ein professioneller Kundenservice-Assistent eines Energieversorgers in Deutschland. "
        "Antworte kurz, freundlich und präzise auf Deutsch. "
        "Keine sensiblen Daten erfinden."
    )

    if mode == "answer_only":
        instruction = (
            "Aufgabe:\n"
            "- Formuliere eine hilfreiche Antwort in 3–6 Sätzen.\n"
            "- Stelle KEINE Rückfrage.\n"
        )
    elif mode == "answer_plus_question":
        instruction = (
            "Aufgabe:\n"
            "- Formuliere eine hilfreiche Antwort in 3–6 Sätzen.\n"
            "- Stelle am Ende GENAU 1 gezielte Rückfrage.\n"
        )
    else:
        raise ValueError(f"Unbekannter mode: {mode}")

    user_msg = f"""
Kategorie: {category}
Kundenanfrage: {user_input}

{instruction}
""".strip()

    try:
        resp = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM-Aufruf fehlgeschlagen: {str(e)}"