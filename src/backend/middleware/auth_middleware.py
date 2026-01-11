"""
Authentication middleware and dependencies for FastAPI.
Provides JWT token validation and user authentication.
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..database.db_config import get_db
from ..database.auth_models import User
from ..services.auth_service import AuthService

# Security scheme for Swagger UI
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Dependency to get AuthService instance."""
    return AuthService(db)


def get_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract JWT token from Authorization header.
    Expected format: "Bearer <token>"
    """
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_token_from_header),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """
    Get current authenticated user from JWT token.
    Raises HTTPException if token is invalid or user not found.
    
    Use as dependency in protected routes:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    user = auth_service.get_current_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify account is active.
    Raises HTTPException if account is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account"
        )
    
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current user and verify email is verified.
    Raises HTTPException if email not verified.
    """
    if not current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email to continue."
        )
    
    return current_user


def get_optional_current_user(
    authorization: Optional[str] = Header(None),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[User]:
    """
    Get current user if token is provided, otherwise return None.
    Useful for routes that work for both authenticated and anonymous users.
    
    Example:
        @app.get("/questions")
        def get_questions(user: Optional[User] = Depends(get_optional_current_user)):
            # Returns personalized results if user is logged in
            # Returns generic results if user is anonymous
            pass
    """
    if not authorization:
        return None
    
    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    
    try:
        user = auth_service.get_current_user_from_token(token)
        return user
    except Exception:
        return None


# Rate limiting helper (simple in-memory implementation)
class RateLimiter:
    """Simple rate limiter for authentication endpoints."""
    
    def __init__(self):
        self.requests = {}  # {key: [timestamp1, timestamp2, ...]}
    
    def is_allowed(
        self,
        key: str,
        max_requests: int = 5,
        window_minutes: int = 1
    ) -> bool:
        """
        Check if request is allowed under rate limit.
        
        Args:
            key: Unique identifier (e.g., email or IP)
            max_requests: Maximum requests allowed in window
            window_minutes: Time window in minutes
        
        Returns:
            True if allowed, False if rate limit exceeded
        """
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Clean old requests
        if key in self.requests:
            self.requests[key] = [
                ts for ts in self.requests[key] if ts > window_start
            ]
        else:
            self.requests[key] = []
        
        # Check if under limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(
    key: str,
    max_requests: int = 5,
    window_minutes: int = 1
) -> None:
    """
    Check rate limit and raise HTTPException if exceeded.
    
    Usage:
        @app.post("/auth/login")
        def login(credentials: UserLogin):
            check_rate_limit(credentials.email, max_requests=5, window_minutes=1)
            # ... rest of login logic
    """
    if not rate_limiter.is_allowed(key, max_requests, window_minutes):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Please try again in {window_minutes} minute(s)."
        )
