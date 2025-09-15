from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os

# You must import the interview module before you can use it.
from app.routes import interview

load_dotenv()

app = FastAPI()

# The list of origins that are allowed to make requests.
# Add your Vercel URL here.
origins = [
    "https://mock-ai-interview-psi.vercel.app",  # Your Vercel frontend URL
    "http://localhost:3000",                     # For local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now that the 'interview' module is imported, this line will work.
app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "Excel Mock Interviewer Backend Running"}