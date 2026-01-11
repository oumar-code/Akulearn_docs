"""
Pydantic schemas for authentication API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import re


# ============================================================================
# Request Schemas
# ============================================================================

class UserRegister(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=255)
    display_name: Optional[str] = Field(None, max_length=100)
    target_exam: Optional[str] = Field(None, max_length=50)
    target_subjects: Optional[List[str]] = None
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password meets strength requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('target_exam')
    def validate_exam(cls, v):
        """Validate target exam is from allowed list."""
        if v and v not in ['WAEC', 'NECO', 'JAMB', 'OTHER']:
            raise ValueError('Target exam must be WAEC, NECO, JAMB, or OTHER')
        return v


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str
    device_info: Optional[str] = None


class TokenRefresh(BaseModel):
    """Token refresh request."""
    refresh_token: str


class EmailVerificationRequest(BaseModel):
    """Email verification request."""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        """Validate password meets strength requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v


class UserUpdate(BaseModel):
    """User profile update request."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    display_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    target_exam: Optional[str] = Field(None, max_length=50)
    target_subjects: Optional[List[str]] = None


# ============================================================================
# Response Schemas
# ============================================================================

class TokenResponse(BaseModel):
    """Token response after login/register."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class UserResponse(BaseModel):
    """User profile response."""
    id: int
    email: str
    full_name: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    target_exam: Optional[str]
    target_subjects: Optional[List[str]]
    email_verified: bool
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility


class RegisterResponse(BaseModel):
    """Registration success response."""
    user: UserResponse
    tokens: TokenResponse
    message: str = "Registration successful. Please verify your email."


class LoginResponse(BaseModel):
    """Login success response."""
    user: UserResponse
    tokens: TokenResponse
    message: str = "Login successful"


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response."""
    message: str
    detail: Optional[str] = None
    error_code: Optional[str] = None


class UserStatsResponse(BaseModel):
    """Public user statistics."""
    user_id: int
    display_name: str
    avatar_url: Optional[str]
    total_questions: int = 0
    total_points: int = 0
    accuracy: float = 0.0
    rank: Optional[int] = None


# ============================================================================
# Internal Schemas
# ============================================================================

class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: int  # user_id
    email: str
    exp: datetime
    iat: datetime
    type: str  # "access" or "refresh"


class OTPData(BaseModel):
    """OTP data for email verification."""
    user_id: int
    email: str
    otp: str
    expires_at: datetime
