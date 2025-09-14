from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import interview

import os

load_dotenv()

app = FastAPI()

# Retrieve the allowed origins from an environment variable.
# Split the string by comma to get a list of URLs.
# Fallback to an empty list if the variable is not set.
origins_str = os.getenv("ALLOWED_ORIGINS", "")
origins = origins_str.split(",") if origins_str else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "Excel Mock Interviewer Backend Running"}