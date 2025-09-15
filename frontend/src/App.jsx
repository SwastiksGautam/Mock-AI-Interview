import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

// --- Excel Logo Component ---
const ExcelLogo = () => (
    <svg className="w-10 h-10 text-green-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.375 19.5h17.25..." />
    </svg>
);

// --- Axios API Client ---
const apiClient = axios.create({
    baseURL: 'https://mock-ai-interview-sb08.onrender.com',
    headers: { 'Content-Type': 'application/json' },
});

// --- API Calls ---
const startInterview = async () => {
    try {
        const response = await axios.post(
            "https://mock-ai-interview-sb08.onrender.com/start",
            { candidate_name: "John Doe" } // <-- send JSON
        );
        setSessionId(response.data.session_id);
        setChatHistory([{ sender: "ai", text: response.data.question.text }]);
        setInterviewState("in_progress");
    } catch (err) {
        console.error("Failed to start interview:", err);
        setError("Failed to start the interview. Please try again.");
    }
};


const submitAnswer = async (sessionId, questionIndex, answer) => {
    const response = await apiClient.post('/answer', {
        session_id: sessionId,
        question_index: questionIndex,
        answer,
        evaluation_score: 4.0,
        feedback: "Good answer" // dummy feedback for testing
    });
    return response.data;
};

// --- Chat Interface ---
const ChatInterface = ({ chatHistory, onAnswerSubmit, isLoading }) => {
    const [currentAnswer, setCurrentAnswer] = useState('');
    const chatEndRef = useRef(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatHistory]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!currentAnswer.trim() || isLoading) return;
        onAnswerSubmit(currentAnswer);
        setCurrentAnswer('');
    };

    return (
        <div className="flex flex-col h-[70vh] bg-slate-800 rounded-xl shadow-2xl p-4">
            <div className="flex-grow overflow-y-auto pr-4 space-y-6">
                {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`flex items-start gap-4 ${msg.sender === 'user' ? 'justify-end' : ''}`}>
                        {msg.sender === 'ai' && <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 flex items-center justify-center font-bold text-slate-900">AI</div>}
                        <div className={`max-w-xl p-4 rounded-xl whitespace-pre-wrap ${msg.sender === 'ai' ? 'bg-slate-700 text-slate-200 rounded-tl-none' : 'bg-blue-600 text-white rounded-br-none'}`}>
                            {msg.text}
                        </div>
                        {msg.sender === 'user' && <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center font-bold">You</div>}
                    </div>
                ))}
                <div ref={chatEndRef} />
            </div>
            <form onSubmit={handleSubmit} className="flex gap-4 mt-4 border-t border-slate-700 pt-4">
                <textarea
                    value={currentAnswer}
                    onChange={(e) => setCurrentAnswer(e.target.value)}
                    placeholder="Type your answer..."
                    disabled={isLoading}
                    rows={3}
                    className="flex-grow bg-slate-700 text-white rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none resize-none disabled:opacity-50"
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) handleSubmit(e); }}
                />
                <button type="submit" disabled={isLoading || !currentAnswer.trim()} className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg transition-transform transform hover:scale-105 disabled:bg-slate-600">
                    {isLoading ? '...' : 'Send'}
                </button>
            </form>
        </div>
    );
};

