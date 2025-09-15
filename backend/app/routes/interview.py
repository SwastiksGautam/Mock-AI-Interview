from fastapi import APIRouter
from pydantic import BaseModel

import uuid

router = APIRouter()

# Simple in-memory session store (for demonstration)
sessions = {}

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.get("/interview-question")
def get_interview_question():
    return {"question": "What is a circular import?"}

@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())
    first_question = {
        "text": "What is a circular import?"
    }
    sessions[session_id] = {"question_count": 1}
    return {
        "session_id": session_id,
        "question": first_question
    }

@router.post("/answer")
def submit_answer(payload: AnswerRequest):
    session_id = payload.session_id
    answer = payload.answer

    if session_id not in sessions:
        return {"error": "Invalid session ID"}

    sessions[session_id]["question_count"] += 1

    # For simplicity: After 3 questions, send a summary
    if sessions[session_id]["question_count"] > 3:
        return {
            "summary": {
                "overall_score": 4.2,
                "strengths": ["Good understanding of concepts"],
                "areas_for_improvement": ["Elaborate answers more"],
                "detailed_feedback": "Well done, but try to give examples next time."
            }
        }

    # Otherwise, send the next question
    next_question = {
        "text": f"This is question #{sessions[session_id]['question_count']}: Explain polymorphism."
    }

    return {
        "question": next_question
    }
