import React, {useState} from 'react';
import api from '../services/api';

export default function AiAssistant(){
  const [query, setQuery] = useState('');
  const [reply, setReply] = useState(null);
  const [loading, setLoading] = useState(false);

  async function ask(){
    setLoading(true);
    try{
      // For demo we call the DaaS query endpoint and show results as 'assistant' output
      const res = await api.queryDaaS(query);
      setReply(res);
    }catch(e){
      setReply({error: String(e)});
    }
    setLoading(false);
  }

  return (
    <div>
      <h2 className="text-lg font-medium">AI Assistant (demo)</h2>
      <div className="mt-2">
        <input className="w-full p-2 border rounded" placeholder="Ask a question or query" value={query} onChange={(e)=>setQuery(e.target.value)} />
      </div>
      <div className="flex gap-2 mt-2">
        <button onClick={ask} className="px-3 py-1 bg-green-600 text-white rounded">Ask</button>
      </div>
      <div className="mt-3 bg-white p-3 rounded shadow">
        {loading && <div className="text-sm text-gray-500">Thinking…</div>}
        {!loading && reply && (
          <pre className="text-xs text-gray-800">{JSON.stringify(reply, null, 2)}</pre>
        )}
      </div>
    </div>
  );
}
