from __future__ import annotations

from typing import Dict, List
import numpy as np
from .cognitive_filter import CognitiveFilter
from .similarity_engine import SimilarityEngine
from .vectorization_service import VectorizationService


class RecommendationEngine:
    def __init__(self, vectorizer: VectorizationService, ml_model):
        self.vectorizer = vectorizer
        self.ml_model = ml_model
        self.cognitive_filter = CognitiveFilter()
        self.similarity_engine = SimilarityEngine()

    def _rule_boost(self, user: Dict, item: Dict, cognitive_capacity: str) -> float:
        boost = 0.0
        if cognitive_capacity == "DUSUK" and item["cognitive_load"] == "yuksek":
            return -1.0
        if user["mbti_type"].startswith("I") and "bireysel" in item["tags"]:
            boost += 0.1
        if user["big_five_scores"]["openness"] > 0.7 and "yaratici" in item["tags"]:
            boost += 0.1
        return boost

    def recommend(self, user: Dict, items: List[Dict], cognitive_capacity: str, top_k: int = 10) -> List[Dict]:
        filtered = self.cognitive_filter.apply(items, cognitive_capacity)
        uv = self.vectorizer.user_vector(user)
        item_matrix = np.vstack([self.vectorizer.content_vector(it) for it in filtered])
        n = min(len(uv), item_matrix.shape[1])
        sim_scores = self.similarity_engine.cosine(uv[:n], item_matrix[:, :n])
        ml_scores = self.ml_model.predict_proba(user, filtered)
        out = []
        for i, item in enumerate(filtered):
            rule = self._rule_boost(user, item, cognitive_capacity)
            final = (0.45 * sim_scores[i]) + (0.45 * ml_scores[i]) + (0.10 * (rule + 1) / 2)
            neden = []
            if user["big_five_scores"]["openness"] > 0.7 and "yaratici" in item["tags"]:
                neden.append("yüksek açıklık düzeyi")
            if cognitive_capacity in {"DUSUK", "ORTA"} and item["cognitive_load"] == "dusuk":
                neden.append("düşük bilişsel yük")
            if user["mbti_type"].startswith("I") and "bireysel" in item["tags"]:
                neden.append("içe dönük kullanıcıya uygun bireysel format")
            if not neden:
                neden = ["kişilik-içerik vektör eşleşmesi"]
            out.append({"title": item["title"], "reason": "Eşleşme nedeni: " + " ve ".join(neden), "score": round(float(final), 4)})
        return sorted(out, key=lambda x: x["score"], reverse=True)[:top_k]
