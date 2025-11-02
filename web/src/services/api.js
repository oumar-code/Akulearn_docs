const IG_HUB_BASE = import.meta.env.VITE_IG_HUB_BASE || 'http://localhost:8080';
const DAAS_BASE = import.meta.env.VITE_DAAS_BASE || 'http://localhost:8090';

export async function registerSuperHub(adminKey, payload){
  const res = await fetch(`${IG_HUB_BASE}/superhubs/register`, {
    method:'POST',
    headers:{'Content-Type':'application/json','X-API-KEY':adminKey},
    body: JSON.stringify(payload)
  });
  return res.json();
}

export async function publishMetadata(apiKey, payload){
  const res = await fetch(`${IG_HUB_BASE}/metadata/publish`, {
    method:'POST',
    headers:{'Content-Type':'application/json','X-API-KEY':apiKey},
    body: JSON.stringify(payload)
  });
  return res.json();
}

export async function queryDaaS(query, token){
  const res = await fetch(`${DAAS_BASE}/query`, {
    method:'POST',
    headers:{'Content-Type':'application/json','Authorization': `Bearer ${token}`},
    body: JSON.stringify({query})
  });
  return res.json();
}
