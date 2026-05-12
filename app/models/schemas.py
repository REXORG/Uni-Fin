from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class UserProfile:
    user_id: str
    big_five_scores: Dict[str, float]
    mbti_type: str
    attention_score: float
    motivation_score: float
    response_time_ms: float
    history: Optional[List[str]] = None


@dataclass
class CognitiveState:
    score: float
    capacity: str
