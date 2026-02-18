#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate a synthetic customer support dataset for an energy provider.
Outputs: data/customer_questions.csv

Categories:
- Rechnung (billing/invoice)
- Vertrag (contract)
- Technik (technical issues)
- Abschlag (monthly installment)

Usage:
  python scripts/generate_data.py --n 80 --out data/customer_questions.csv --seed 42
"""

from __future__ import annotations

import argparse
import csv
import os
import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class TemplatePool:
    label: str
    templates: List[str]


def _pick(rng: random.Random, items: List[str]) -> str:
    return rng.choice(items)


def _format(rng: random.Random, tpl: str) -> str:
    """Fill placeholders in templates."""
    salutation = _pick(rng, ["Hallo", "Guten Tag", "Hi", "Moin"])
    name = _pick(rng, ["", " Team", " Support-Team", ""])
    month = _pick(rng, ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"])
    amount = _pick(rng, ["45", "59", "72", "89", "110", "135", "168", "210"])
    contract_id = _pick(rng, ["VK-10293", "VK-23811", "VK-45012", "VK-77801", "VK-99007"])
    meter_id = _pick(rng, ["Z-100238", "Z-220901", "Z-340771", "Z-558012", "Z-771204"])
    address = _pick(rng, ["Frankfurt", "Friedberg", "Gießen", "Hanau", "Darmstadt"])
    reason = _pick(rng, ["Umzug", "Preis", "Kundenservice", "Tarifwechsel", "Doppelzahlung"])
    channel = _pick(rng, ["per E-Mail", "online", "über das Portal", "telefonisch", "in der App"])

    return tpl.format(
        salutation=salutation,
        name=name,
        month=month,
        amount=amount,
        contract_id=contract_id,
        meter_id=meter_id,
        address=address,
        reason=reason,
        channel=channel,
    ).strip()


def build_pools() -> List[TemplatePool]:
    rechnung = TemplatePool(
        label="Rechnung",
        templates=[
            "{salutation}{name}, meine Stromrechnung ist diesen {month} ungewöhnlich hoch. Können Sie das prüfen?",
            "Warum ist meine Rechnung höher als erwartet? Ich habe meinen Verbrauch nicht erhöht.",
            "Ich glaube, ich habe eine Doppelabbuchung. Können Sie die Rechnung und Zahlung überprüfen?",
            "Bitte senden Sie mir eine detaillierte Erklärung zur Rechnung für {month}.",
            "Ich vermute einen falschen Zählerstand auf der Rechnung. Zähler-ID: {meter_id}.",
            "Die Rechnung scheint geschätzt zu sein. Wie kann ich den korrekten Zählerstand nachreichen {channel}?",
            "Ich habe eine Mahnung erhalten, aber ich habe bereits bezahlt. Betrag: {amount} EUR.",
            "Können Sie mir eine Rechnungskopie zusenden? Vertragsnummer: {contract_id}.",
            "Ich habe den Tarif gewechselt und möchte verstehen, wie die Rechnung berechnet wurde.",
            "Warum wurden zusätzliche Gebühren berechnet? Bitte erklären Sie die Positionen auf der Rechnung.",
        ],
    )

    vertrag = TemplatePool(
        label="Vertrag",
        templates=[
            "{salutation}{name}, ich möchte meinen Vertrag kündigen. Wie gehe ich vor?",
            "Wie lange läuft mein Vertrag noch? Vertragsnummer: {contract_id}.",
            "Ich möchte von meinem Sonderkündigungsrecht wegen {reason} Gebrauch machen.",
            "Kann ich meinen Vertrag auf eine andere Person übertragen (z.B. bei {reason})?",
            "Ich bin umgezogen nach {address}. Wie melde ich die neue Adresse und den Einzug?",
            "Welche Fristen gelten für eine Kündigung und wann ist der nächstmögliche Termin?",
            "Ich möchte meine Vertragsdaten aktualisieren. Wo kann ich das {channel} machen?",
            "Wie kann ich meinen Tarif wechseln? Gibt es günstigere Optionen?",
            "Bitte bestätigen Sie mir schriftlich die Vertragskündigung.",
            "Ich habe Fragen zu Vertragslaufzeit und Preisgarantie. Können Sie mir das erklären?",
        ],
    )

    technik = TemplatePool(
        label="Technik",
        templates=[
            "{salutation}{name}, bei mir gibt es einen Stromausfall in {address}. Was kann ich tun?",
            "Mein Zähler funktioniert nicht / zeigt nichts mehr an. Zähler-ID: {meter_id}.",
            "Ich habe einen neuen Zähler erhalten. Wie erfolgt die Inbetriebnahme?",
            "Die Verbrauchswerte scheinen unplausibel. Können Sie den Zähler prüfen?",
            "Ich möchte den Zählerstand melden, aber das Portal zeigt einen Fehler.",
            "Ich habe flackerndes Licht und Spannungsschwankungen. An wen kann ich mich wenden?",
            "Wie kann ich einen technischen Defekt melden und wie lange dauert die Bearbeitung?",
            "Ich benötige Unterstützung beim Smart-Meter. Zähler-ID: {meter_id}.",
            "Die App erkennt meinen Vertrag nicht. Vertragsnummer: {contract_id}.",
            "Ich habe eine Störung gemeldet, aber keine Rückmeldung erhalten. Können Sie den Status prüfen?",
        ],
    )

    abschlag = TemplatePool(
        label="Abschlag",
        templates=[
            "{salutation}{name}, ich möchte meinen monatlichen Abschlag anpassen. Wie geht das {channel}?",
            "Kann ich meinen Abschlag reduzieren? Aktuell zahle ich {amount} EUR pro Monat.",
            "Bitte erhöhen Sie meinen Abschlag, da mein Verbrauch gestiegen ist.",
            "Wie wird der Abschlag berechnet und wann wird er angepasst?",
            "Ich habe eine neue Person im Haushalt. Können wir den Abschlag neu berechnen?",
            "Ich möchte den Abbuchungstermin für den Abschlag ändern. Ist das möglich?",
            "Der Abschlag wurde ohne Info geändert. Können Sie mir den Grund nennen?",
            "Kann ich eine einmalige Sonderzahlung leisten, um den Abschlag zu stabilisieren?",
            "Wie kann ich den Abschlag pausieren oder stunden (z.B. wegen {reason})?",
            "Ich möchte meinen Abschlag auf Basis aktueller Zählerstände aktualisieren.",
        ],
    )

    return [rechnung, vertrag, technik, abschlag]


def generate_rows(n: int, seed: int) -> List[Tuple[str, str]]:
    rng = random.Random(seed)
    pools = build_pools()

    # Ensure balanced distribution across classes
    base = n // len(pools)
    remainder = n % len(pools)

    rows: List[Tuple[str, str]] = []
    for i, pool in enumerate(pools):
        k = base + (1 if i < remainder else 0)
        for _ in range(k):
            tpl = _pick(rng, pool.templates)
            text = _format(rng, tpl)

            # Add a bit of random "noise" to avoid too repetitive patterns
            if rng.random() < 0.25:
                suffix = _pick(rng, [" Danke!", " Vielen Dank.", " Bitte um kurze Rückmeldung.", " Können Sie helfen?"])
                text = f"{text}{suffix}"

            rows.append((text, pool.label))

    rng.shuffle(rows)
    return rows


def write_csv(rows: List[Tuple[str, str]], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=80, help="Total number of samples to generate (default: 80)")
    p.add_argument("--out", type=str, default="data/customer_questions.csv", help="Output CSV path")
    p.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.n < 20:
        raise SystemExit("Please generate at least 20 samples for a meaningful prototype (e.g., --n 40).")

    rows = generate_rows(n=args.n, seed=args.seed)
    write_csv(rows, out_path=args.out)
    print(f"✅ Generated {len(rows)} rows → {args.out}")


if __name__ == "__main__":
    main()
