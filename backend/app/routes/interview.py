# app/routes/interview.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import os
import json
from datetime import datetime

# Corrected import of services
from app.services.evaluator import generate_excel_question, evaluate_answer, generate_transition, generate_summary_feedback

router = APIRouter()

# In-memory store for interview sessions.
active_sessions = {}
SESSIONS_FILE = "sessions.json"

# Helper function to save sessions to disk
def save_sessions():
    with open(SESSIONS_FILE, "w") as f:
        json.dump(active_sessions, f, indent=2, default=str)

# ------------------- Routes -------------------
@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())
    
    # Dynamically generate the first question
    first_question = generate_excel_question(stage=1)
    
    # Store the entire question object, including the ideal answer, in the session state
    active_sessions[session_id] = {
        "stage": 1,
        "questions_asked": [first_question.dict()], # Store as a list
        "history": []
    }
    save_sessions()

    return {
        "session_id": session_id,
        "question": {
            "id": first_question.id,
            "text": f"Welcome! I'm your AI interviewer. Let's start with some quick questions. First up: {first_question.question_text}"
        }
    }

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/answer")
def submit_answer(request: AnswerRequest):
    session_id = request.session_id
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    session = active_sessions[session_id]
    
    # Check for "I don't know" or similar answers
    if any(keyword in request.answer.lower() for keyword in ["i don't know", "i am not sure", "pass", "no idea"]):
        # Add a record to history for this skipped question
        current_question_data = session["questions_asked"][-1]
        session["history"].append({
            "question_id": current_question_data['id'],
            "question_text": current_question_data['question_text'],
            "answer": request.answer,
            "evaluation": {"average_score": 1.0, "feedback": "Answer was not provided.", "is_sufficient": False}
        })
        
        # Move to the next question
        current_stage = session["stage"]
        next_stage_threshold = 5
        
        if len(session["questions_asked"]) >= next_stage_threshold:
            return {"session_id": session_id, "summary": generate_summary(session)}

        next_question = generate_excel_question(stage=current_stage)
        session["questions_asked"].append(next_question.dict())
        
        transition_text = generate_transition(
            feedback="That's okay. Let's try another one.",
            next_question=next_question.question_text
        )
        
        return {
            "session_id": session_id,
            "question": {"id": next_question.id, "text": transition_text},
            "previous_answer_feedback": "Answer was not provided."
        }
    
    # Get the details of the question the user just answered
    current_question_data = session["questions_asked"][-1]
    
    # Evaluate the answer using the ideal answer we stored earlier
    evaluation = evaluate_answer(
        question_text=current_question_data['question_text'],
        candidate_answer=request.answer,
        ideal_answer=current_question_data['ideal_answer']
    )
    
    # Store history
    session["history"].append({
        "question_id": current_question_data['id'],
        "question_text": current_question_data['question_text'],
        "answer": request.answer,
        "evaluation": evaluation
    })

    # Decide if the interview is over or if we need to generate a new question
    current_stage = session["stage"]
    next_stage_threshold = 3 # Let's say we ask 3 questions per stage
    
    if len(session["questions_asked"]) >= next_stage_threshold:
        if current_stage == 1:
            total_score = sum(h['evaluation']['average_score'] for h in session['history'][-next_stage_threshold:])
            avg_score = total_score / next_stage_threshold
            
            if avg_score >= 3.0: 
                session["stage"] = 2
                next_question = generate_excel_question(stage=2)
                session["questions_asked"].append(next_question.dict())
                
                transition_text = generate_transition(
                    feedback="Great job on those warm-up questions.",
                    next_question=next_question.question_text
                )
                return {"session_id": session_id, "question": {"id": next_question.id, "text": transition_text}}
            else:
                return {"session_id": session_id, "summary": generate_summary(session)}
        else: # Stage 2 complete
            return {"session_id": session_id, "summary": generate_summary(session)}

    # If not complete, generate a new question
    next_question = generate_excel_question(stage=current_stage)
    session["questions_asked"].append(next_question.dict())
    
    transition_text = generate_transition(
        feedback=evaluation['feedback'],
        next_question=next_question.question_text
    )
    
    return {
        "session_id": session_id,
        "question": {"id": next_question.id, "text": transition_text},
        "previous_answer_feedback": evaluation['feedback']
    }


def generate_summary(session):
    history = session['history']
    if not history:
        return {"overall_score": 0, "strengths": [], "areas_for_improvement": [], "detailed_feedback": "No questions were answered."}

    # Use the LLM to generate keywords for strengths and areas for improvement
    summary_feedback = generate_summary_feedback(history)
    
    total_score = sum(h['evaluation']['average_score'] for h in history)
    overall_score = round(total_score / len(history), 2)
    
    detailed_feedback = "Performance Summary:\n"
    for item in history:
        detailed_feedback += f"- Q: {item['question_text']}\n  - Score: {item['evaluation']['average_score']}/5\n  - Feedback: {item['evaluation']['feedback']}\n"
        
    return {
        "overall_score": overall_score,
        "strengths": summary_feedback.get('strengths', []),
        "areas_for_improvement": summary_feedback.get('areas_for_improvement', []),
        "detailed_feedback": detailed_feedback
    }