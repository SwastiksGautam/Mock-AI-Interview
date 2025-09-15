from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from app.services.mock_database import mock_questions
from app.services.evaluator import evaluate_answer, generate_transition
from app.database import SessionLocal, SessionModel

router = APIRouter()
MAX_QUESTIONS_PER_SESSION = 5  # Fixed number of questions per interview

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())
    db = SessionLocal()

    # Initialize session in DB
    new_session = SessionModel(
        session_id=session_id,
        current_index=0,
        answers=[]
    )
    db.add(new_session)
    db.commit()
    db.close()

    first_question = {
        "text": mock_questions[0]["question_text"]
    }

    return {
        "session_id": session_id,
        "question": first_question
    }

@router.post("/answer")
def submit_answer(payload: AnswerRequest):
    db = SessionLocal()
    session_id = payload.session_id
    candidate_answer = payload.answer

    # Fetch session from DB
    session = db.query(SessionModel).filter_by(session_id=session_id).first()
    if not session:
        # Create new session automatically
        new_session_id = str(uuid.uuid4())
        new_session = SessionModel(
            session_id=new_session_id,
            current_index=0,
            answers=[]
        )
        db.add(new_session)
        db.commit()
        db.close()
        return {
            "error": "Invalid session ID. A new session has been started.",
            "new_session_id": new_session_id,
            "question": {"text": mock_questions[0]["question_text"]}
        }

    current_idx = session.current_index
    if current_idx >= len(mock_questions):
        db.close()
        return {"error": "No more questions available"}

    current_question = mock_questions[current_idx]
    ideal_answer = current_question["ideal_answer"]

    # Evaluate the answer
    evaluation = evaluate_answer(
        question_text=current_question["question_text"],
        candidate_answer=candidate_answer,
        ideal_answer=ideal_answer
    )

    # Store answer and evaluation
    session.answers.append({
        "question": current_question["question_text"],
        "candidate_answer": candidate_answer,
        "evaluation": evaluation
    })
    session.current_index += 1
    db.commit()
    db.close()

    # Check if max questions reached
    if session.current_index >= MAX_QUESTIONS_PER_SESSION or session.current_index >= len(mock_questions):
        total_answers = session.answers
        avg_score = sum(ans["evaluation"]["average_score"] for ans in total_answers) / len(total_answers)
        return {
            "summary": {
                "total_questions": len(total_answers),
                "average_score": round(avg_score, 2),
                "strengths": ["Good understanding of Excel concepts"],
                "areas_for_improvement": ["Provide more detailed examples"],
                "detailed_feedbacks": [ans["evaluation"]["feedback"] for ans in total_answers]
            }
        }

    # Otherwise, send next question
    next_question_text = mock_questions[session.current_index]["question_text"]
    transition = generate_transition(
        feedback=evaluation["feedback"],
        next_question=next_question_text
    )

    return {
        "evaluation": evaluation,
        "question": {"text": next_question_text},
        "transition": transition
    }
