# app/services/evaluator.py
import os
import json
import uuid
import io
import openai
from pydantic import BaseModel
from fastapi import UploadFile, HTTPException
from pydub import AudioSegment


# Load the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------
# Data Models
# -------------------------------
class QuestionGenerationOutput(BaseModel):
    id: str
    question_text: str
    ideal_answer: str

# -------------------------------
# Excel Question Generation
# -------------------------------
def generate_excel_question(stage: int, topic: str = "general") -> QuestionGenerationOutput:
    system_prompt = f"""
    You are an expert Data Analyst and a technical interviewer for an advanced Excel position.
    Your task is to generate a difficult and relevant Excel interview question for an advanced user.
    The question should be practical and test core Excel skills.
    For stage 1, the questions should be more foundational. For stage 2, they should be more complex.
    
    The output MUST be a single, valid JSON object with the following keys:
    - "question_text": The Excel interview question.
    - "ideal_answer": A detailed, expert-level answer that explains the solution, including relevant functions or methods.
    
    Example output:
    {{"question_text": "How can you use the VLOOKUP function to return a value from a different worksheet, and what are its limitations?", "ideal_answer": "VLOOKUP can be used by referencing the other sheet... its main limitation is that it can only look up values to the right..."}}
    """
    user_prompt = f"Generate an Excel interview question for Stage {stage}. The topic is {topic}."
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        generated_content = json.loads(response.choices[0].message.content)
        generated_content['id'] = str(uuid.uuid4())
        return QuestionGenerationOutput(**generated_content)
    except Exception as e:
        print(f"AI Question Generation Error: {e}")
        return QuestionGenerationOutput(
            id=str(uuid.uuid4()),
            question_text="What is the difference between INDEX-MATCH and VLOOKUP?",
            ideal_answer="INDEX-MATCH is more flexible than VLOOKUP..."
        )

# -------------------------------
# Evaluate Candidate Answer
# -------------------------------
def evaluate_answer(question_text: str, candidate_answer: str, ideal_answer: str):
    system_prompt = "You are an expert Data Analyst and a strict but fair technical interviewer for an advanced Excel position."
    user_prompt = f"""
    Here is the evaluation context:

    1.  **THE QUESTION ASKED:**
        "{question_text}"

    2.  **THE CANDIDATE'S ANSWER:**
        "{candidate_answer}"

    3.  **THE IDEAL, EXPERT-LEVEL ANSWER (for your reference):**
        "{ideal_answer}"

    **EVALUATION INSTRUCTIONS:**
    Based on the context above, evaluate the candidate's answer using the following rubric:
    - Correctness (1-5)
    - Completeness (1-5)
    - Best Practices (1-5)
    - Clarity (1-5)

    Calculate an average score. Provide concise feedback.

    OUTPUT FORMAT: Single JSON with keys: "average_score", "feedback", "is_sufficient".
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        evaluation = json.loads(response.choices[0].message.content)
        return evaluation
    except Exception as e:
        print(f"AI Evaluation Error: {e}")
        return {"average_score": 2.5, "feedback": "There was an error processing the evaluation.", "is_sufficient": False}

# -------------------------------
# Transition to Next Question
# -------------------------------
def generate_transition(feedback: str, next_question: str) -> str:
    prompt = f"""
    You are an AI interviewer. Candidate feedback: "{feedback}"
    Next question: "{next_question}"
    Generate a short transition connecting the feedback to the next question.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Transition Error: {e}")
        return next_question

# -------------------------------
# Audio Transcription with Whisper
# -------------------------------
def transcribe_audio(audio_file: UploadFile) -> str:
    """
    Transcribes an uploaded audio file.
    """
    temp_dir = "temp_audio"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    temp_filename = f"{temp_dir}/{uuid.uuid4()}-{audio_file.filename}"
    
    try:
        # Read the file content into a bytes object in memory
        file_content = audio_file.file.read()
        
        # Check if the file is empty before proceeding
        if not file_content or os.path.getsize(temp_filename) == 0:
            os.remove(temp_filename)
            return "Voice not recorded" # <-- Returns a specific string instead of raising an error
            
        # Use pydub to load the file from disk and process it
        audio = AudioSegment.from_file(temp_filename, format="webm")
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        
        # Send the new WAV file content to the OpenAI API
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=(audio_file.filename.replace('.webm', '.wav'), wav_io.read(), "audio/wav")
        )
        
        os.remove(temp_filename) # Clean up the temporary file
        return response.text
    
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        print(f"Whisper Transcription Error: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed. Please check your audio format.")

# -------------------------------
# Summary Feedback
# -------------------------------
def generate_summary_feedback(history: list):
    history_text = "\n\n".join([
        f"Question: {item['question_text']}\nAnswer: {item['answer']}\nFeedback: {item['evaluation']['feedback']}\nScore: {item['evaluation']['average_score']}"
        for item in history
    ])
    user_prompt = f"""
    You are an AI interviewer providing a final summary. Based on interview history, generate key strengths and areas for improvement.
    Interview History:
    {history_text}
    Provide output as JSON with keys: "strengths", "areas_for_improvement".
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional technical interviewer."},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"AI Summary Generation Error: {e}")
        return {"strengths": ["Basic understanding of Excel formulas"], "areas_for_improvement": ["Need to improve on advanced features"]}