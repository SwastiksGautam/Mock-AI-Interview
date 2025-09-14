import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = ({ chatHistory, onAnswerSubmit, isLoading }) => {
  const [currentAnswer, setCurrentAnswer] = useState('');
  const chatEndRef = useRef(null);

  // Automatically scroll to the latest message
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
      {/* Chat History */}
      <div className="flex-grow overflow-y-auto pr-4 space-y-6">
        {chatHistory.map((message, index) => (
          <div key={index} className={`flex items-start gap-4 ${message.sender === 'user' ? 'justify-end' : ''}`}>
            {message.sender === 'ai' && (
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 flex items-center justify-center font-bold text-slate-900">AI</div>
            )}
            <div
              className={`max-w-xl p-4 rounded-xl whitespace-pre-wrap transition-all duration-300 ${message.sender === 'ai'
                  ? 'bg-slate-700 text-slate-200 rounded-tl-none'
                  : 'bg-blue-600 text-white rounded-br-none'
                }`}
            >
              {message.text}
            </div>
            {message.sender === 'user' && (
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center font-bold">You</div>
            )}
          </div>
        ))}
        {isLoading && chatHistory[chatHistory.length - 1]?.sender === 'user' && (
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-500 flex items-center justify-center font-bold text-slate-900">AI</div>
            <div className="max-w-xl p-4 rounded-xl bg-slate-700 text-slate-400 rounded-tl-none animate-pulse">
              Evaluating...
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Form */}
      <div className="mt-4 border-t border-slate-700 pt-4">
        <form onSubmit={handleSubmit} className="flex gap-4">
          <textarea
            value={currentAnswer}
            onChange={(e) => setCurrentAnswer(e.target.value)}
            placeholder="Type your answer here..."
            disabled={isLoading}
            rows="3"
            className="flex-grow bg-slate-700 text-white rounded-lg p-3 focus:ring-2 focus:ring-green-500 focus:outline-none resize-none disabled:opacity-50 transition-colors"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                handleSubmit(e);
              }
            }}
          />
          <button
            type="submit"
            disabled={isLoading || !currentAnswer.trim()}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:bg-slate-600 disabled:cursor-not-allowed disabled:scale-100"
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;