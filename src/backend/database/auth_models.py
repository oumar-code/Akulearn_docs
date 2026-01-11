"""
Authentication database models for Phase 5.
Includes User, Session, EmailVerification, and PasswordReset tables.
"""
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import uuid

Base = declarative_base()


class User(Base):
    """User account model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    display_name = Column(String(100))
    avatar_url = Column(String(500))
    
    # Educational preferences
    target_exam = Column(String(50))  # WAEC, NECO, JAMB
    target_subjects = Column(Text)    # JSON array as string
    
    # Account status
    email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_login = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    verifications = relationship("EmailVerification", back_populates="user", cascade="all, delete-orphan")
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.full_name}')>"


class UserSession(Base):
    """Active user session with JWT tokens."""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Tokens
    access_token = Column(String(500), unique=True, nullable=False, index=True)
    refresh_token = Column(String(500), unique=True, nullable=False, index=True)
    
    # Session info
    expires_at = Column(DateTime, nullable=False)
    device_info = Column(Text)  # JSON as string
    ip_address = Column(String(45))
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_active = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"
    
    @property
    def is_expired(self):
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at


class EmailVerification(Base):
    """Email verification OTPs."""
    __tablename__ = "email_verifications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # OTP
    otp = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    # Status
    is_used = Column(Boolean, default=False)
    
    # Timestamp
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="verifications")
    
    def __repr__(self):
        return f"<EmailVerification(id={self.id}, user_id={self.user_id})>"
    
    @property
    def is_expired(self):
        """Check if OTP is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self):
        """Check if OTP is valid (not expired and not used)."""
        return not self.is_expired and not self.is_used


class PasswordReset(Base):
    """Password reset tokens."""
    __tablename__ = "password_resets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Reset token
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    
    # Status
    is_used = Column(Boolean, default=False)
    
    # Timestamp
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="password_resets")
    
    def __repr__(self):
        return f"<PasswordReset(id={self.id}, user_id={self.user_id})>"
    
    @property
    def is_expired(self):
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self):
        """Check if token is valid (not expired and not used)."""
        return not self.is_expired and not self.is_used


# Database initialization helper
def create_tables(engine):
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def drop_tables(engine):
    """Drop all tables from the database."""
    Base.metadata.drop_all(bind=engine)
