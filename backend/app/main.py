from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import interview

app = FastAPI()  # <-- Gunicorn looks for this exact name

origins = [
    "http://localhost:3000",
    "https://mock-ai-interview-psi.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "Excel Mock Interviewer Backend Running"}
