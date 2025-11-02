import React, {useEffect, useState} from 'react';
import api from '../services/api';
import idb from '../lib/idb';

export default function AkuDataInsights(){
  const [rows, setRows] = useState(null);
  const [loading, setLoading] = useState(false);
  const [offline, setOffline] = useState(!navigator.onLine);

  useEffect(()=>{
    const onOnline = ()=>setOffline(false);
    const onOffline = ()=>setOffline(true);
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    return ()=>{window.removeEventListener('online', onOnline); window.removeEventListener('offline', onOffline)};
  },[]);

  useEffect(()=>{
    async function load(){
      setLoading(true);
      // Try cache first
      const cached = await idb.get('data-insights-cache');
      if(cached){
        setRows(cached.rows);
      }
      // Try network
      try{
        const res = await api.queryDaaS('SELECT date, value FROM demo');
        if(res && res.rows){
          setRows(res.rows);
          await idb.set('data-insights-cache', res);
        }
      }catch(e){
        // network failed; keep cached
        console.warn('DaaS query failed', e);
      }
      setLoading(false);
    }
    load();
  },[]);

  return (
    <div>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium">Data Insights</h2>
        <div className="text-sm text-gray-500">{offline? 'Offline (showing cached)': 'Online'}</div>
      </div>

      <div className="mt-3 bg-white p-3 rounded shadow">
        {loading && <div className="text-sm text-gray-500">Loading…</div>}
        {!loading && !rows && <div className="text-sm text-gray-400">No data available.</div>}
        {rows && (
          <div className="overflow-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-gray-500">
                  <th className="px-2 py-1">Date</th>
                  <th className="px-2 py-1">Value</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i)=> (
                  <tr key={i} className="border-t">
                    <td className="px-2 py-2">{r[0]}</td>
                    <td className="px-2 py-2">{r[1]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
