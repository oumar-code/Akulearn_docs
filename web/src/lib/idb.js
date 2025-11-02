// Tiny IndexedDB helper (promise-based) - minimal wrapper for demo use
const DB_NAME = 'aku-workspace-db';
const DB_VERSION = 1;

function openDB(){
  return new Promise((resolve, reject)=>{
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (ev)=>{
      const db = ev.target.result;
      if(!db.objectStoreNames.contains('kv')){
        db.createObjectStore('kv');
      }
    };
    req.onsuccess = ()=> resolve(req.result);
    req.onerror = ()=> reject(req.error);
  });
}

export async function idbGet(key){
  const db = await openDB();
  return new Promise((resolve, reject)=>{
    const tx = db.transaction('kv','readonly');
    const store = tx.objectStore('kv');
    const r = store.get(key);
    r.onsuccess = ()=> resolve(r.result);
    r.onerror = ()=> reject(r.error);
  });
}

export async function idbSet(key, value){
  const db = await openDB();
  return new Promise((resolve, reject)=>{
    const tx = db.transaction('kv','readwrite');
    const store = tx.objectStore('kv');
    const r = store.put(value, key);
    r.onsuccess = ()=> resolve(r.result);
    r.onerror = ()=> reject(r.error);
  });
}

export async function idbDelete(key){
  const db = await openDB();
  return new Promise((resolve, reject)=>{
    const tx = db.transaction('kv','readwrite');
    const store = tx.objectStore('kv');
    const r = store.delete(key);
    r.onsuccess = ()=> resolve();
    r.onerror = ()=> reject(r.error);
  });
}

export default {get:idbGet,set:idbSet,delete:idbDelete};
