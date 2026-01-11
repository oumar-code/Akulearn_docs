"""
Authentication service for Phase 5.
Handles user registration, login, JWT tokens, password hashing, and email verification.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets
import random
import json

from ..database.auth_models import User, UserSession, EmailVerification, PasswordReset
from ..schemas.auth_schemas import (
    UserRegister, UserLogin, UserUpdate, TokenPayload, TokenResponse
)

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"  # TODO: Move to environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service for user management and JWT tokens."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========================================================================
    # Password Management
    # ========================================================================
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    # ========================================================================
    # JWT Token Management
    # ========================================================================
    
    @staticmethod
    def create_access_token(user_id: int, email: str) -> str:
        """Create JWT access token."""
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": user_id,
            "email": email,
            "exp": expires,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def create_refresh_token(user_id: int, email: str) -> str:
        """Create JWT refresh token."""
        expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": user_id,
            "email": email,
            "exp": expires,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Optional[TokenPayload]:
        """
        Decode and validate JWT token.
        Returns TokenPayload if valid, None if invalid/expired.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return TokenPayload(
                sub=payload["sub"],
                email=payload["email"],
                exp=datetime.fromtimestamp(payload["exp"]),
                iat=datetime.fromtimestamp(payload["iat"]),
                type=payload["type"]
            )
        except JWTError:
            return None
    
    def create_session(
        self,
        user: User,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Create new user session with access and refresh tokens.
        Returns (access_token, refresh_token).
        """
        # Generate tokens
        access_token = self.create_access_token(user.id, user.email)
        refresh_token = self.create_refresh_token(user.id, user.email)
        
        # Create session record
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        session = UserSession(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address
        )
        
        self.db.add(session)
        self.db.commit()
        
        return access_token, refresh_token
    
    def invalidate_session(self, access_token: str) -> bool:
        """Delete session (logout)."""
        session = self.db.query(UserSession).filter(
            UserSession.access_token == access_token
        ).first()
        
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False
    
    def invalidate_all_sessions(self, user_id: int) -> int:
        """Delete all sessions for a user. Returns count of deleted sessions."""
        count = self.db.query(UserSession).filter(
            UserSession.user_id == user_id
        ).delete()
        self.db.commit()
        return count
    
    # ========================================================================
    # User Management
    # ========================================================================
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def register_user(self, user_data: UserRegister) -> User:
        """
        Register a new user.
        Raises ValueError if email already exists.
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash password
        password_hash = self.hash_password(user_data.password)
        
        # Prepare target_subjects as JSON string
        target_subjects = None
        if user_data.target_subjects:
            target_subjects = json.dumps(user_data.target_subjects)
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=password_hash,
            full_name=user_data.full_name,
            display_name=user_data.display_name or user_data.full_name,
            target_exam=user_data.target_exam,
            target_subjects=target_subjects,
            email_verified=False,
            is_active=True
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        Returns User if credentials are valid, None otherwise.
        """
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user profile."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Update fields
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.display_name is not None:
            user.display_name = user_data.display_name
        if user_data.avatar_url is not None:
            user.avatar_url = user_data.avatar_url
        if user_data.target_exam is not None:
            user.target_exam = user_data.target_exam
        if user_data.target_subjects is not None:
            user.target_subjects = json.dumps(user_data.target_subjects)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user account and all related data."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    # ========================================================================
    # Email Verification (OTP)
    # ========================================================================
    
    @staticmethod
    def generate_otp() -> str:
        """Generate 6-digit OTP."""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def create_email_verification(self, user_id: int) -> str:
        """
        Create email verification OTP.
        Returns the OTP (should be sent via email).
        """
        # Invalidate any existing OTPs for this user
        self.db.query(EmailVerification).filter(
            EmailVerification.user_id == user_id,
            EmailVerification.is_used == False
        ).update({"is_used": True})
        
        # Generate new OTP
        otp = self.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        verification = EmailVerification(
            user_id=user_id,
            otp=otp,
            expires_at=expires_at,
            is_used=False
        )
        
        self.db.add(verification)
        self.db.commit()
        
        return otp
    
    def verify_email(self, user_id: int, otp: str) -> bool:
        """
        Verify email with OTP.
        Returns True if successful, False otherwise.
        """
        verification = self.db.query(EmailVerification).filter(
            EmailVerification.user_id == user_id,
            EmailVerification.otp == otp,
            EmailVerification.is_used == False
        ).first()
        
        if not verification or not verification.is_valid:
            return False
        
        # Mark OTP as used
        verification.is_used = True
        
        # Mark user email as verified
        user = self.get_user_by_id(user_id)
        if user:
            user.email_verified = True
        
        self.db.commit()
        return True
    
    # ========================================================================
    # Password Reset
    # ========================================================================
    
    @staticmethod
    def generate_reset_token() -> str:
        """Generate secure password reset token."""
        return secrets.token_urlsafe(32)
    
    def create_password_reset(self, email: str) -> Optional[str]:
        """
        Create password reset token.
        Returns token if user exists, None otherwise.
        """
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        # Invalidate any existing reset tokens
        self.db.query(PasswordReset).filter(
            PasswordReset.user_id == user.id,
            PasswordReset.is_used == False
        ).update({"is_used": True})
        
        # Generate new token
        token = self.generate_reset_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
            is_used=False
        )
        
        self.db.add(reset)
        self.db.commit()
        
        return token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Reset password with token.
        Returns True if successful, False otherwise.
        """
        reset = self.db.query(PasswordReset).filter(
            PasswordReset.token == token,
            PasswordReset.is_used == False
        ).first()
        
        if not reset or not reset.is_valid:
            return False
        
        # Mark token as used
        reset.is_used = True
        
        # Update user password
        user = self.get_user_by_id(reset.user_id)
        if user:
            user.password_hash = self.hash_password(new_password)
            
            # Invalidate all sessions (force re-login)
            self.invalidate_all_sessions(user.id)
        
        self.db.commit()
        return True
    
    # ========================================================================
    # Token Refresh
    # ========================================================================
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Generate new access token from refresh token.
        Returns new access token if valid, None otherwise.
        """
        # Decode refresh token
        payload = self.decode_token(refresh_token)
        if not payload or payload.type != "refresh":
            return None
        
        # Check if session exists and is valid
        session = self.db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token
        ).first()
        
        if not session or session.is_expired:
            return None
        
        # Get user
        user = self.get_user_by_id(payload.sub)
        if not user or not user.is_active:
            return None
        
        # Generate new access token
        new_access_token = self.create_access_token(user.id, user.email)
        
        # Update session
        session.access_token = new_access_token
        session.last_active = datetime.utcnow()
        self.db.commit()
        
        return new_access_token
    
    # ========================================================================
    # Utilities
    # ========================================================================
    
    def get_current_user_from_token(self, access_token: str) -> Optional[User]:
        """
        Get current user from access token.
        Returns User if token is valid, None otherwise.
        """
        payload = self.decode_token(access_token)
        if not payload or payload.type != "access":
            return None
        
        # Check if session exists
        session = self.db.query(UserSession).filter(
            UserSession.access_token == access_token
        ).first()
        
        if not session:
            return None
        
        # Get user
        user = self.get_user_by_id(payload.sub)
        if not user or not user.is_active:
            return None
        
        # Update last active
        session.last_active = datetime.utcnow()
        self.db.commit()
        
        return user
