# app/services/evaluator.py
import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluate_answer(question_text: str, candidate_answer: str, ideal_answer: str):
    """
    Evaluates a candidate's answer using a detailed prompt and a rubric,
    forcing a JSON output.
    """
    system_prompt = """
    You are an expert Data Analyst and a strict but fair technical interviewer for an advanced Excel position.
    Your task is to evaluate a candidate's answer to a technical question.
    """

    user_prompt = f"""
    Here is the evaluation context:

    1.  **THE QUESTION ASKED:**
        "{question_text}"

    2.  **THE CANDIDATE'S ANSWER:**
        "{candidate_answer}"

    3.  **THE IDEAL, EXPERT-LEVEL ANSWER (for your reference):**
        "{ideal_answer}"

    **EVALUATION INSTRUCTIONS:**
    Based on the context above, evaluate the candidate's answer using the following rubric.
    - **Correctness (1-5):** Is the answer factually correct?
    - **Completeness (1-5):** Did it cover all key aspects from the ideal answer?
    - **Best Practices (1-5):** Did they mention modern, efficient methods?
    - **Clarity (1-5):** Was the explanation clear and well-structured?

    Calculate an average score from your rubric ratings. Provide concise, constructive feedback.

    **OUTPUT FORMAT:**
    Your entire response MUST be a single, valid JSON object. Do not include any text before or after the JSON.
    The JSON object must have these exact keys: "average_score", "feedback", "is_sufficient".
    - "average_score" should be a float between 1.0 and 5.0.
    - "feedback" should be a string containing one paragraph of feedback.
    - "is_sufficient" should be a boolean (true if average_score is 3.5 or higher, otherwise false).

    Example output:
    {{"average_score": 4.5, "feedback": "Excellent explanation. You correctly identified the key components and provided a clear example. To improve, you could also mention its limitations.", "is_sufficient": true}}
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo", # Use a model that supports JSON mode
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # The response is guaranteed to be a valid JSON string
        evaluation = json.loads(response.choices[0].message.content)
        return evaluation

    except Exception as e:
        print(f"AI Evaluation Error: {e}")
        # Return a fallback JSON object in case of an error
        return {"average_score": 2.5, "feedback": "There was an error processing the evaluation.", "is_sufficient": False}

def generate_transition(feedback: str, next_question: str) -> str:
    """
    Generates a natural-sounding transition to the next question.
    """
    prompt = f"""
    You are an AI interviewer. Your goal is to make the conversation flow naturally.
    The candidate just answered a question and their feedback was: "{feedback}"
    The next question you need to ask is: "{next_question}"

    Your task is to generate a short, one-sentence transition that connects the feedback to the next question.
    Examples:
    - "Okay, that makes sense. Let's switch gears a bit. How would you..."
    - "Good explanation. Building on that, can you tell me..."
    - "I see. Let's move on to our next scenario. Imagine you have..."

    Your response should ONLY be the transition and the next question.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Transition Error: {e}")
        return next_question # Fallback to just the question