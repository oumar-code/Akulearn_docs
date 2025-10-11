"""
Admin Portal Service
Supports user management for administrators and content uploads to the CMS.
"""
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
import os

from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext

app = FastAPI(title="Akulearn Admin Portal Service")

# Simple in-memory user store
users_db = {}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Endpoint to create initial admin user
@app.post("/create_admin")
def create_admin(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = get_password_hash(user.password)
    return {"msg": "Admin user created"}

# Simple login endpoint
@app.post("/login")
def login(user: UserLogin):
    hashed = users_db.get(user.username)
    if not hashed or not verify_password(user.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # For demo, return a dummy token
    return {"access_token": f"dummy-token-for-{user.username}", "token_type": "bearer"}

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
