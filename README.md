📊 Excel Mock Interviewer (AI-Powered)

AI-powered mock interview platform for testing and improving Excel skills.
Built with FastAPI (backend) and React (frontend), it simulates a technical Excel interview, automatically generates questions, evaluates answers, and provides a detailed performance summary with strengths and areas for improvement.

🚀 Features
🚀 Features

🎯 Interactive AI Interview

Stage 1: Foundational MCQs

Stage 2: Advanced open-ended Excel questions

🧠 AI-Powered Question Generation

Dynamic Excel interview questions via OpenAI GPT

Covers shortcuts, formulas, functions, and data management

⚖️ Real-Time Answer Evaluation

Scored (1–5) on correctness, completeness, clarity, and best practices

Concise, AI-driven feedback

🔄 Dynamic Transitions

Natural conversational flow between questions

📊 Performance Summary

Overall score (/5)

Key strengths & improvement areas

Detailed breakdown of each question

💻 Modern UI

React + TailwindCSS for clean design

Chat-like interface with smooth animations

Summary report visualization

🛠️ Tech Stack

Backend

⚡ FastAPI (Python)

🤖 OpenAI GPT (questions, evaluation, transitions, summaries)

🗄 SQLite (prototype session storage)

🌐 CORS-enabled API

Frontend

⚛️ React (Vite/CRA)

📡 Axios (API calls)

🎨 TailwindCSS (UI styling)

⚙️ System Workflow

1️⃣ Start Interview → Backend generates first Excel question
2️⃣ Answer Submission → User submits → AI evaluates (score + feedback)
3️⃣ Stage Transition →

If performance ≥ 3.0/5 after 5 Qs → move to Stage 2 (advanced)

Otherwise → summary & end session
4️⃣ Performance Summary → AI provides strengths, improvement areas, and detailed feedback

📂 Project Structure
📦 Excel-Mock-Interviewer
├── backend/ (FastAPI)
│   ├── app/
│   │   ├── routes/interview.py       # Routes for interview flow
│   │   ├── services/evaluator.py     # AI evaluation & question generation
│   │   ├── services/mock_database.py # Mock dataset
│   ├── main.py                       # FastAPI entrypoint
│
├── frontend/ (React)
│   ├── src/App.js                    # Main React app
│   ├── components/                   # UI components
│   ├── api/                          # Axios API calls
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
POST	/answer	Submit answer & get next question/summary
GET	/	Health check endpoint
📊 Example Flow

AI: "What is the shortcut to lock a cell reference in Excel?"
User: "F4"
AI Feedback: "Correct! F4 cycles between relative and absolute references."
Next Question → …
After 5–10 Qs → Summary Report with Scores & Feedback

📌 Roadmap

 Add voice interview mode (speech-to-text + AI evaluation)

 Expand beyond Excel (SQL, Python, Data Analysis)

 Persistent database (PostgreSQL + ChromaDB for embeddings)

 Deploy with Docker + Vercel/Render
