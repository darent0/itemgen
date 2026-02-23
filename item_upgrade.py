#!/usr/bin/env python3
"""Ein kleines WoW-inspiriertes Item-Upgrade-Spiel für die Konsole."""

from __future__ import annotations

import random
from dataclasses import dataclass


# Seltenheitswahrscheinlichkeiten (in Prozent)
RARITY_CHANCES = [
    ("Grau", 6.25, "\033[90m"),
    ("Weiß", 60.95, "\033[97m"),
    ("Grün", 31.25, "\033[92m"),
    ("Blau", 1.25, "\033[94m"),
    ("Lila", 0.25, "\033[95m"),
    ("Orange", 0.05, "\033[38;5;208m"),
]

RARITY_ORDER = {rarity: index for index, (rarity, _, _) in enumerate(RARITY_CHANCES)}

RESET = "\033[0m"

PREFIXES = [
    "Vergessene",
    "Stählerne",
    "Schattenhafte",
    "Runenverzierte",
    "Heilige",
    "Blutrote",
    "Flüsternde",
    "Sonnengeprägte",
    "Verfluchte",
    "Drachenzahn",
]

SUFFIXES = [
    "Klinge",
    "Schneide",
    "Kurzschwert",
    "Kriegsklinge",
    "Säbel",
    "Stoßklinge",
    "Wächterschwert",
    "Lichtschneide",
    "Nachtklinge",
    "Sturmschwert",
]


@dataclass
class Item:
    name: str
    rarity: str
    color_code: str
    itemlevel: int


def roll_itemlevel(current_level: int) -> int:
    """70% gleich, 20% +1, 10% +2."""
    roll = random.random()
    if roll < 0.70:
        return current_level
    if roll < 0.90:
        return current_level + 1
    return current_level + 2


def roll_rarity() -> tuple[str, str]:
    """Wählt die Seltenheit anhand der angegebenen Wahrscheinlichkeiten."""
    roll = random.random() * 100
    cumulative = 0.0

    for rarity, chance, color in RARITY_CHANCES:
        cumulative += chance
        if roll <= cumulative:
            return rarity, color

    # Fallback bei Rundungsfehlern
    last_rarity, _, last_color = RARITY_CHANCES[-1]
    return last_rarity, last_color


def keep_current_rarity_on_downgrade(
    current_item: Item, new_itemlevel: int, new_rarity: str, new_color: str
) -> tuple[str, str]:
    """Bei gleichem Itemlevel bleibt die aktuelle Farbe, falls ein niedrigerer Roll kommt."""
    current_rank = RARITY_ORDER[current_item.rarity]
    new_rank = RARITY_ORDER[new_rarity]

    if new_itemlevel == current_item.itemlevel and new_rank < current_rank:
        return current_item.rarity, current_item.color_code

    return new_rarity, new_color


def generate_unique_sword_name(used_names: set[str], roll_number: int) -> str:
    """Erzeugt möglichst eindeutige Schwertnamen."""
    for _ in range(100):
        name = f"{random.choice(PREFIXES)} {random.choice(SUFFIXES)}"
        if name not in used_names:
            used_names.add(name)
            return name

    # Falls doch alles aufgebraucht ist, wird eine laufende Nummer ergänzt.
    fallback = f"Verlorene Klinge #{roll_number}"
    used_names.add(fallback)
    return fallback


def print_item(item: Item) -> None:
    print("\nDein aktuelles Item:")
    print(f"Typ: Einhandschwert")
    print(f"Name: {item.color_code}{item.name}{RESET} ({item.rarity})")
    print(f"Itemlevel: {item.itemlevel}")


def main() -> None:
    print("=== WoW-Style Item Upgrade ===")
    print("Startitem: Graues Einhandschwert mit Itemlevel 100")
    print("Jeder Roll erzeugt einen neuen Namen und eine neue Seltenheit.")

    used_names: set[str] = set()
    roll_number = 1

    start_name = generate_unique_sword_name(used_names, roll_number)
    current_item = Item(name=start_name, rarity="Grau", color_code="\033[90m", itemlevel=100)
    print_item(current_item)

    while True:
        user_input = input("\nDrücke [Enter] für Roll oder tippe 'q' zum Beenden: ").strip().lower()
        if user_input == "q":
            print("\nViel Erfolg auf deinem Loot-Abenteuer!")
            break

        roll_number += 1
        new_level = roll_itemlevel(current_item.itemlevel)
        rarity, color = roll_rarity()
        rarity, color = keep_current_rarity_on_downgrade(current_item, new_level, rarity, color)
        name = generate_unique_sword_name(used_names, roll_number)

        current_item = Item(name=name, rarity=rarity, color_code=color, itemlevel=new_level)
        print_item(current_item)


if __name__ == "__main__":
    main()
