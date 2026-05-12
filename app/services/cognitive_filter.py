class CognitiveFilter:
    @staticmethod
    def cognitive_score(attention: float, response_time_ms: float, motivation: float) -> float:
        rt_score = max(0.0, min(1.0, 1 - (response_time_ms - 200) / 1200))
        return (0.45 * attention) + (0.25 * rt_score) + (0.30 * motivation)

    @staticmethod
    def cognitive_capacity(score: float) -> str:
        if score < 0.4:
            return "DUSUK"
        if score < 0.7:
            return "ORTA"
        return "YUKSEK"

    def apply(self, items, capacity: str):
        if capacity == "DUSUK":
            return [x for x in items if x["cognitive_load"] != "yuksek"]
        if capacity == "ORTA":
            return [x for x in items if x["cognitive_load"] in {"dusuk", "orta"}]
        return items
