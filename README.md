📊 Excel Mock Interviewer (AI-Powered)

An AI-powered mock interview platform for testing and improving Excel skills, built with FastAPI (backend) and React (frontend). The system simulates a technical Excel interview, automatically generates questions, evaluates answers using AI, and provides a detailed performance summary with strengths and improvement areas.

🚀 Features

Interactive AI Interview

Stage 1: Foundational MCQs

Stage 2: Advanced open-ended Excel questions

AI-Powered Question Generation

Questions dynamically generated using OpenAI GPT models

Covers Excel shortcuts, formulas, functions, and data management

Real-Time Answer Evaluation

Strict but fair evaluation with scores (1–5)

Feedback on correctness, completeness, clarity, and best practices

Dynamic Transitions

Natural conversational flow between questions with AI-generated transitions

Performance Summary

Overall score out of 5

Key strengths and areas for improvement

Detailed breakdown of each question

Modern UI

Built with React + TailwindCSS

Chat-like interface with smooth animations

Summary report visualization

🛠️ Tech Stack
Backend

FastAPI (Python)

OpenAI GPT (Question generation, evaluation, transitions, summaries)

SQLite (session persistence prototype)

CORS-enabled API

Frontend

React (Vite/CRA)

Axios (API communication)

TailwindCSS (UI styling)

⚙️ System Workflow
1. Start Interview

User begins session → Backend generates first Excel question.

2. Answer Submission

User submits written answer.

AI evaluates response → Scores + Feedback.

3. Stage Transition

If performance ≥ 3.0/5 after 5 Stage 1 questions → move to Stage 2 (advanced).

Otherwise, generate summary and end session.

4. Performance Summary

AI summarizes history → Key strengths & areas for improvement.

Detailed breakdown displayed in frontend summary report.

📂 Project Structure
📦 Excel-Mock-Interviewer
├── backend/ (FastAPI)
│   ├── app/
│   │   ├── routes/interview.py     # Routes for interview flow
│   │   ├── services/evaluator.py   # AI-powered evaluation & question generation
│   │   ├── services/mock_database.py # Mock Q&A dataset
│   ├── main.py                     # FastAPI entrypoint
│
├── frontend/ (React)
│   ├── src/App.js                  # Main React app
│   ├── components/                 # UI components
│   ├── api/                        # Axios API calls
│
└── README.md

⚡ Setup & Installation
Backend (FastAPI)
cd backend
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
export OPENAI_API_KEY="your-openai-api-key"

uvicorn main:app --reload

Frontend (React)
cd frontend
npm install
npm start

🌐 API Endpoints
Method	Endpoint	Description
POST	/start	Start a new interview session
POST	/answer	Submit answer & receive next question or summary
GET	/	Health check endpoint
📊 Example Flow

AI: "What is the shortcut to lock a cell reference in Excel?"

User: "F4"

AI Feedback: "Correct! F4 cycles between relative and absolute references."

Next Question…

After 5–10 Qs → Summary Report with Scores & Feedback

📌 Roadmap

 Add voice interview mode (speech-to-text + AI evaluation)

 Expand topics beyond Excel (SQL, Python, Data Analysis)

 Persistent database (PostgreSQL + ChromaDB for embeddings)

 Deploy with Docker & Vercel/Render

🖼️ Screenshots (Optional)

Start Screen

AI Chat Interface

Performance Summary

🤝 Contributing

PRs are welcome! For major changes, open an issue first to discuss what you’d like to change.

📜 License

MIT License – Free to use and modify.
