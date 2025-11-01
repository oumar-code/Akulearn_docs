# IG-Hub Control Panel (example)

This is a small example FastAPI service demonstrating a lightweight IG-Hub control plane used for Super Hub registration and metadata ingestion.

## Endpoints

- POST /superhubs/register
  - Requires admin API key via header `X-API-KEY`.
  - body: { superHubId, countryCode, publicKey }
  - registers a Super Hub and returns an issued SuperHub API key for subsequent publishing.
- POST /metadata/publish
  - Requires SuperHub API key via header `X-API-KEY`.
  - body: { superHubId, datasetId, anonymizedPayload }
  - accepts anonymized metadata uploads from registered Super Hubs.
- GET /connectivity/status
  - returns basic health and counts.

## Running locally

1. python -m venv .venv
2. .\.venv\Scripts\Activate.ps1   # on Windows PowerShell
3. pip install -r requirements.txt
4. uvicorn main:app --reload --port 8080

Environment variables

- `IGHUB_DB_PATH` - path to SQLite DB (default: `/tmp/ig_hub.db`). Use `:memory:` for tests.
- `IGHUB_ADMIN_API_KEY` - admin key required to register Super Hubs. Default in example: `admin-secret-example`.

## Super Hub client demo

Use `client.py` to register and publish (example):

```powershell
python client.py register --admin-key admin-secret-example --id sh-demo --country NG
python client.py publish --api-key <issued-key> --id sh-demo --dataset d1 --payload '{"count":1}'
```

## Notes

- This example shows a simple API key flow and SQLite-backed persistence for prototyping. For production, replace with mutual TLS, OAuth/JWT, hashed keys, proper key rotation, RBAC, and hardened persistent storage.
