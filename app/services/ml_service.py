from __future__ import annotations
from typing import Dict, List
import numpy as np
from sklearn.linear_model import LogisticRegression
from .vectorization_service import VectorizationService


class MLCompatibilityModel:
    def __init__(self, vectorizer: VectorizationService):
        self.vectorizer = vectorizer
        self.model = LogisticRegression(max_iter=300)
        self.fitted = False

    def _heuristic_label(self, user: Dict, item: Dict) -> int:
        op = user["big_five_scores"]["openness"]
        ex = user["big_five_scores"]["extraversion"]
        score = 0.4 * op + 0.2 * user["attention_score"] + 0.2 * user["motivation_score"]
        if "yaratici" in item["tags"]:
            score += 0.1
        if ex < 0.4 and "bireysel" in item["tags"]:
            score += 0.15
        if item["cognitive_load"] == "yuksek" and user["attention_score"] < 0.4:
            score -= 0.25
        return int(score >= 0.55)

    def train(self, users: List[Dict], items: List[Dict]) -> None:
        X, y = [], []
        for u in users:
            uv = self.vectorizer.user_vector(u)
            for it in items[:80]:
                X.append(np.concatenate([uv, self.vectorizer.content_vector(it)]))
                y.append(self._heuristic_label(u, it))
        self.model.fit(np.array(X), np.array(y))
        self.fitted = True

    def predict_proba(self, user: Dict, items: List[Dict]) -> np.ndarray:
        uv = self.vectorizer.user_vector(user)
        X = [np.concatenate([uv, self.vectorizer.content_vector(it)]) for it in items]
        if not self.fitted:
            return np.full(len(items), 0.5)
        return self.model.predict_proba(np.array(X))[:, 1]
