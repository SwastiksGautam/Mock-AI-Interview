from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./mock_interview.db"  # can be postgres later

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ------------------- Models -------------------
class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True, index=True)
    candidate_name = Column(String)
    start_time = Column(DateTime)
    last_question_index = Column(Integer, default=-1)

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id"))
    question_index = Column(Integer)
    answer = Column(String)
    evaluation_score = Column(Float)
    feedback = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ------------------- App Setup -------------------
app = FastAPI()

origins = ["https://mock-ai-interview-psi.vercel.app", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# ------------------- Request Models -------------------
class StartRequest(BaseModel):
    candidate_name: str = "Anonymous"

class AnswerRequest(BaseModel):
    session_id: str
    question_index: int
    answer: str
    evaluation_score: float
    feedback: str

# ------------------- Routes -------------------
@app.post("/start")
def start_interview(request: StartRequest):
    db = SessionLocal()
    session_id = str(uuid.uuid4())
    new_session = Session(
        session_id=session_id,
        candidate_name=request.candidate_name,
        start_time=datetime.utcnow()
    )
    db.add(new_session)
    db.commit()
    db.close()

    first_question = {"text": "What is the keyboard shortcut to lock a cell reference in Excel?"}
    return {"session_id": session_id, "question": first_question}

@app.post("/answer")
def submit_answer(payload: AnswerRequest):
    db = SessionLocal()
    session_obj = db.query(Session).filter(Session.session_id == payload.session_id).first()

    # Handle invalid session
    if not session_obj:
        db.close()
        return {"error": "Invalid session ID. Please start a new session."}

    # Save answer
    answer = Answer(
        session_id=payload.session_id,
        question_index=payload.question_index,
        answer=payload.answer,
        evaluation_score=payload.evaluation_score,
        feedback=payload.feedback
    )
    db.add(answer)

    # Update last question index
    session_obj.last_question_index = payload.question_index
    db.commit()
    db.close()

    next_question_index = payload.question_index + 1
    if next_question_index >= 5:
        return {"summary": {
            "total_questions": next_question_index,
            "overall_score": round(payload.evaluation_score, 1),
            "strengths": ["Good understanding of Excel basics"],
            "areas_for_improvement": ["Answer with more examples"],
            "detailed_feedback": payload.feedback
        }}

    next_question_text = f"Question {next_question_index + 1}: Example Excel question here."
    return {"question": {"text": next_question_text}}
