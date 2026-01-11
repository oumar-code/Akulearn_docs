"""
Authentication API endpoints for Phase 5.
Handles user registration, login, logout, token refresh, email verification, and password reset.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import json

from ..database.db_config import get_db
from ..database.auth_models import User
from ..services.auth_service import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from ..schemas.auth_schemas import (
    UserRegister, UserLogin, TokenRefresh, EmailVerificationRequest,
    ForgotPasswordRequest, ResetPasswordRequest, UserUpdate,
    RegisterResponse, LoginResponse, TokenResponse, UserResponse,
    MessageResponse, ErrorResponse, UserStatsResponse
)
from ..middleware.auth_middleware import (
    get_auth_service, get_current_user, get_current_active_user,
    get_current_verified_user, check_rate_limit
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
user_router = APIRouter(prefix="/api/users", tags=["Users"])


# ============================================================================
# Helper Functions
# ============================================================================

def user_to_response(user: User) -> UserResponse:
    """Convert User model to UserResponse schema."""
    target_subjects = None
    if user.target_subjects:
        try:
            target_subjects = json.loads(user.target_subjects)
        except:
            target_subjects = []
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        target_exam=user.target_exam,
        target_subjects=target_subjects,
        email_verified=user.email_verified,
        is_active=user.is_active,
        created_at=user.created_at,
        last_login=user.last_login
    )


# ============================================================================
# Authentication Endpoints
# ============================================================================

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email and password. Password must be at least 8 characters with uppercase, lowercase, and number."
)
async def register(
    user_data: UserRegister,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user account."""
    # Rate limiting
    check_rate_limit(user_data.email, max_requests=3, window_minutes=5)
    
    try:
        # Register user
        user = auth_service.register_user(user_data)
        
        # Create session and tokens
        device_info = request.headers.get("user-agent")
        ip_address = request.client.host if request.client else None
        access_token, refresh_token = auth_service.create_session(
            user, device_info, ip_address
        )
        
        # Create email verification OTP
        otp = auth_service.create_email_verification(user.id)
        # TODO: Send OTP via email service
        print(f"📧 Email verification OTP for {user.email}: {otp}")
        
        # Prepare response
        tokens = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return RegisterResponse(
            user=user_to_response(user),
            tokens=tokens,
            message="Registration successful. Please check your email for verification code."
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="Authenticate user with email and password. Returns JWT tokens."
)
async def login(
    credentials: UserLogin,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login with email and password."""
    # Rate limiting
    check_rate_limit(credentials.email, max_requests=5, window_minutes=1)
    
    # Authenticate user
    user = auth_service.authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create session and tokens
    device_info = credentials.device_info or request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    access_token, refresh_token = auth_service.create_session(
        user, device_info, ip_address
    )
    
    # Prepare response
    tokens = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return LoginResponse(
        user=user_to_response(user),
        tokens=tokens,
        message="Login successful"
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="User logout",
    description="Invalidate current session and access token."
)
async def logout(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Logout current user."""
    # Token is extracted by get_current_user dependency
    # We need to get the token again to invalidate the session
    from fastapi.security import HTTPBearer
    from fastapi import Request
    
    # This is a workaround - in production, you'd want to pass the token explicitly
    # For now, we'll invalidate all sessions for the user
    count = auth_service.invalidate_all_sessions(current_user.id)
    
    return MessageResponse(
        message=f"Logout successful. {count} session(s) invalidated.",
        success=True
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Generate new access token using refresh token."
)
async def refresh_token(
    token_data: TokenRefresh,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token."""
    new_access_token = auth_service.refresh_access_token(token_data.refresh_token)
    
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=token_data.refresh_token,  # Refresh token stays the same
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify email with OTP",
    description="Verify user email address using 6-digit OTP sent to email."
)
async def verify_email(
    verification: EmailVerificationRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Verify email with OTP."""
    # Rate limiting
    check_rate_limit(verification.email, max_requests=5, window_minutes=5)
    
    # Get user
    user = auth_service.get_user_by_email(verification.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify OTP
    success = auth_service.verify_email(user.id, verification.otp)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    return MessageResponse(
        message="Email verified successfully",
        success=True
    )


@router.post(
    "/resend-verification",
    response_model=MessageResponse,
    summary="Resend verification OTP",
    description="Resend email verification OTP to user's email."
)
async def resend_verification(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Resend verification OTP."""
    if current_user.email_verified:
        return MessageResponse(
            message="Email already verified",
            success=True
        )
    
    # Generate new OTP
    otp = auth_service.create_email_verification(current_user.id)
    # TODO: Send OTP via email service
    print(f"📧 Email verification OTP for {current_user.email}: {otp}")
    
    return MessageResponse(
        message="Verification code sent to your email",
        success=True
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Request password reset link. Token will be sent to email."
)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Request password reset."""
    # Rate limiting
    check_rate_limit(request_data.email, max_requests=3, window_minutes=15)
    
    # Create reset token
    token = auth_service.create_password_reset(request_data.email)
    
    # Always return success (don't reveal if email exists)
    if token:
        # TODO: Send token via email service
        print(f"🔐 Password reset token for {request_data.email}: {token}")
    
    return MessageResponse(
        message="If your email is registered, you will receive a password reset link.",
        success=True
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset password",
    description="Reset password using token from email."
)
async def reset_password(
    reset_data: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Reset password with token."""
    success = auth_service.reset_password(reset_data.token, reset_data.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    return MessageResponse(
        message="Password reset successful. Please login with your new password.",
        success=True
    )


# ============================================================================
# User Profile Endpoints
# ============================================================================

@user_router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Get profile information for currently authenticated user."
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return user_to_response(current_user)


@user_router.put(
    "/me",
    response_model=UserResponse,
    summary="Update user profile",
    description="Update profile information for currently authenticated user."
)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Update user profile."""
    updated_user = auth_service.update_user(current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_to_response(updated_user)


@user_router.delete(
    "/me",
    response_model=MessageResponse,
    summary="Delete user account",
    description="Permanently delete user account and all associated data."
)
async def delete_user_account(
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Delete user account."""
    success = auth_service.delete_user(current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return MessageResponse(
        message="Account deleted successfully",
        success=True
    )


@user_router.get(
    "/{user_id}/stats",
    response_model=UserStatsResponse,
    summary="Get public user statistics",
    description="Get public statistics for any user (for leaderboards, etc.)."
)
async def get_user_stats(
    user_id: int,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get public user statistics."""
    user = auth_service.get_user_by_id(user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # TODO: Get actual stats from progress tracking
    # For now, return placeholder data
    return UserStatsResponse(
        user_id=user.id,
        display_name=user.display_name or "Anonymous",
        avatar_url=user.avatar_url,
        total_questions=0,
        total_points=0,
        accuracy=0.0,
        rank=None
    )
