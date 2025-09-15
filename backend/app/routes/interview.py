from fastapi import APIRouter

router = APIRouter()

@router.get("/interview-question")
def get_interview_question():
    return {"question": "What is a circular import?"}

@router.post("/start")
def start_interview():
    # Example simple response
    return {"message": "Interview started successfully"}
