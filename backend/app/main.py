from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Import the interview router
from app.routes import interview

load_dotenv()

app = FastAPI()

# The list of origins that are allowed to make requests.
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

# Include the router from the interview module
app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "Excel Mock Interviewer Backend Running"}