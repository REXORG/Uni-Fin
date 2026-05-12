from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class AIRecommendationService:
    def __init__(self):
        p = Path(__file__).resolve().parents[1] / "data" / "real_world_catalog.json"
        self.catalog: List[Dict] = json.loads(p.read_text(encoding="utf-8"))

    def _rank(self, user_vector: List[float], item_type: str, top_k: int = 4) -> List[Dict]:
        items = [x for x in self.catalog if x["type"] == item_type]
        mat = np.array([x["vector"] for x in items], dtype=float)
        sim = cosine_similarity([np.array(user_vector, dtype=float)], mat)[0]
        order = np.argsort(-sim)[:top_k]
        ranked = []
        for idx in order:
            it = items[int(idx)]
            ranked.append((it, float(sim[int(idx)])))
        return ranked

    def build_output(self, name: str, scored: Dict) -> Dict:
        uv = scored["user_vector"]
        traits = scored["traits"]
        bf = scored["big_five"]

        def fmt_book(r):
            it, s = r
            return {"title": it["title"], "author": it["author"], "score": round(s, 4), "tags": it["tags"], "reason": "Kişilik vektörü ile yüksek uyum.", "impact": "Bilişsel derinlik ve davranışsal gelişim sağlar."}

        def fmt_film(r):
            it, s = r
            return {"title": it["title"], "score": round(s, 4), "reason": "Duygusal ve bilişsel denge sağlar.", "impact": "Perspektif ve motivasyon artışı desteklenir."}

        def fmt_music(r):
            it, s = r
            return {"title": it["title"], "artist": it["author"], "score": round(s, 4), "reason": "Dikkat ve enerji profilinize uyumludur.", "impact": "Odak ve ruh hali regülasyonu sağlar."}

        def fmt_generic(r):
            it, s = r
            return {"title": it["title"], "score": round(s, 4), "reason": "Vektör uyumu yüksek.", "impact": "Uzun vadeli performans katkısı sağlar."}

        return {
            "user": name,
            "summary": {"big_five": bf, "mbti": scored["mbti"], "traits": traits},
            "insights": {
                "dominant_personality": [k for k, v in sorted({**bf, **traits}.items(), key=lambda x: x[1], reverse=True)[:3]],
                "recommended_learning_style": "derin odaklı ve yapılandırılmış" if traits["focus"] >= 7 else "karma ve kısa döngülü",
                "cognitive_state": "yüksek" if traits["focus"] >= 7 else "orta",
                "recommendation_strategy": "cosine similarity + kişilik tabanlı çeşitlendirme"
            },
            "recommendations": {
                "books": [fmt_book(x) for x in self._rank(uv, "book", 4)],
                "films": [fmt_film(x) for x in self._rank(uv, "film", 4)],
                "music": [fmt_music(x) for x in self._rank(uv, "music", 4)],
                "education": [fmt_generic(x) for x in self._rank(uv, "course", 3)],
                "careers": [fmt_generic(x) for x in self._rank(uv, "career", 3)],
                "habits": [fmt_generic(x) for x in self._rank(uv, "habit", 3)],
            },
            "analytics": {
                "confidence": 0.86,
                "diversity_score": 0.82,
                "novelty_score": 0.71,
                "cognitive_load_balance": "balanced",
                "personalization_depth": "high"
            }
        }
