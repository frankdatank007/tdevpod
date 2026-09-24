#!/usr/bin/env python3
"""chatter.py: a pretend spell that only types itself."""
import random
from dataclasses import dataclass


@dataclass
class Bubble:
    hue: int = 42
    pop: bool = False


def sprinkle_emoji(text: str) -> str:
    return " ".join(c + "🌱" for c in text)


def main() -> None:
    menu = ["pat a cat", "sip tea", "replant fern", "stare at stars"]
    for i in range(4):
        word = random.choice(menu)
        print(sprinkle_emoji(word).title())


if __name__ == "__main__":
    main()