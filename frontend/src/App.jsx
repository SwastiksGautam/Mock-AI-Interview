import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

// --- Helper Components & API Logic ---

const ExcelLogo = () => (
    <svg className="w-10 h-10 text-green-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125v-1.5c0-.621.504-1.125 1.125-1.125m17.25 0h.008v.008h-.008v-.008zm-17.25 0h.008v.008h-.008v-.008zM12 21.75h.008v.008h-.008v-.008zM12 18h.008v.008h-.008v-.008zM12 14.25h.008v.008h-.008v-.008zM12 10.5h.008v.008h-.008v-.008zM12 6.75h.008v.008h-.008v-.008zM9.75 21.75h.008v.008h-.008v-.008zM9.75 18h.008v.008h-.008v-.008zM9.75 14.25h.008v.008h-.008v-.008zM9.75 10.5h.008v.008h-.008v-.008zM9.75 6.75h.008v.008h-.008v-.008zM7.5 21.75h.008v.008h-.008v-.008zM7.5 18h.008v.008h-.008v-.008zM7.5 14.25h.008v.008h-.008v-.008zM7.5 10.5h.008v.008h-.008v-.008zM7.5 6.75h.008v.008h-.008v-.008zm-3.375 0h.008v.008h-.008v-.008zM14.25 21.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm2.25 15h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm2.25 15h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zm0-3.75h.008v.008h-.008v-.008zM3.375 9.75h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125v-1.5c0-.621.504-1.125 1.125-1.125m17.25 0h.008v.008h-.008v-.008zm-17.25 0h.008v.008h-.008v-.008z" />
    </svg>
);

const apiClient = axios.create({
    baseURL: 'https://mock-ai-interview-sb08.onrender.com',
    headers: { 'Content-Type': 'application/json' },
});

const startInterview = async () => {
    const response = await apiClient.post('/start');
    return response.data;
};

const submitAnswer = async (sessionId, answer) => {
    const response = await apiClient.post('/answer', { session_id: sessionId, answer });
    return response.data;
};

// --- Chat Interface Component ---
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
        <div className="flex flex-col h-[70vh] bg-slate-800 rounded-xl shadow-2xl p-4 animate-fade-in">
            <div className="flex-grow overflow-y-auto pr-4 space-y-6">
                {chatHistory.map((message, index) => (
                    <div key={index} className={`flex items-start gap-4 ${message.sender === 'user' ? 'justify-end' : ''}`}>
                        {message.sender === 'ai' && <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 flex items-center justify-center font-bold text-slate-900">AI</div>}
                        <div className={`max-w-xl p-4 rounded-xl whitespace-pre-wrap ${message.sender === 'ai' ? 'bg-slate-700 text-slate-200 rounded-tl-none' : 'bg-blue-600 text-white rounded-br-none'}`}>{message.text}</div>
                        {message.sender === 'user' && <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center font-bold">You</div>}
                    </div>
                ))}
                {isLoading && chatHistory[chatHistory.length - 1]?.sender === 'user' && (
                    <div className="flex items-start gap-4">
                        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 flex items-center justify-center font-bold text-slate-900">AI</div>
                        <div className="max-w-xl p-4 rounded-xl bg-slate-700 text-slate-400 rounded-tl-none animate-pulse">Evaluating...</div>
                    </div>
                )}
                <div ref={chatEndRef} />
            </div>
            <form onSubmit={handleSubmit} className="flex gap-4 mt-4 border-t border-slate-700 pt-4">
                <textarea
                    value={currentAnswer}
                    onChange={(e) => setCurrentAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    disabled={isLoading}
                    rows="3"
                    className="flex-grow bg-slate-700 text-white rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none resize-none disabled:opacity-50"
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) handleSubmit(e); }}
                />
                <button type="submit" disabled={isLoading || !currentAnswer.trim()} className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg transition-transform transform hover:scale-105 disabled:bg-slate-600 disabled:cursor-not-allowed">
                    {isLoading ? '...' : 'Send'}
                </button>
            </form>
        </div>
    );
};

