import React from 'react';

const SummaryReport = ({ summary, onRestart }) => {
  if (!summary) {
    return (
      <div className="text-center p-8 bg-slate-800 rounded-xl">
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
        <p className={`text-7xl font-bold ${getScoreColor(summary.overall_score)}`}>
          {summary.overall_score.toFixed(1)}<span className="text-4xl text-slate-400">/5</span>
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-8">
        <div className="bg-slate-900/50 p-6 rounded-lg">
          <h3 className="text-xl font-semibold mb-4 text-green-400">✅ Strengths</h3>
          {summary.strengths?.length > 0 ? (
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              {summary.strengths.map((strength, index) => (
                <li key={index}>{strength}</li>
              ))}
            </ul>
          ) : <p className="text-slate-400">No specific strengths identified in this session.</p>}
        </div>

        <div className="bg-slate-900/50 p-6 rounded-lg">
          <h3 className="text-xl font-semibold mb-4 text-yellow-400">🔍 Areas for Improvement</h3>
          {summary.areas_for_improvement?.length > 0 ? (
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              {summary.areas_for_improvement.map((area, index) => (
                <li key={index}>{area}</li>
              ))}
            </ul>
          ) : <p className="text-slate-400">Looks good! No major areas for improvement noted.</p>}
        </div>
      </div>

      <div className="bg-slate-900/50 p-6 rounded-lg">
        <h3 className="text-xl font-semibold mb-4 text-slate-200">Detailed Feedback</h3>
        <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">{summary.detailed_feedback}</p>
      </div>

      <div className="text-center mt-8">
        <button
          onClick={onRestart}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-transform transform hover:scale-105"
        >
          Try Again
        </button>
      </div>
    </div>
  );
};

export default SummaryReport;