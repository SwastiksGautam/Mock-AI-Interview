from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from app.services.mock_database import mock_questions
from app.services.evaluator import evaluate_answer, generate_transition

router = APIRouter()
sessions = {}

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())

    # Initialize session state
    sessions[session_id] = {
        "current_index": 0  # Start at first question (index 0)
    }

    first_question = {
        "text": mock_questions[0]["question_text"]
    }

    return {
        "session_id": session_id,
        "question": first_question
    }

@router.post("/answer")
def submit_answer(payload: AnswerRequest):
    session_id = payload.session_id
    candidate_answer = payload.answer

    if session_id not in sessions:
        return {"error": "Invalid session ID"}

    session = sessions[session_id]
    current_idx = session["current_index"]

    # Get current question data
    current_question = mock_questions[current_idx]
    ideal_answer = current_question["ideal_answer"]

    # Evaluate answer
    evaluation = evaluate_answer(
        question_text=current_question["question_text"],
        candidate_answer=candidate_answer,
        ideal_answer=ideal_answer
    )

    # Move to next question
    session["current_index"] += 1

    if session["current_index"] >= len(mock_questions):
        # Interview complete → return summary
        return {
            "summary": {
                "overall_score": evaluation["average_score"],
                "strengths": ["Good understanding of Excel concepts"],
                "areas_for_improvement": ["Elaborate more with examples"],
                "detailed_feedback": evaluation["feedback"]
            }
        }

    # Next question
    next_question_text = mock_questions[session["current_index"]]["question_text"]

    # Generate a transition sentence
    transition = generate_transition(
        feedback=evaluation["feedback"],
        next_question=next_question_text
    )

    return {
        "evaluation": evaluation,
        "question": {"text": next_question_text},
        "transition": transition
    }
