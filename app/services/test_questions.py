from __future__ import annotations

from typing import Dict, List

LIKERT_OPTIONS = [
    {"value": 1, "label": "Kesinlikle Katılmıyorum"},
    {"value": 2, "label": "Katılmıyorum"},
    {"value": 3, "label": "Kararsızım"},
    {"value": 4, "label": "Katılıyorum"},
    {"value": 5, "label": "Kesinlikle Katılıyorum"},
]

BIG_FIVE_QUESTIONS: List[Dict] = [
    {"id": f"bf_{i}", "type": "big_five", "text": f"Big Five soru {i}", "options": LIKERT_OPTIONS}
    for i in range(1, 51)
]

MBTI_QUESTIONS: List[Dict] = [
    {"id": f"mbti_{i}", "type": "mbti", "text": f"MBTI soru {i}", "options": LIKERT_OPTIONS}
    for i in range(1, 21)
]
