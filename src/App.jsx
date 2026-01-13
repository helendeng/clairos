import React, { useState } from 'react';
import { Upload, FileText, MessageSquare, AlertTriangle, CheckCircle, Loader } from 'lucide-react';

function App() {
  const [file, setFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [piiResults, setPiiResults] = useState(null);
  const [summary, setSummary] = useState('');
  const [documentContext, setDocumentContext] = useState('');
  const [query, setQuery] = useState('');
  const [queryHistory, setQueryHistory] = useState([]);
  const [docId, setDocId] = useState('');

  // Real file upload - calls backend
  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;
    
    setFile(uploadedFile);
    setProcessing(true);
    setShowResults(false);
    
    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setDocId(data.doc_id);

      // Store results
      setPiiResults(data.pii);
      setSummary(data.summary);
      setDocumentContext(data.summary); // Use summary as context for queries
      setShowResults(true);
      setProcessing(false);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading file. Make sure backend is running on port 8000!');
      setProcessing(false);
    }
  };

  // Real query - calls backend with Ollama
  const handleQuery = async () => {
    if (!query.trim()) return;
    
    setProcessing(true);
    
    try {
      const formData = new FormData();
      formData.append('question', query);
      formData.append('doc_id', docId);
      
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      setQueryHistory([...queryHistory, { question: query, answer: data.answer }]);
      setQuery('');
      setProcessing(false);
    } catch (error) {
      console.error('Query error:', error);
      alert('Error querying. Make sure backend and Ollama are running!');
      setProcessing(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setShowResults(false);
    setPiiResults(null);
    setSummary('');
    setDocumentContext('');
    setQueryHistory([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">ClairOS: AI Transition Assistant</h1>
          <p className="text-gray-600">Privacy-First Data Analysis • SOC 2 Compliant • Zero Data Retention</p>
          <p className="text-sm text-green-600 mt-2">✓ Powered by Local AI Models (Ollama)</p>
        </div>

        {/* Upload Section */}
        {!showResults && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
            <div className="text-center">
              <Upload className="w-16 h-16 text-indigo-500 mx-auto mb-4" />
              <h2 className="text-2xl font-semibold mb-4">Upload Document</h2>
              <p className="text-gray-600 mb-6">Upload files containing sensitive information for secure processing</p>
              
              <label className="inline-block">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  className="hidden"
                  accept=".txt,.pdf,.doc,.docx"
                />
                <span className="bg-indigo-600 text-white px-6 py-3 rounded-lg cursor-pointer hover:bg-indigo-700 transition inline-block">
                  Choose File
                </span>
              </label>
              
              {file && !processing && !showResults && (
                <p className="mt-4 text-green-600 flex items-center justify-center gap-2">
                  <CheckCircle className="w-5 h-5" />
                  {file.name} ready to process
                </p>
              )}
              
              {processing && (
                <div className="mt-4 flex items-center justify-center gap-2 text-indigo-600">
                  <Loader className="w-5 h-5 animate-spin" />
                  Processing with local AI models... This may take 10-30 seconds
                </div>
              )}
            </div>
          </div>
        )}

        {/* Results Section */}
        {showResults && piiResults && (
          <div className="space-y-6">
            {/* PII Detection Alert */}
            {piiResults.detected.length > 0 ? (
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold text-yellow-800">PII Detected & Redacted</h3>
                    <p className="text-sm text-yellow-700 mt-1">
                      Found and redacted: {piiResults.detected.join(', ')}
                    </p>
                    <p className="text-sm text-yellow-700">Total items redacted: {piiResults.redacted_count}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold text-green-800">No PII Detected</h3>
                    <p className="text-sm text-green-700 mt-1">Document appears safe to process</p>
                  </div>
                </div>
              </div>
            )}

            {/* Component 1: Summary Brief */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <FileText className="w-6 h-6 text-indigo-600" />
                <h2 className="text-2xl font-semibold">Document Summary</h2>
              </div>
              <div className="bg-gray-50 p-4 rounded whitespace-pre-line text-gray-700">
                {summary || 'Generating summary...'}
              </div>
            </div>

            {/* Component 2: Query Interface */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <MessageSquare className="w-6 h-6 text-indigo-600" />
                <h2 className="text-2xl font-semibold">Ask Questions</h2>
              </div>

              {/* Query History */}
              {queryHistory.length > 0 && (
                <div className="mb-4 space-y-3 max-h-64 overflow-y-auto">
                  {queryHistory.map((item, idx) => (
                    <div key={idx} className="border-l-4 border-indigo-300 pl-4">
                      <p className="font-medium text-gray-800">Q: {item.question}</p>
                      <p className="text-gray-600 mt-1">A: {item.answer}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Query Input */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !processing && handleQuery()}
                  placeholder="Ask a question about the document..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  disabled={processing}
                />
                <button
                  onClick={handleQuery}
                  disabled={processing || !query.trim()}
                  className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {processing ? (
                    <>
                      <Loader className="w-4 h-4 animate-spin" />
                      Thinking...
                    </>
                  ) : (
                    'Ask'
                  )}
                </button>
              </div>
              
              <p className="text-sm text-gray-500 mt-2">
                Ask anything about the document - powered by local AI
              </p>
            </div>

            {/* Reset Button */}
            <div className="text-center">
              <button
                onClick={handleReset}
                className="text-indigo-600 hover:text-indigo-800 underline"
              >
                Upload New Document
              </button>
            </div>
          </div>
        )}

        {/* Tech Stack Note */}
        <div className="mt-8 bg-white rounded-lg shadow p-4 text-sm text-gray-600">
          <p className="font-semibold mb-2">🔧 Tech Stack:</p>
          <ul className="list-disc list-inside space-y-1 ml-4">
            <li><strong>Frontend:</strong> React + Vite + Tailwind CSS</li>
            <li><strong>Backend:</strong> Python FastAPI (localhost:8000)</li>
            <li><strong>AI:</strong> Ollama (localhost:11434) with llama3.2</li>
            <li><strong>Privacy:</strong> 100% local processing, no data leaves your machine</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;