// --- Summary Report Component ---
const SummaryReport = ({ summary, onRestart }) => {
    if (!summary) {
        return (
            <div className="text-center p-8 bg-slate-800 rounded-xl animate-fade-in">
                <h2 className="text-2xl font-semibold text-yellow-400">Generating your report...</h2>
                <p className="animate-pulse mt-4">Please wait a moment.</p>
            </div>
        );
    }

    const getScoreColor = (score) => {
        if (score >= 4.0) return 'text-green-400';
        if (score >= 2.5) return 'text-yellow-400';
        return 'text-red-400';
    };

    return (
        <div className="p-8 bg-slate-800 rounded-xl shadow-2xl animate-fade-in">
            <h2 className="text-3xl font-bold text-center mb-2 text-green-400">Interview Performance Report</h2>
            <p className="text-center text-slate-400 mb-8">Here's a detailed breakdown of your performance.</p>
            <div className="text-center mb-8">
                <p className="text-slate-300 text-lg">Overall Score</p>
                <p className={`text-7xl font-bold ${getScoreColor(summary?.overall_score || 0)}`}>
                    {summary?.overall_score !== undefined ? summary.overall_score.toFixed(1) : 'N/A'}
                    <span className="text-4xl text-slate-400">/5</span>
                </p>
            </div>
            <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div className="bg-slate-900/50 p-6 rounded-lg">
                    <h3 className="text-xl font-semibold mb-4 text-green-400">✅ Strengths</h3>
                    {summary.strengths?.length > 0
                        ? <ul className="list-disc list-inside space-y-2 text-slate-300">
                            {summary.strengths.map((s, i) => <li key={i}>{s}</li>)}
                        </ul>
                        : <p className="text-slate-400">No specific strengths identified.</p>
                    }
                </div>
                <div className="bg-slate-900/50 p-6 rounded-lg">
                    <h3 className="text-xl font-semibold mb-4 text-yellow-400">🔍 Areas for Improvement</h3>
                    {summary.areas_for_improvement?.length > 0
                        ? <ul className="list-disc list-inside space-y-2 text-slate-300">
                            {summary.areas_for_improvement.map((a, i) => <li key={i}>{a}</li>)}
                        </ul>
                        : <p className="text-slate-400">No major areas for improvement noted.</p>
                    }
                </div>
            </div>
            <div className="bg-slate-900/50 p-6 rounded-lg">
                <h3 className="text-xl font-semibold mb-4 text-slate-200">Detailed Feedback</h3>
                <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">{summary.detailed_feedback}</p>
            </div>
            <div className="text-center mt-8">
                <button onClick={onRestart} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105">
                    Try Again
                </button>
            </div>
        </div>
    );
};

// --- Main App Component ---
function App() {
    const [interviewState, setInterviewState] = useState('not_started');
    const [sessionId, setSessionId] = useState(null);
    const [chatHistory, setChatHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [summary, setSummary] = useState(null);
    const [error, setError] = useState(null);

    const handleStartInterview = async () => {
        setIsLoading(true);
        setError(null);
        setSummary(null);
        setChatHistory([]);
        try {
            const data = await startInterview();
            setSessionId(data.session_id);
            setChatHistory([{ sender: 'ai', text: data.question.text }]);
            setInterviewState('in_progress');
        } catch (err) {
            setError('Failed to start the interview. Please ensure the backend is running and try again.');
        } finally {
            setIsLoading(false);
        }
    };


    const handleAnswerSubmit = async (answer) => {
        setChatHistory(prev => [...prev, { sender: 'user', text: answer }]);
        setIsLoading(true);
        setError(null);

        try {
            const data = await submitAnswer(sessionId, answer);

            // <<< ADD THIS BLOCK AT THE TOP
            if (data.error) {
                if (data.new_session_id) {
                    setSessionId(data.new_session_id);
                    setError("Session was invalid. Restarted automatically.");
                    // Optionally, you can fetch the first question of the new session
                    if (data.question) {
                        setChatHistory(prev => [...prev, { sender: 'ai', text: data.question.text }]);
                    }
                } else {
                    setError(`Backend error: ${data.error}`);
                    setInterviewState('not_started');
                }
                return; // stop further processing
            }
            // <<< END OF BLOCK

            if (data.summary) {
                setSummary(data.summary);
                setInterviewState('completed');
            } else if (data.question) {
                setChatHistory(prev => [...prev, { sender: 'ai', text: data.question.text }]);
            }
        } catch (err) {
            setError('An error occurred. Please try submitting your answer again.');
        } finally {
            setIsLoading(false);
        }
    };



    const renderContent = () => {
        if (error) {
            return <div className="text-center p-8 bg-red-900/50 rounded-lg text-red-300">{error}</div>;
        }
        switch (interviewState) {
            case 'not_started':
                return (
                    <div className="text-center p-12 bg-slate-800 rounded-xl shadow-lg animate-fade-in">
                        <h2 className="text-3xl font-bold mb-4 text-slate-100">AI-Powered Excel Interview</h2>
                        <p className="text-slate-400 mb-8 max-w-prose mx-auto">Test your technical Excel skills with our automated AI interviewer. You'll face a mix of quick-fire and scenario-based questions to assess your proficiency. Click below when you're ready to begin.</p>
                        <button onClick={handleStartInterview} disabled={isLoading} className="bg-green-600 hover:bg-green-700 disabled:bg-slate-600 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105">
                            {isLoading ? 'Initializing...' : 'Start Interview'}
                        </button>
                    </div>
                );
            case 'in_progress':
                return <ChatInterface chatHistory={chatHistory} onAnswerSubmit={handleAnswerSubmit} isLoading={isLoading} />;
            case 'completed':
                return <SummaryReport summary={summary} onRestart={handleStartInterview} />;
            default:
                return null;
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
                <main className="w-full">
                    {renderContent()}
                </main>
            </div>
            <footer className="w-full text-center py-4 text-sm text-slate-500">
                &copy; {new Date().getFullYear()} Mock Interview Platform. All rights reserved.
            </footer>
        </div>
    );
}

export default App;
