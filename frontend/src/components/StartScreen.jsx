const StartScreen = ({ onStartWritten, onStartVoice }) => (
  <div className="text-center p-12 bg-slate-800 rounded-xl shadow-lg">
    <h2 className="text-3xl font-bold mb-4 text-slate-100">
      AI-Powered Excel Interview
    </h2>
    <p className="text-slate-400 mb-8">
      Test your Excel skills with AI. Choose your interview mode below.
    </p>
    <div className="flex justify-center gap-4">
      <button
        onClick={onStartWritten}
        className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-bold py-3 px-8 rounded-lg"
      >
        Written Interview
      </button>
      <button
        onClick={onStartVoice}
        className="bg-green-600 hover:bg-green-700 disabled:bg-slate-600 text-white font-bold py-3 px-8 rounded-lg"
      >
        Voice Interview
      </button>
    </div>
  </div>
);