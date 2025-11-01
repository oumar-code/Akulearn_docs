from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime
import os
import json

from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from datetime import datetime
import os
import json
import sqlite3
import secrets

app = FastAPI(title="Aku IG-Hub Control Panel (example)")


DB_PATH = os.environ.get('IGHUB_DB_PATH', '/tmp/ig_hub.db')
ADMIN_API_KEY = os.environ.get('IGHUB_ADMIN_API_KEY', 'admin-secret-example')


class SuperHubRegisterRequest(BaseModel):
    superHubId: str = Field(..., description="Unique identifier for the Super Hub")
    countryCode: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    publicKey: str = Field(..., description="Public key for secure communication")


class MetadataPublishRequest(BaseModel):
    superHubId: str
    datasetId: str
    anonymizedPayload: Dict[str, Any]


def get_db_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            superHubId TEXT PRIMARY KEY,
            countryCode TEXT,
            publicKey TEXT,
            apiKey TEXT,
            registeredAt TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            superHubId TEXT,
            datasetId TEXT,
            anonymizedPayload TEXT,
            receivedAt TEXT
        )
        """
    )
    conn.commit()
    conn.close()


@app.on_event('startup')
def startup():
    init_db()


def require_admin_key(x_api_key: Optional[str]):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail='Invalid admin API key')


def validate_superhub_api_key(superHubId: str, x_api_key: Optional[str]) -> bool:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT apiKey FROM registrations WHERE superHubId=?', (superHubId,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    return x_api_key == row['apiKey']


@app.post('/superhubs/register')
def register_superhub(req: SuperHubRegisterRequest, x_api_key: Optional[str] = Header(None)):
    # Admin-only operation: create a registration and return an issued API key for the SuperHub
    require_admin_key(x_api_key)
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM registrations WHERE superHubId=?', (req.superHubId,))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail='SuperHub already registered')
    issued_key = secrets.token_hex(16)
    cur.execute(
        'INSERT INTO registrations(superHubId, countryCode, publicKey, apiKey, registeredAt) VALUES (?,?,?,?,?)',
        (req.superHubId, req.countryCode, req.publicKey, issued_key, datetime.utcnow().isoformat() + 'Z')
    )
    conn.commit()
    conn.close()
    return {'status': 'ok', 'superHubId': req.superHubId, 'apiKey': issued_key}


@app.post('/metadata/publish')
def publish_metadata(req: MetadataPublishRequest, x_api_key: Optional[str] = Header(None)):
    # SuperHub must present its issued API key
    if not validate_superhub_api_key(req.superHubId, x_api_key):
        raise HTTPException(status_code=403, detail='Invalid or missing SuperHub API key')
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO ingestions(superHubId, datasetId, anonymizedPayload, receivedAt) VALUES (?,?,?,?)',
        (req.superHubId, req.datasetId, json.dumps(req.anonymizedPayload), datetime.utcnow().isoformat() + 'Z')
    )
    conn.commit()
    conn.close()
    return {'status': 'accepted', 'datasetId': req.datasetId}


@app.get('/connectivity/status')
def connectivity_status():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as c FROM registrations')
    regs = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) as c FROM ingestions')
    ing = cur.fetchone()['c']
    conn.close()
    return {
        'status': 'ok',
        'registeredSuperHubs': regs,
        'ingestions': ing
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
