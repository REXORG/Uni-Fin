from __future__ import annotations

from typing import Dict, List
import numpy as np


class PsychometricService:
    def _normalize_0_10(self, values: List[float]) -> float:
        arr = np.array(values, dtype=float)
        likert_01 = (arr - 1.0) / 4.0
        return round(float(np.clip(likert_01.mean() * 10.0, 0, 10)), 2)

    def score(self, responses: List[int]) -> Dict:
        if len(responses) != 100:
            raise ValueError("responses must contain exactly 100 items")

        # Big Five blocks: 10 soru / trait
        b_blocks = {
            "openness": responses[0:10],
            "conscientiousness": responses[10:20],
            "extraversion": responses[20:30],
            "agreeableness": responses[30:40],
            "neuroticism": responses[40:50],
        }
        big_five = {k: self._normalize_0_10(v) for k, v in b_blocks.items()}

        # MBTI axes blocks (5 soru / eksen yönü)
        mbti_blocks = {
            "E": responses[50:55], "I": responses[55:60],
            "N": responses[60:65], "S": responses[65:70],
            "T": responses[70:75], "F": responses[75:80],
            "J": responses[80:85], "P": responses[85:90],
        }
        mbti_scores = {k: self._normalize_0_10(v) for k, v in mbti_blocks.items()}
        mbti_type = "".join([
            "E" if mbti_scores["E"] >= mbti_scores["I"] else "I",
            "N" if mbti_scores["N"] >= mbti_scores["S"] else "S",
            "T" if mbti_scores["T"] >= mbti_scores["F"] else "F",
            "J" if mbti_scores["J"] >= mbti_scores["P"] else "P",
        ])

        behavior = responses[90:100]
        traits = {
            "social_energy": round((0.55 * big_five["extraversion"] + 0.45 * mbti_scores["E"]), 2),
            "structure": round((0.6 * big_five["conscientiousness"] + 0.4 * mbti_scores["J"]), 2),
            "empathy": round((0.6 * big_five["agreeableness"] + 0.4 * mbti_scores["F"]), 2),
            "focus": round((0.45 * big_five["conscientiousness"] + 0.35 * mbti_scores["J"] + 0.2 * self._normalize_0_10(behavior[:5])), 2),
            "motivation": round((0.5 * self._normalize_0_10(behavior[5:]) + 0.5 * (10 - big_five["neuroticism"])), 2),
        }

        user_vector = [
            big_five["openness"],
            traits["structure"],
            traits["focus"],
            traits["empathy"],
            traits["social_energy"],
            big_five["conscientiousness"],
            big_five["extraversion"],
            big_five["neuroticism"],
        ]

        return {"big_five": big_five, "mbti": {"axes": mbti_scores, "type": mbti_type}, "traits": traits, "user_vector": user_vector}
