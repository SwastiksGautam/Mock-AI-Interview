from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import csv
import os
import json
from datetime import datetime

# ------------------- App Setup -------------------
app = FastAPI()

origins = [
    "https://mock-ai-interview-psi.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Models -------------------
class StartRequest(BaseModel):
    candidate_name: str = "Anonymous"

class AnswerRequest(BaseModel):
    session_id: str
    question_index: int
    answer: str
    evaluation_score: float
    feedback: str

# ------------------- Storage -------------------
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

SESSIONS_FILE = "sessions.json"

# Load sessions from file if exists
if os.path.exists(SESSIONS_FILE):
    with open(SESSIONS_FILE, "r") as f:
        active_sessions = json.load(f)
else:
    active_sessions = {}

# Helper function to save sessions to disk
def save_sessions():
    with open(SESSIONS_FILE, "w") as f:
        json.dump(active_sessions, f, indent=2, default=str)

# ------------------- Routes -------------------
@app.post("/start")
def start_interview(request: StartRequest):
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "candidate_name": request.candidate_name,
        "start_time": datetime.now().isoformat(),
        "last_question_index": -1  # no question answered yet
    }
    save_sessions()  # persist session

    # Create CSV file for storing answers
    csv_file = os.path.join(RESULTS_DIR, f"{session_id}.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question_index", "answer", "evaluation_score", "feedback"])
        writer.writeheader()

    first_question = {"text": "What is the keyboard shortcut to lock a cell reference in Excel?"}

    return {"session_id": session_id, "question": first_question}


@app.post("/answer")
def submit_answer(payload: AnswerRequest):
    # Handle invalid session: create new session automatically
    if payload.session_id not in active_sessions:
        new_session_id = str(uuid.uuid4())
        active_sessions[new_session_id] = {
            "candidate_name": "Anonymous",
            "start_time": datetime.now().isoformat(),
            "last_question_index": -1
        }
        save_sessions()

        # create new CSV file
        csv_file = os.path.join(RESULTS_DIR, f"{new_session_id}.csv")
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["question_index", "answer", "evaluation_score", "feedback"])
            writer.writeheader()

        return {
            "error": "Invalid session ID. Started new session automatically.",
            "new_session_id": new_session_id,
            "question": {"text": "What is the keyboard shortcut to lock a cell reference in Excel?"}
        }

    session_id = payload.session_id
    csv_file = os.path.join(RESULTS_DIR, f"{session_id}.csv")
    if not os.path.exists(csv_file):
        raise HTTPException(status_code=500, detail="Session file missing. Please restart.")

    # store answer
    with open(csv_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question_index", "answer", "evaluation_score", "feedback"])
        writer.writerow({
            "question_index": payload.question_index,
            "answer": payload.answer,
            "evaluation_score": payload.evaluation_score,
            "feedback": payload.feedback
        })

    # Update session
    active_sessions[session_id]["last_question_index"] = payload.question_index
    save_sessions()  # persist updated session

    # For demo, send next question or summary
    next_question_index = payload.question_index + 1
    if next_question_index >= 5:  # max 5 questions per session
        return {"summary": {
            "total_questions": next_question_index,
            "overall_score": round(payload.evaluation_score, 1),
            "strengths": ["Good understanding of Excel basics"],
            "areas_for_improvement": ["Answer with more examples"],
            "detailed_feedback": payload.feedback
        }}

    next_question_text = f"Question {next_question_index + 1}: Example Excel question here."
    return {"question": {"text": next_question_text}}
