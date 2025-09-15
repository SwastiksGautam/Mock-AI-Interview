from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

sessions = {}  # example in-memory session storage

class AnswerPayload(BaseModel):
    session_id: str
    answer: str

@router.post("/answer")
def submit_answer(payload: AnswerPayload):
    session_id = payload.session_id
    answer = payload.answer

    if session_id not in sessions:
        return {
            "error": "Invalid session ID. Please restart the interview."
        }

    # normal processing here
    session = sessions[session_id]
    # ... compute next question or summary
    return {"question": session.get_next_question()}
