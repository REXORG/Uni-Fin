from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from test_engine import TestEngine

app = FastAPI(title="Uni-Fin Composite Test API")
engine = TestEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SubmitPayload(BaseModel):
    session_id: str
    question_id: str
    answer: str | int


class SessionPayload(BaseModel):
    session_id: str


@app.get("/")
def root():
    return FileResponse("index.html")


@app.post("/start-test")
def start_test():
    return engine.start_test()


@app.post("/get-question")
def get_question(payload: SessionPayload):
    try:
        return engine.get_question(payload.session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/submit-answer")
def submit_answer(payload: SubmitPayload):
    try:
        return engine.submit_answer(payload.session_id, payload.question_id, payload.answer)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/finish-test")
def finish_test(payload: SessionPayload):
    try:
        return engine.finish_test(payload.session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
