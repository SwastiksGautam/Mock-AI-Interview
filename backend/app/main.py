from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import csv
import os
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

# Keep session info in memory for quick validation
active_sessions = {}

# ------------------- Routes -------------------
@app.post("/start")
def start_interview(request: StartRequest):
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "candidate_name": request.candidate_name,
        "start_time": datetime.now().isoformat()
    }

    # create CSV file for storing answers
    csv_file = os.path.join(RESULTS_DIR, f"{session_id}.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question_index", "answer", "evaluation_score", "feedback"])
        writer.writeheader()

    return {"session_id": session_id, "message": "Interview started"}

@app.post("/answer")
def submit_answer(payload: AnswerRequest):
    if payload.session_id not in active_sessions:
        # optional: automatically start new session
        raise HTTPException(status_code=400, detail="Invalid session ID. Please restart the interview.")

    csv_file = os.path.join(RESULTS_DIR, f"{payload.session_id}.csv")
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

    return {"message": "Answer saved successfully"}

@app.get("/result/{session_id}")
def get_result(session_id: str):
    csv_file = os.path.join(RESULTS_DIR, f"{session_id}.csv")
    if not os.path.exists(csv_file):
        raise HTTPException(status_code=404, detail="No result found for this session")

    return {"result_file": f"/{csv_file}"}
