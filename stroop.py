"""Stroop test question generator and scorer."""

from __future__ import annotations

import random
from typing import Dict, List

COLORS = ["KIRMIZI", "MAVI", "YESIL", "SARI", "TURUNCU"]


def generate_stroop_questions(count: int = 30) -> List[Dict]:
    questions = []
    for idx in range(1, count + 1):
        word = random.choice(COLORS)
        ink_color = random.choice([c for c in COLORS if c != word])
        questions.append(
            {
                "id": f"stroop_{idx}",
                "type": "stroop",
                "text": word,
                "display_color": ink_color.lower(),
                "options": [{"value": c, "label": c} for c in COLORS],
                "correct": ink_color,
            }
        )
    return questions


def score_stroop(answers: Dict[str, str], questions: List[Dict]) -> Dict[str, float]:
    total = len(questions)
    correct = sum(1 for q in questions if answers.get(q["id"]) == q["correct"])
    accuracy = (correct / total) * 100 if total else 0.0
    return {"correct": correct, "total": total, "accuracy": round(accuracy, 2)}