// --- Summary Report ---
const SummaryReport = ({ summary, onRestart }) => {
    if (!summary) return null;

    const getScoreColor = (score) => (score >= 4 ? 'text-green-400' : score >= 2.5 ? 'text-yellow-400' : 'text-red-400');

    return (
        <div className="p-8 bg-slate-800 rounded-xl shadow-2xl">
            <h2 className="text-3xl font-bold text-center mb-4 text-green-400">Interview Summary</h2>
            <p className="text-center text-slate-400 mb-8">Here's your performance breakdown:</p>
            <div className="text-center mb-8">
                <p className="text-slate-300 text-lg">Overall Score</p>
                <p className={`text-7xl font-bold ${getScoreColor(summary.overall_score || 0)}`}>
                    {summary.overall_score?.toFixed(1) || 'N/A'}<span className="text-4xl text-slate-400">/5</span>
                </p>
            </div>
            <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div className="bg-slate-900/50 p-6 rounded-lg">
                    <h3 className="text-xl font-semibold mb-4 text-green-400">✅ Strengths</h3>
                    {summary.strengths?.length ? <ul className="list-disc list-inside text-slate-300">{summary.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul> : <p className="text-slate-400">No specific strengths identified.</p>}
                </div>
                <div className="bg-slate-900/50 p-6 rounded-lg">
                    <h3 className="text-xl font-semibold mb-4 text-yellow-400">🔍 Areas for Improvement</h3>
                    {summary.areas_for_improvement?.length ? <ul className="list-disc list-inside text-slate-300">{summary.areas_for_improvement.map((a, i) => <li key={i}>{a}</li>)}</ul> : <p className="text-slate-400">No major areas for improvement noted.</p>}
                </div>
            </div>
            <div className="bg-slate-900/50 p-6 rounded-lg mb-8">
                <h3 className="text-xl font-semibold mb-4 text-slate-200">Detailed Feedback</h3>
                <p className="text-slate-300 whitespace-pre-wrap">{summary.detailed_feedback}</p>
            </div>
            <div className="text-center">
                <button onClick={onRestart} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105">Try Again</button>
            </div>
        </div>
    );
};

// --- Main App ---
export default function App() {
    const [interviewState, setInterviewState] = useState('not_started');
    const [sessionId, setSessionId] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [summary, setSummary] = useState(null);
    const [questionIndex, setQuestionIndex] = useState(0);
    const [error, setError] = useState(null);

    const handleStart = async () => {
        setIsLoading(true);
        setError(null);
        setSummary(null);
        setChatHistory([]);
        setQuestionIndex(0);
        try {
            const data = await startInterview();
            setSessionId(data.session_id);
            setChatHistory([{ sender: 'ai', text: data.question.text }]);
            setInterviewState('in_progress');
        } catch {
            setError('Failed to start the interview. Check backend.');
        } finally { setIsLoading(false); }
    };

    const handleAnswerSubmit = async (answer) => {
        setChatHistory(prev => [...prev, { sender: 'user', text: answer }]);
        setIsLoading(true);
        try {
            const data = await submitAnswer(sessionId, questionIndex, answer);

            if (data.error && data.new_session_id) {
                setSessionId(data.new_session_id);
                setChatHistory([{ sender: 'ai', text: data.question.text }]);
                setError('Session expired. Restarted automatically.');
                setQuestionIndex(0);
            } else if (data.summary) {
                setSummary(data.summary);
                setInterviewState('completed');
            } else if (data.question) {
                setChatHistory(prev => [...prev, { sender: 'ai', text: data.question.text }]);
                setQuestionIndex(prev => prev + 1);
            }
        } catch {
            setError('Error submitting your answer.');
        } finally { setIsLoading(false); }
    };

    const renderContent = () => {
        if (error) return <div className="text-center p-6 bg-red-900/50 rounded-lg">{error}</div>;

        switch (interviewState) {
            case 'not_started':
                return (
                    <div className="text-center p-12 bg-slate-800 rounded-xl shadow-lg">
                        <h2 className="text-3xl font-bold mb-4 text-slate-100">AI-Powered Excel Interview</h2>
                        <p className="text-slate-400 mb-8">Test your Excel skills with AI. Click below to start.</p>
                        <button onClick={handleStart} disabled={isLoading} className="bg-green-600 hover:bg-green-700 disabled:bg-slate-600 text-white font-bold py-3 px-8 rounded-lg">{isLoading ? 'Initializing...' : 'Start Interview'}</button>
                    </div>
                );
            case 'in_progress':
                return <ChatInterface chatHistory={chatHistory} onAnswerSubmit={handleAnswerSubmit} isLoading={isLoading} />;
            case 'completed':
                return <SummaryReport summary={summary} onRestart={handleStart} />;
            default: return null;
        }
    };

    return (
        <div className="bg-slate-900 min-h-screen flex flex-col items-center text-white font-sans p-4">
            <div className="w-full max-w-4xl flex flex-col justify-center flex-grow">
                <header className="w-full text-center mb-8">
                    <h1 className="text-4xl font-bold text-green-400 flex items-center justify-center gap-3">
                        <ExcelLogo /> Excel Mock Interviewer
                    </h1>
                </header>
                <main className="w-full">{renderContent()}</main>
            </div>
            <footer className="w-full text-center py-4 text-sm text-slate-500">&copy; {new Date().getFullYear()} Mock Interview Platform</footer>
        </div>
    );
}
