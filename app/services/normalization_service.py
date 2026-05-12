from typing import Dict


class NormalizationService:
    @staticmethod
    def clamp01(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def normalize_big_five(self, scores: Dict[str, float]) -> Dict[str, float]:
        keys = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        return {k: self.clamp01(scores.get(k, 0.5)) for k in keys}
