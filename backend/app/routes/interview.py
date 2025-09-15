from fastapi import APIRouter

router = APIRouter()

@router.get("/interview-question")
def get_interview_question():
    return {"question": "What is a circular import?"}
