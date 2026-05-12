from __future__ import annotations

import random
from typing import Dict, List

COLORS = ["KIRMIZI", "MAVI", "YESIL", "SARI", "TURUNCU"]


def generate_stroop_questions(count: int = 30) -> List[Dict]:
    out: List[Dict] = []
    for i in range(1, count + 1):
        word = random.choice(COLORS)
        ink = random.choice([c for c in COLORS if c != word])
        out.append({
            "id": f"stroop_{i}",
            "type": "stroop",
            "text": word,
            "display_color": ink.lower(),
            "correct": ink,
            "options": [{"value": c, "label": c} for c in COLORS],
        })
    return out
