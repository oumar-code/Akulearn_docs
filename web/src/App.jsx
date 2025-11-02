import React, {useState} from 'react';
import ZamfaraNetworkMap from './components/ZamfaraNetworkMap';
import AkuDataInsights from './pages/AkuDataInsights';
import AkuDocsEditor from './pages/AkuDocsEditor';
import AiAssistant from './pages/AiAssistant';

export default function App() {
  const [page, setPage] = useState('dashboard');

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      <header className="bg-white shadow sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-semibold text-blue-600">Aku Workspace</h1>
          <nav className="flex gap-2">
            <button onClick={()=>setPage('dashboard')} className={`p-2 rounded-md hover:bg-gray-100 ${page==='dashboard'?'bg-gray-100':''}`}>Dashboard</button>
            <button onClick={()=>setPage('data')} className={`p-2 rounded-md hover:bg-gray-100 ${page==='data'?'bg-gray-100':''}`}>Data</button>
            <button onClick={()=>setPage('editor')} className={`p-2 rounded-md hover:bg-gray-100 ${page==='editor'?'bg-gray-100':''}`}>Docs</button>
            <button onClick={()=>setPage('assistant')} className={`p-2 rounded-md hover:bg-gray-100 ${page==='assistant'?'bg-gray-100':''}`}>Assistant</button>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-4 grid gap-4 grid-cols-1 md:grid-cols-3">
        <aside className="bg-white rounded-lg p-4 shadow col-span-1 md:col-span-1">
          <h2 className="text-xl font-medium">Workspace</h2>
          <p className="text-sm text-gray-500">Mobile-first, responsive PWA shell — demo components below.</p>
          <div className="mt-4 flex flex-col gap-2">
            <button onClick={()=>setPage('dashboard')} className="text-left p-2 rounded hover:bg-gray-50">Dashboard</button>
            <button onClick={()=>setPage('data')} className="text-left p-2 rounded hover:bg-gray-50">Data Insights</button>
            <button onClick={()=>setPage('editor')} className="text-left p-2 rounded hover:bg-gray-50">Docs Editor</button>
            <button onClick={()=>setPage('assistant')} className="text-left p-2 rounded hover:bg-gray-50">AI Assistant</button>
          </div>
        </aside>

        <section className="bg-white rounded-lg p-4 shadow md:col-span-2">
          {page==='dashboard' && (
            <>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-medium">Network Map</h3>
              </div>
              <div className="h-[60vh]">
                <ZamfaraNetworkMap />
              </div>
            </>
          )}

          {page==='data' && <AkuDataInsights />}
          {page==='editor' && <AkuDocsEditor />}
          {page==='assistant' && <AiAssistant />}
        </section>
      </main>

      <footer className="py-4 text-center text-sm text-gray-500">
        © Aku Platform
      </footer>
    </div>
  );
}
