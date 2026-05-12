"""Composite test engine for Big Five + MBTI + Stroop."""

from __future__ import annotations

import random
import time
import uuid
from typing import Dict, List

from questions import BIG_FIVE_QUESTIONS, MBTI_QUESTIONS
from stroop import generate_stroop_questions, score_stroop

TEST_DURATION_SECONDS = 30


class TestEngine:
    def __init__(self) -> None:
        self.sessions: Dict[str, Dict] = {}

    def start_test(self) -> Dict:
        session_id = str(uuid.uuid4())
        stroop_questions = generate_stroop_questions(30)
        questions = BIG_FIVE_QUESTIONS[:50] + MBTI_QUESTIONS[:20] + stroop_questions
        random.shuffle(questions)
        self.sessions[session_id] = {
            "id": session_id,
            "questions": questions,
            "answers": {},
            "cursor": 0,
            "started_at": time.time(),
            "expires_at": time.time() + TEST_DURATION_SECONDS,
            "stroop_questions": stroop_questions,
            "finished": False,
        }
        return {"session_id": session_id, "total_questions": len(questions), "duration": TEST_DURATION_SECONDS}

    def _session(self, session_id: str) -> Dict:
        if session_id not in self.sessions:
            raise ValueError("Session not found")
        return self.sessions[session_id]

    def get_question(self, session_id: str) -> Dict:
        session = self._session(session_id)
        if self._is_expired(session) or session["cursor"] >= len(session["questions"]):
            return {"done": True}
        q = session["questions"][session["cursor"]].copy()
        q.pop("correct", None)
        return {
            "done": False,
            "index": session["cursor"] + 1,
            "remaining_seconds": max(0, int(session["expires_at"] - time.time())),
            "question": q,
        }

    def submit_answer(self, session_id: str, question_id: str, answer) -> Dict:
        session = self._session(session_id)
        if self._is_expired(session):
            return {"accepted": False, "reason": "expired"}
        session["answers"][question_id] = answer
        session["cursor"] += 1
        return {"accepted": True, "next_index": session["cursor"] + 1}

    def finish_test(self, session_id: str) -> Dict:
        session = self._session(session_id)
        if session["finished"]:
            return session["result"]
        answers = session["answers"]
        result = {
            "big_five": self._score_big_five(answers),
            "mbti": self._score_mbti(answers),
            "stroop": score_stroop(answers, session["stroop_questions"]),
            "answered": len(answers),
            "total": len(session["questions"]),
            "timed_out": self._is_expired(session),
        }
        session["finished"] = True
        session["result"] = result
        return result

    def _score_big_five(self, answers: Dict[str, int]) -> Dict[str, float]:
        scores = {"extraversion": 0, "conscientiousness": 0, "openness": 0, "agreeableness": 0, "neuroticism": 0}
        counts = {k: 0 for k in scores}
        for q in BIG_FIVE_QUESTIONS[:50]:
            if q["id"] in answers:
                val = int(answers[q["id"]])
                val = 6 - val if q["reverse"] else val
                scores[q["trait"]] += val
                counts[q["trait"]] += 1
        return {k: round(scores[k] / counts[k], 2) if counts[k] else 0 for k in scores}

    def _score_mbti(self, answers: Dict[str, int]) -> Dict[str, str]:
        dims = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
        for q in MBTI_QUESTIONS[:20]:
            if q["id"] in answers:
                val = int(answers[q["id"]]) - 3
                dims[q["dimension"]] += val if q["direction"] == q["dimension"][0] else -val
        return {
            "EI": "E" if dims["EI"] >= 0 else "I",
            "SN": "S" if dims["SN"] >= 0 else "N",
            "TF": "T" if dims["TF"] >= 0 else "F",
            "JP": "J" if dims["JP"] >= 0 else "P",
            "type": f"{'E' if dims['EI'] >= 0 else 'I'}{'S' if dims['SN'] >= 0 else 'N'}{'T' if dims['TF'] >= 0 else 'F'}{'J' if dims['JP'] >= 0 else 'P'}",
        }

    @staticmethod
    def _is_expired(session: Dict) -> bool:
        return time.time() > session["expires_at"]
