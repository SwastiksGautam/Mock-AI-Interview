from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import os
import json
from datetime import datetime

# Import the services correctly
from app.services.mock_database import get_question, get_questions_by_stage
from app.services.evaluator import evaluate_answer, generate_transition

router = APIRouter()

# In-memory store for interview sessions.
active_sessions = {}
RESULTS_DIR = "results"
SESSIONS_FILE = "sessions.json"

# Helper function to save sessions to disk
def save_sessions():
    with open(SESSIONS_FILE, "w") as f:
        json.dump(active_sessions, f, indent=2, default=str)

# ------------------- Routes -------------------
@router.post("/start")
def start_interview():
    session_id = str(uuid.uuid4())
    stage1_question_ids = get_questions_by_stage(1)
    stage2_question_ids = get_questions_by_stage(2)

    if not stage1_question_ids:
        raise HTTPException(status_code=500, detail="Could not load Stage 1 questions.")

    active_sessions[session_id] = {
        "stage": 1,
        "stage1_question_ids": stage1_question_ids,
        "stage2_question_ids": stage2_question_ids,
        "current_question_index": 0,
        "history": []
    }
    save_sessions()

    first_question_id = stage1_question_ids[0]
    first_question = get_question(first_question_id)
    
    return {
        "session_id": session_id,
        "question": {
            "id": first_question['id'],
            "text": f"Welcome to the interview! Let's start with some quick questions. First up: {first_question['question_text']}"
        }
    }

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/answer")
def submit_answer(request: AnswerRequest):
    # Your /answer route logic here
    session_id = request.session_id
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    session = active_sessions[session_id]
    stage = session["stage"]
    index = session["current_question_index"]
    
    # Get current question details from DB
    current_question_list = session["stage1_question_ids"] if stage == 1 else session["stage2_question_ids"]
    question_id = current_question_list[index]
    question_data = get_question(question_id)
    
    # Evaluate the answer (this needs to be in your evaluator.py)
    evaluation = evaluate_answer(
        question_text=question_data['question_text'],
        candidate_answer=request.answer,
        ideal_answer=question_data['ideal_answer']
    )
    
    # Store history
    session["history"].append({
        "question_id": question_id,
        "question_text": question_data['question_text'],
        "answer": request.answer,
        "evaluation": evaluation
    })

    # Move to the next question
    session["current_question_index"] += 1
    next_index = session["current_question_index"]

    # Check for stage/interview completion
    if next_index >= len(current_question_list):
        if stage == 1:
            total_score = sum(h['evaluation']['average_score'] for h in session['history'] if h['question_id'] in session['stage1_question_ids'])
            avg_score = total_score / len(session['stage1_question_ids'])
            
            if avg_score >= 3.0: # Threshold to pass Stage 1
                session["stage"] = 2
                session["current_question_index"] = 0
                next_question_id = session["stage2_question_ids"][0]
                next_question_data = get_question(next_question_id)
                
                transition_text = generate_transition(
                    feedback="Great job on those warm-up questions.",
                    next_question=next_question_data['question_text']
                )
                return {"session_id": session_id, "question": {"id": next_question_id, "text": transition_text}}
            else:
                return {"session_id": session_id, "summary": generate_summary(session)}
        else:
            return {"session_id": session_id, "summary": generate_summary(session)}

    # If not complete, get the next question
    next_question_id = current_question_list[next_index]
    next_question_data = get_question(next_question_id)
    
    transition_text = generate_transition(
        feedback=evaluation['feedback'],
        next_question=next_question_data['question_text']
    )
    
    return {
        "session_id": session_id,
        "question": {"id": next_question_id, "text": transition_text},
        "previous_answer_feedback": evaluation['feedback']
    }

def generate_summary(session):
    history = session['history']
    if not history:
        return {"overall_score": 0, "strengths": [], "areas_for_improvement": [], "detailed_feedback": "No questions were answered."}

    total_score = sum(h['evaluation']['average_score'] for h in history)
    overall_score = round(total_score / len(history), 2)
    
    strengths = [h['question_text'] for h in history if h['evaluation']['average_score'] >= 4.0]
    areas_for_improvement = [h['question_text'] for h in history if h['evaluation']['average_score'] < 3.0]
    
    detailed_feedback = "Performance Summary:\n"
    for item in history:
        detailed_feedback += f"- Q: {item['question_text']}\n  - Score: {item['evaluation']['average_score']}/5\n  - Feedback: {item['evaluation']['feedback']}\n"
        
    return {
        "overall_score": overall_score,
        "strengths": strengths,
        "areas_for_improvement": areas_for_improvement,
        "detailed_feedback": detailed_feedback
    }