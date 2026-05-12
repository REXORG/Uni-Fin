from typing import Dict, List

import numpy as np


class VectorizationService:
    mbti_axes = {"E": 1, "I": -1, "N": 1, "S": -1, "T": 1, "F": -1, "J": 1, "P": -1}

    tag_vocab = [
        "yaratici", "analitik", "bireysel", "grup", "rahatlatici", "odaklanma", "enerjik", "teknik",
        "hikaye", "liderlik", "bilim", "sanat", "farkindalik", "uretkenlik", "muzik_teorisi", "sinema"
    ]

    def mbti_to_vector(self, mbti: str) -> List[float]:
        mbti = (mbti or "INTJ").upper()
        if len(mbti) != 4:
            mbti = "INTJ"
        return [self.mbti_axes.get(c, 0) for c in mbti]

    def user_vector(self, user: Dict) -> np.ndarray:
        b = user["big_five_scores"]
        return np.array([
            b["openness"], b["conscientiousness"], b["extraversion"], b["agreeableness"], b["neuroticism"],
            *self.mbti_to_vector(user["mbti_type"]), float(user.get("attention_score", 0.5)), float(user.get("motivation_score", 0.5)),
        ], dtype=float)

    def content_vector(self, item: Dict) -> np.ndarray:
        diff = float(item["difficulty_level"]) / 5.0
        load = {"dusuk": 0.2, "orta": 0.6, "yuksek": 1.0}[item["cognitive_load"]]
        mood_map = {"sakin": [1, 0, 0], "enerjik": [0, 1, 0], "odak": [0, 0, 1]}
        category_map = {"kitap": [1, 0, 0, 0], "film": [0, 1, 0, 0], "muzik": [0, 0, 1, 0], "kurs": [0, 0, 0, 1]}
        tag_vec = [1.0 if t in item["tags"] else 0.0 for t in self.tag_vocab]
        return np.array([diff, load, *mood_map[item["mood"]], *category_map[item["category"]], *tag_vec], dtype=float)
