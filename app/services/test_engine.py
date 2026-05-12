from __future__ import annotations

import random
import time
import uuid
from typing import Dict

from .psychometric_service import PsychometricService
from .stroop import generate_stroop_questions
from .test_questions import BIG_FIVE_QUESTIONS, MBTI_QUESTIONS


class CompositeTestEngine:
    def __init__(self, psychometric_service: PsychometricService, duration_seconds: int = 30) -> None:
        self.psychometric_service = psychometric_service
        self.duration_seconds = duration_seconds
        self.sessions: Dict[str, Dict] = {}

    def start_test(self) -> Dict:
        sid = str(uuid.uuid4())
        stroop = generate_stroop_questions(30)
        questions = BIG_FIVE_QUESTIONS + MBTI_QUESTIONS + stroop
        random.shuffle(questions)
        self.sessions[sid] = {"questions": questions, "answers": {}, "index": 0, "expires": time.time() + self.duration_seconds}
        return {"session_id": sid, "total_questions": 100, "duration": self.duration_seconds}

    def get_question(self, session_id: str) -> Dict:
        s = self.sessions[session_id]
        if time.time() > s["expires"] or s["index"] >= len(s["questions"]):
            return {"done": True}
        q = dict(s["questions"][s["index"]])
        q.pop("correct", None)
        return {"done": False, "index": s["index"] + 1, "remaining_seconds": max(0, int(s["expires"] - time.time())), "question": q}

    def submit_answer(self, session_id: str, question_id: str, answer) -> Dict:
        s = self.sessions[session_id]
        s["answers"][question_id] = answer
        s["index"] += 1
        return {"accepted": True}

    def finish_test(self, session_id: str) -> Dict:
        s = self.sessions[session_id]
        responses = []
        for i in range(1, 91):
            qid = f"bf_{i}" if i <= 50 else f"mbti_{i-50}"
            responses.append(int(s["answers"].get(qid, 3)))
        responses.extend([3] * 10)
        scored = self.psychometric_service.score(responses)
        stroop_q = [q for q in s["questions"] if q["type"] == "stroop"]
        correct = 0
        for q in stroop_q:
            if s["answers"].get(q["id"]) == q.get("correct"):
                correct += 1
        scored["stroop"] = {"correct": correct, "total": len(stroop_q), "accuracy": round((correct / len(stroop_q)) * 100, 2) if stroop_q else 0}
        scored["answered"] = len(s["answers"])
        scored["total"] = len(s["questions"])
        return scored
