import React, {useEffect, useState} from 'react';
import idb from '../lib/idb';

export default function AkuDocsEditor(){
  const [text, setText] = useState('');
  const [status, setStatus] = useState('');

  useEffect(()=>{
    async function load(){
      const draft = await idb.get('docs-editor-draft');
      if(draft) setText(draft);
    }
    load();
  },[]);

  async function save(){
    await idb.set('docs-editor-draft', text);
    setStatus('Saved locally');
    setTimeout(()=>setStatus(''),2000);
  }

  return (
    <div>
      <h2 className="text-lg font-medium">Docs Editor (offline drafts)</h2>
      <div className="mt-2">
        <textarea className="w-full h-48 p-2 border rounded" value={text} onChange={(e)=>setText(e.target.value)} />
      </div>
      <div className="flex gap-2 mt-2">
        <button onClick={save} className="px-3 py-1 bg-blue-600 text-white rounded">Save draft</button>
        <button onClick={()=>{setText(''); idb.delete('docs-editor-draft');}} className="px-3 py-1 bg-gray-200 rounded">Clear</button>
        <div className="text-sm text-gray-500">{status}</div>
      </div>
    </div>
  );
}
