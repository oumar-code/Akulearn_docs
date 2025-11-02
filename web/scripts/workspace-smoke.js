const http = require('http');

async function check(url){
  return new Promise((resolve)=>{
    const req = http.get(url, (res)=>{
      resolve({status: res.statusCode});
    });
    req.on('error', ()=>resolve({status: 0}));
    req.setTimeout(3000, ()=>{req.abort(); resolve({status:0})});
  });
}

(async ()=>{
  console.log('Running workspace smoke checks...');
  const ig = await check('http://127.0.0.1:8080/connectivity/status');
  const daas = await check('http://127.0.0.1:8090/query');
  const web = await check('http://127.0.0.1:5173');

  console.log('IG-Hub status', ig.status);
  console.log('DaaS status', daas.status);
  console.log('Web status', web.status);

  if(ig.status===200 && daas.status===200 && (web.status===200||web.status===0)){
    console.log('Smoke checks passed (note: web may be 0 if dev server not started).');
    process.exit(0);
  }
  console.error('Smoke checks failed.');
  process.exit(2);
})();
const fetch = (...args) => import('node-fetch').then(({default: f}) => f(...args));

async function main(){
  const igHub = process.env.IG_HUB_BASE || 'http://127.0.0.1:8080';
  const daas = process.env.DAAS_BASE || 'http://127.0.0.1:8090';

  console.log('Checking IG-Hub', igHub);
  try{
    const r = await fetch(`${igHub}/connectivity/status`);
    if(!r.ok) throw new Error(`IG-Hub status ${r.status}`);
    console.log('IG-Hub OK', await r.text());
  }catch(e){
    console.error('IG-Hub check failed', e);
    process.exitCode = 2;
    return;
  }

  console.log('Checking DaaS', daas);
  try{
    const r = await fetch(`${daas}/query`, {
      method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({query:'SELECT 1'})
    });
    if(!r.ok) throw new Error(`DaaS status ${r.status}`);
    const j = await r.json();
    console.log('DaaS OK', j && j.rows? `rows=${j.rows.length}` : JSON.stringify(j));
  }catch(e){
    console.error('DaaS check failed', e);
    process.exitCode = 3;
    return;
  }

  console.log('Smoke checks passed');
}

main();
