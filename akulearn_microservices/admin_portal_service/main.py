"""
Admin Portal Service
Supports user management for administrators and content uploads to the CMS.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os

app = FastAPI(title="Akulearn Admin Portal Service")

# JWT Authentication Middleware
security = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Example: Validate JWT with Auth Service
    auth_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:9000/verify")
    resp = requests.post(auth_url, json={"token": token})
    if resp.status_code != 200 or not resp.json().get("valid"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return resp.json().get("user")

# Vault Secret Fetching
def get_secret(secret_path: str):
    vault_url = os.getenv("VAULT_URL", "http://localhost:8200/v1/secret/data/")
    vault_token = os.getenv("VAULT_TOKEN", "test-token")
    headers = {"X-Vault-Token": vault_token}
    resp = requests.get(f"{vault_url}{secret_path}", headers=headers)
    if resp.status_code == 200:
        return resp.json().get("data", {}).get("data", {})
    return {}

# OPA Policy Enforcement
def check_policy(user: dict, action: str, resource: str):
    opa_url = os.getenv("OPA_URL", "http://localhost:8181/v1/data/akulearn/authz")
    input_data = {"input": {"user": user, "action": action, "resource": resource}}
    resp = requests.post(opa_url, json=input_data)
    if resp.status_code == 200 and resp.json().get("result", {}).get("allow"):
        return True
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied by policy")


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}

# Example protected endpoint
@app.get("/admin/profile")
def get_admin_profile(request: Request, user=Depends(verify_jwt)):
    check_policy(user, "read", "admin_profile")
    secret = get_secret("admin_profile")
    return {"user": user, "profile": secret}
