// App.jsx - React frontend for ClairOS AI Handoff Assistant
import React, { useState, useEffect } from 'react';
import { Upload, FileText, MessageSquare, AlertTriangle, CheckCircle, Loader, ChevronRight, ThumbsUp, ThumbsDown, Flag, XCircle } from 'lucide-react';

function App() {
  const [viewMode, setViewMode] = useState('manager');
  const [activeTab, setActiveTab] = useState('upload');
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Shared state
  const [file, setFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [docId, setDocId] = useState('');
  const [piiResults, setPiiResults] = useState(null);
  const [briefContent, setBriefContent] = useState('');
  const [confidence, setConfidence] = useState(0);
  const [sources, setSources] = useState([]);
  const [ingestionStatus, setIngestionStatus] = useState(null);
  // null = no file uploaded
  // 'started' = mbox uploaded, ingestion running
  // 'done' = ingestion complete
  // 'failed' = ingestion failed
  // 'not_applicable' = txt file, no ingestion needed

  // Manager state
  const [approvalItems, setApprovalItems] = useState([]);

  // Employee/Chat state
  const [query, setQuery] = useState('');
  const [queryHistory, setQueryHistory] = useState([]);

  // ── Polling: check ingestion status every 10s until done ──
  useEffect(() => {
    if (!docId || ingestionStatus !== 'started') return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/ingestion-status/${docId}`);
        const data = await res.json();

        if (data.status === 'done') {
          setIngestionStatus('done');
          if (data.brief) {
            setBriefContent(data.brief);
            setConfidence(data.confidence || 0);
          }
          fetchApprovalItems();
          clearInterval(interval);
        } else if (data.status === 'failed') {
          setIngestionStatus('failed');
          clearInterval(interval);
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    }, 10000);

    return () => clearInterval(interval);
  }, [docId, ingestionStatus]);

  // ── Auto-dismiss green banner 5 minutes after ingestion completes ──
  useEffect(() => {
    if (ingestionStatus !== 'done') return;
    const timer = setTimeout(() => setIngestionStatus('dismissed'), 5 * 60 * 1000);
    return () => clearTimeout(timer);
  }, [ingestionStatus]);

  // ── File upload ──
  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    setProcessing(true);
    setBriefContent('');
    setIngestionStatus(null);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);

      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      setPiiResults(data.pii);
      setDocId(data.doc_id);
      setSources(data.sources);
      setProcessing(false);
      setActiveTab('review');

      if (data.ingestion === 'started') {
        // mbox file — ingestion running, no brief yet
        setIngestionStatus('started');
        setBriefContent('');
      } else {
        // txt file — brief available immediately
        setIngestionStatus('not_applicable');
        setBriefContent(data.summary);
        setConfidence(data.confidence);
        fetchApprovalItems();
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading file. Make sure backend is running!');
      setProcessing(false);
    }
  };

  const fetchApprovalItems = async () => {
    try {
      const response = await fetch(`${API_URL}/approval-items`);
      const data = await response.json();
      setApprovalItems(data.items || []);
    } catch (error) {
      console.error('Error fetching approval items:', error);
    }
  };

  const handleApproval = async (itemId, approved, flagged = false) => {
    try {
      const formData = new FormData();
      formData.append('item_id', itemId);
      formData.append('approved', approved);
      formData.append('flagged', flagged);
      await fetch(`${API_URL}/approve-item`, { method: 'POST', body: formData });
      fetchApprovalItems();
    } catch (error) {
      console.error('Approval error:', error);
    }
  };

  const handleQuery = async () => {
    if (!query.trim() || !docId) return;
    setProcessing(true);
    try {
      const formData = new FormData();
      formData.append('question', query);
      formData.append('doc_id', docId);
      const response = await fetch(`${API_URL}/query`, { method: 'POST', body: formData });
      const data = await response.json();
      const uniqueSources = data.sources.filter((s, idx, arr) =>
        arr.findIndex(x => x.name === s.name) === idx
      )
      setQueryHistory([...queryHistory, {
        question: query,
        answer: data.answer,
        confidence: data.confidence,
        sources: uniqueSources
      }]);
      
      setQuery('');
      setProcessing(false);
    } catch (error) {
      console.error('Query error:', error);
      alert('Error querying. Make sure backend is running!');
      setProcessing(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setDocId('');
    setPiiResults(null);
    setBriefContent('');
    setQueryHistory([]);
    setApprovalItems([]);
    setIngestionStatus(null);
    setActiveTab('upload');
  };

  // ── Ingestion status banner (reused in both views) ──
  const IngestionBanner = () => {
    if (!file) return null;
    if (activeTab === 'chat') return null;
    if (ingestionStatus === 'dismissed') return null;
    if (ingestionStatus === 'started') return (
      <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-4 flex items-center gap-3">
        <Loader className="w-5 h-5 text-yellow-600 animate-spin flex-shrink-0" />
        <div>
          <p className="font-medium text-yellow-800">Indexing email archive...</p>
          <p className="text-sm text-yellow-700">This may take 30–90 minutes. The handoff brief will appear automatically when ready.</p>
        </div>
      </div>
    );
    if (ingestionStatus === 'done') return (
      <div className="bg-green-50 border border-green-300 rounded-lg p-4 flex items-center gap-3">
        <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
        <p className="font-medium text-green-800">Email archive indexed! Handoff brief is ready.</p>
      </div>
    );
    if (ingestionStatus === 'failed') return (
      <div className="bg-red-50 border border-red-300 rounded-lg p-4 flex items-center gap-3">
        <XCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
        <p className="font-medium text-red-800">Ingestion failed. Please try uploading again.</p>
      </div>
    );
    return null;
  };

  const isQueryDisabled = processing || !docId || ingestionStatus === 'started';

  // ── Manager View ──
  if (viewMode === 'manager') {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-600">C</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold">Trunq.io: AI Handoff Assistant</h1>
                <p className="text-blue-100 text-sm">Private Knowledge Transfer | SOC 2 Compliant | Institutional Memory Platform</p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-medium">Adam Han</p>
              <p className="text-sm text-blue-100">Manager</p>
            </div>
          </div>
        </div>

        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex gap-8">
              <button
                onClick={() => setActiveTab('upload')}
                className={`py-4 px-2 border-b-2 transition flex items-center gap-2 ${activeTab === 'upload' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-600 hover:text-gray-900'}`}
              >
                <Upload className="w-4 h-4" />
                Data Ingestion
              </button>
              <button
                onClick={() => setActiveTab('review')}
                className={`py-4 px-2 border-b-2 transition flex items-center gap-2 ${activeTab === 'review' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-600 hover:text-gray-900'}`}
              >
                <FileText className="w-4 h-4" />
                Review Draft
                {approvalItems.filter(i => i.approved === null).length > 0 && (
                  <span className="bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {approvalItems.filter(i => i.approved === null).length}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 py-8">
          {activeTab === 'upload' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Data Ingestion & Processing</h2>
                <p className="text-gray-600">Upload employee documentation for handoff brief generation</p>
              </div>

              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-lg font-semibold mb-4">New Handoff Creation</h3>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Departing Employee</label>
                    <input type="text" defaultValue="Jeff Dasovich" className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Incoming Employee</label>
                    <input type="text" defaultValue="Alex Thompson" className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                  </div>
                </div>

                <label className="block text-sm font-medium text-gray-700 mb-2">Upload Email Export</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition cursor-pointer">
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    className="hidden"
                    id="file-upload"
                    accept=".txt,.pdf,.doc,.docx,.mbox"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                    <p className="text-gray-700 mb-1">Drop file or click to browse</p>
                    <p className="text-sm text-gray-500">Supports .txt, .pdf, .doc, .docx, .mbox files</p>
                  </label>
                </div>

                {file && !processing && (
                  <div className="mt-4 flex items-center gap-2 text-green-600">
                    <CheckCircle className="w-5 h-5" />
                    <span>{file.name} uploaded successfully</span>
                  </div>
                )}
                {processing && (
                  <div className="mt-4 flex items-center gap-2 text-blue-600">
                    <Loader className="w-5 h-5 animate-spin" />
                    <span>Processing document with AI...</span>
                  </div>
                )}
              </div>

              <IngestionBanner />

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex gap-3">
                <FileText className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-blue-900">
                  All uploaded data is encrypted. PII and sensitive content are automatically filtered.
                  Only manager-approved content will be included in the final handoff brief.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'review' && (
            <div className="space-y-6">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Draft Handoff Brief Review</h2>
                  <p className="text-gray-600">Review and approve AI-generated content</p>
                </div>
                <button onClick={handleReset} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                  Export Final Brief
                </button>
              </div>

              <IngestionBanner />

              {piiResults && piiResults.detected.length > 0 && (
                <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded flex gap-3">
                  <AlertTriangle className="w-6 h-6 text-yellow-600 flex-shrink-0" />
                  <div>
                    <h3 className="font-semibold text-yellow-900">PII Detected & Redacted</h3>
                    <p className="text-sm text-yellow-700 mt-1">Found: {piiResults.detected.join(', ')} ({piiResults.redacted_count} items)</p>
                  </div>
                </div>
              )}

              {!briefContent && ingestionStatus !== 'started' && (
                <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
                  <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">No documents uploaded yet. Go to Data Ingestion to upload files.</p>
                </div>
              )}

              {briefContent && (
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold">Generated Handoff Brief</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${confidence >= 0.8 ? 'bg-green-100 text-green-700' : confidence >= 0.6 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'}`}>
                        {(confidence * 100).toFixed(0)}% Confidence
                      </span>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => handleApproval('1', true)} className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition">
                        <CheckCircle className="w-4 h-4" /> Approve
                      </button>
                      <button onClick={() => handleApproval('1', false)} className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition">
                        <XCircle className="w-4 h-4" /> Reject
                      </button>
                      <button onClick={() => handleApproval('1', null, true)} className="flex items-center gap-2 px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition">
                        <Flag className="w-4 h-4" /> Flag Sensitive
                      </button>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded whitespace-pre-line text-gray-700 mb-4">{briefContent}</div>
                  {sources.length > 0 && (
                    <div className="border-t pt-4">
                      <p className="text-sm text-gray-600 mb-2">Sources:</p>
                      <div className="flex flex-wrap gap-2">
                        {sources.map((source, idx) => (
                          <span key={idx} className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm">
                            📄 {source.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        <button onClick={() => { setViewMode('employee'); setActiveTab('brief'); }} className="fixed bottom-6 right-6 px-6 py-3 bg-gray-900 text-white rounded-lg shadow-lg hover:bg-gray-800 transition flex items-center gap-2">
          Switch to Employee View <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    );
  }

  // ── Employee View ──
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center">
              <span className="text-2xl font-bold text-blue-600">C</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold">ClairOS AI Handoff Assistant</h1>
              <p className="text-blue-100 text-sm">Institutional Memory Platform</p>
            </div>
          </div>
          <div className="text-right">
            <p className="font-medium">Alex Thompson</p>
            <p className="text-sm text-blue-100">New Employee - Project Manager</p>
          </div>
        </div>
      </div>

      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex gap-8">
            <button onClick={() => setActiveTab('brief')} className={`py-4 px-2 border-b-2 transition flex items-center gap-2 ${activeTab === 'brief' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-600 hover:text-gray-900'}`}>
              <FileText className="w-4 h-4" /> Handoff Brief
            </button>
            <button onClick={() => setActiveTab('chat')} className={`py-4 px-2 border-b-2 transition flex items-center gap-2 ${activeTab === 'chat' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-600 hover:text-gray-900'}`}>
              <MessageSquare className="w-4 h-4" /> Ask Questions
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'brief' && (
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-2xl font-bold mb-4">Employee Handoff Brief</h2>

            <IngestionBanner />

            {!briefContent && ingestionStatus !== 'started' && (
              <div className="text-center py-12">
                <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">Your manager will provide access to your handoff brief soon.</p>
              </div>
            )}

            {briefContent && (
              <div className="space-y-6 mt-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><span className="text-gray-600">Approved by:</span> Adam Han</div>
                    <div><span className="text-gray-600">Date:</span> {new Date().toLocaleDateString()}</div>
                    <div><span className="text-gray-600">Document:</span> {docId}</div>
                    <div><span className="text-gray-600">Confidence:</span> {(confidence * 100).toFixed(0)}%</div>
                  </div>
                </div>
                <div className="bg-gray-50 p-6 rounded whitespace-pre-line text-gray-700">{briefContent}</div>
                {sources.length > 0 && (
                  <div className="border-t pt-4">
                    <p className="text-sm text-gray-600 mb-2">Sources:</p>
                    <div className="flex flex-wrap gap-2">
                      {sources.map((source, idx) => (
                        <span key={idx} className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm">📄 {source.name}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="bg-white rounded-lg shadow-sm border p-6 h-[calc(100vh-300px)] flex flex-col">
            <div className="mb-4 space-y-3">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-900">All responses are based on manager-approved documentation and include source citations.</p>
              </div>
              <IngestionBanner />
            </div>

            <div className="flex-1 overflow-y-auto mb-4 space-y-4">
              {!docId && (
                <div className="text-center py-12">
                  <MessageSquare className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">Upload a document first to start asking questions.</p>
                </div>
              )}

              {queryHistory.map((item, idx) => (
                <div key={idx} className="space-y-4">
                  <div className="flex justify-end">
                    <div className="bg-blue-50 rounded-lg p-4 max-w-[70%]">
                      <p className="text-gray-900">{item.question}</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center flex-shrink-0">
                      <span className="text-white text-sm">AI</span>
                    </div>
                    <div className="flex-1 max-w-[70%]">
                      <div className="bg-white border rounded-lg p-4">
                        <p className="text-gray-900 mb-3">{item.answer}</p>
                        {item.sources && item.sources.length > 0 && (
                          <div className="border-t pt-3 mt-3">
                            <p className="text-xs text-gray-600 mb-2">Sources:</p>
                            <div className="flex flex-wrap gap-2">
                              {item.sources.map((source, sidx) => (
                                <span key={sidx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                                  {source.type === 'knowledge_base' ? '🗄️' : '📄'} {source.name}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        <div className="border-t pt-3 mt-3 flex items-center justify-between">
                          <span className={`text-xs ${item.confidence >= 0.8 ? 'text-green-600' : item.confidence >= 0.6 ? 'text-yellow-600' : 'text-red-600'}`}>
                            Confidence: {(item.confidence * 100).toFixed(0)}%
                          </span>
                          <div className="flex gap-1">
                            <button className="p-1 hover:bg-gray-100 rounded"><ThumbsUp className="w-4 h-4 text-gray-600" /></button>
                            <button className="p-1 hover:bg-gray-100 rounded"><ThumbsDown className="w-4 h-4 text-gray-600" /></button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}

              {processing && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center">
                    <Loader className="w-4 h-4 text-white animate-spin" />
                  </div>
                  <p className="text-sm text-gray-500">Searching documentation...</p>
                </div>
              )}
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !isQueryDisabled && handleQuery()}
                placeholder={ingestionStatus === 'started' ? 'Waiting for indexing to complete...' : 'Ask a question about your role...'}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:text-gray-400"
                disabled={isQueryDisabled}
              />
              <button
                onClick={handleQuery}
                disabled={isQueryDisabled || !query.trim()}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {processing ? <Loader className="w-4 h-4 animate-spin" /> : 'Ask'}
              </button>
            </div>

            {/* <div className="text-center mt-4">
              <button onClick={handleReset} className="text-indigo-600 hover:text-indigo-800 underline">
                Upload New Document
              </button>
            </div>""" 
            Note: Commented out reset button in employee view to simplify UI and avoid confusion. Employee can upload new document from manager view after export.
             */}
            
          </div>
        )}
      </div>

      <button onClick={() => {setViewMode('manager'); setActiveTab('upload');}} className="fixed bottom-6 right-6 px-6 py-3 bg-gray-900 text-white rounded-lg shadow-lg hover:bg-gray-800 transition flex items-center gap-2">
        Switch to Manager View
        <span className="px-2 py-0.5 bg-white text-gray-900 rounded text-xs font-medium">Admin</span>
      </button>
    </div>
  );
}

export default App;