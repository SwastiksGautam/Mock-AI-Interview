from fastapi import APIRouter
import uuid

router = APIRouter()

@router.get("/interview-question")
def get_interview_question():
    return {"question": "What is a circular import?"}

@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())
    first_question = {
        "text": "What is a circular import?"
    }
    return {
        "session_id": session_id,
        "question": first_question
    }
