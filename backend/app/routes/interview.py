from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from app.services.mock_database import mock_questions
from app.services.evaluator import evaluate_answer, generate_transition

router = APIRouter()
sessions = {}

MAX_QUESTIONS_PER_SESSION = 5  # Ask exactly 5 questions per interview session

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())

    # Initialize session state
    sessions[session_id] = {
        "current_index": 0,  # Start at first question (index 0)
        "answers": []        # Store candidate's answers and evaluations
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

    if current_idx >= len(mock_questions):
        return {"error": "No more questions available"}

    current_question = mock_questions[current_idx]
    ideal_answer = current_question["ideal_answer"]

    # Evaluate the answer
    evaluation = evaluate_answer(
        question_text=current_question["question_text"],
        candidate_answer=candidate_answer,
        ideal_answer=ideal_answer
    )

    # Save the answer and evaluation
    session["answers"].append({
        "question": current_question["question_text"],
        "candidate_answer": candidate_answer,
        "evaluation": evaluation
    })

    session["current_index"] += 1

    # Check if we reached the max questions per session
    if session["current_index"] >= MAX_QUESTIONS_PER_SESSION or session["current_index"] >= len(mock_questions):
        # Return summary after 5 questions or when questions run out
        avg_score = sum(ans["evaluation"]["average_score"] for ans in session["answers"]) / len(session["answers"])

        return {
            "summary": {
                "total_questions": len(session["answers"]),
                "average_score": round(avg_score, 2),
                "strengths": ["Good understanding of Excel concepts"],
                "areas_for_improvement": ["Provide more examples where applicable"],
                "detailed_feedbacks": [ans["evaluation"]["feedback"] for ans in session["answers"]]
            }
        }

    # Otherwise, return next question
    next_question_text = mock_questions[session["current_index"]]["question_text"]

    transition = generate_transition(
        feedback=evaluation["feedback"],
        next_question=next_question_text
    )

    return {
        "evaluation": evaluation,
        "question": {"text": next_question_text},
        "transition": transition
    }
