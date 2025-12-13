# Auth Service for Akulearn Backend
# Handles user registration, login, JWT tokens, and OTP verification

import os
import json
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import hashlib
import re

try:
    from jwt import encode, decode, InvalidTokenError
except ImportError:
    # Fallback for JWT operations (to be installed)
    pass


class AuthService:
    """
    Manages user authentication, JWT tokens, and OTP verification.
    
    For MVP: Uses in-memory storage. Production should use PostgreSQL.
    """
    
    # In-memory user store (replace with DB in production)
    _users_db = {}
    _otp_store = {}  # {email: {"otp": "123456", "expires_at": datetime, "verified": bool}}
    _tokens_blacklist = set()
    
    # Configuration
    JWT_SECRET = os.getenv("JWT_SECRET", "akulearn-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_HOURS = 24
    OTP_EXPIRY_MINUTES = 15
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 (use bcrypt in production)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength.
        
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one digit
        - At least one special character
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character"
        
        return True, None
    
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP."""
        return str(secrets.randbelow(1000000)).zfill(6)
    
    def register(self, email: str, password: str, full_name: str, 
                 phone: Optional[str] = None, exam_board: Optional[str] = None,
                 target_subjects: Optional[list] = None) -> Dict:
        """
        Register a new user.
        
        Args:
            email: User's email address
            password: User's password
            full_name: User's full name
            phone: Optional phone number
            exam_board: Preferred exam board (WAEC, NECO, JAMB)
            target_subjects: List of target subjects
            
        Returns:
            Dict with user_id, message, and verification_token
        """
        # Validate email
        if not self.validate_email(email):
            return {"success": False, "error": "Invalid email format"}
        
        # Check if user already exists
        if email in self._users_db:
            return {"success": False, "error": "Email already registered"}
        
        # Validate password
        is_valid, error_msg = self.validate_password(password)
        if not is_valid:
            return {"success": False, "error": error_msg}
        
        # Create user
        user_id = f"user_{secrets.token_hex(8)}"
        password_hash = self.hash_password(password)
        
        self._users_db[email] = {
            "user_id": user_id,
            "email": email,
            "password_hash": password_hash,
            "full_name": full_name,
            "phone": phone,
            "exam_board": exam_board,
            "target_subjects": target_subjects or [],
            "email_verified": False,
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None
        }
        
        # Generate and store OTP
        otp = self.generate_otp()
        self._otp_store[email] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=self.OTP_EXPIRY_MINUTES),
            "verified": False
        }
        
        return {
            "success": True,
            "user_id": user_id,
            "email": email,
            "message": "Registration successful. Verify your email with OTP.",
            "verification_token": otp  # In production, send via email
        }
    
    def verify_otp(self, email: str, otp: str) -> Dict:
        """Verify OTP for email verification."""
        if email not in self._otp_store:
            return {"success": False, "error": "No OTP found for this email"}
        
        otp_data = self._otp_store[email]
        
        # Check expiry
        if datetime.utcnow() > otp_data["expires_at"]:
            del self._otp_store[email]
            return {"success": False, "error": "OTP expired"}
        
        # Check OTP
        if otp_data["otp"] != otp:
            return {"success": False, "error": "Invalid OTP"}
        
        # Mark as verified
        self._users_db[email]["email_verified"] = True
        del self._otp_store[email]
        
        return {"success": True, "message": "Email verified successfully"}
    
    def resend_otp(self, email: str) -> Dict:
        """Resend OTP to user's email."""
        if email not in self._users_db:
            return {"success": False, "error": "User not found"}
        
        # Generate new OTP
        otp = self.generate_otp()
        self._otp_store[email] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=self.OTP_EXPIRY_MINUTES),
            "verified": False
        }
        
        # In production, send OTP via email service
        # For MVP, return in response (insecure but convenient for testing)
        return {
            "success": True,
            "message": "OTP sent to your email",
            "otp_test": otp  # Remove in production
        }
    
    def login(self, email: str, password: str) -> Dict:
        """
        Login user with email and password.
        
        Returns:
            Dict with access_token, refresh_token, user_id, expires_in
        """
        # Check if user exists
        if email not in self._users_db:
            return {"success": False, "error": "Invalid email or password"}
        
        user = self._users_db[email]
        
        # Check if email is verified
        if not user["email_verified"]:
            return {"success": False, "error": "Email not verified. Please verify first."}
        
        # Check password
        if self.hash_password(password) != user["password_hash"]:
            return {"success": False, "error": "Invalid email or password"}
        
        # Generate tokens
        try:
            access_token = self._generate_access_token(email, user["user_id"])
            refresh_token = self._generate_refresh_token(email, user["user_id"])
        except NameError:
            return {"success": False, "error": "JWT not installed. Install with: pip install PyJWT"}
        
        # Update last login
        user["last_login"] = datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user["user_id"],
            "email": email,
            "full_name": user["full_name"],
            "expires_in": self.JWT_EXPIRY_HOURS * 3600
        }
    
    def _generate_access_token(self, email: str, user_id: str) -> str:
        """Generate JWT access token."""
        payload = {
            "email": email,
            "user_id": user_id,
            "type": "access",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.JWT_EXPIRY_HOURS)
        }
        return encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
    
    def _generate_refresh_token(self, email: str, user_id: str) -> str:
        """Generate JWT refresh token (longer expiry)."""
        payload = {
            "email": email,
            "user_id": user_id,
            "type": "refresh",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        return encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode JWT token."""
        if token in self._tokens_blacklist:
            return {"success": False, "error": "Token has been revoked"}
        
        try:
            payload = decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return {"success": True, "payload": payload}
        except InvalidTokenError as e:
            return {"success": False, "error": f"Invalid token: {str(e)}"}
    
    def refresh_token(self, refresh_token: str) -> Dict:
        """Generate new access token from refresh token."""
        result = self.verify_token(refresh_token)
        if not result["success"]:
            return result
        
        payload = result["payload"]
        if payload.get("type") != "refresh":
            return {"success": False, "error": "Invalid token type"}
        
        email = payload["email"]
        user_id = payload["user_id"]
        
        access_token = self._generate_access_token(email, user_id)
        
        return {
            "success": True,
            "access_token": access_token,
            "expires_in": self.JWT_EXPIRY_HOURS * 3600
        }
    
    def logout(self, token: str) -> Dict:
        """Invalidate a token by adding to blacklist."""
        self._tokens_blacklist.add(token)
        return {"success": True, "message": "Logged out successfully"}
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Get user details by email."""
        if email not in self._users_db:
            return None
        
        user = self._users_db[email].copy()
        # Don't return password hash
        user.pop("password_hash", None)
        return user
    
    def update_user(self, email: str, **kwargs) -> Dict:
        """Update user profile."""
        if email not in self._users_db:
            return {"success": False, "error": "User not found"}
        
        allowed_fields = {"full_name", "phone", "exam_board", "target_subjects"}
        for key, value in kwargs.items():
            if key in allowed_fields:
                self._users_db[email][key] = value
        
        return {"success": True, "message": "Profile updated"}


# Global instance
auth_service = AuthService()
