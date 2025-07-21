from sqlalchemy import (
    Column, String, Boolean, Enum, ForeignKey, TIMESTAMP, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import enum
import uuid

Base = declarative_base()

class UserRole(enum.Enum):
    super_admin = "super_admin"
    school_admin = "school_admin"
    it_support = "it_support"
    teacher = "teacher"
    student = "student"
    guardian = "guardian"
    government = "government"
    corporation = "corporation"
    ngo_partner = "ngo_partner"

class School(Base):
    __tablename__ = "schools"
    school_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    contact_email = Column(String, unique=True)
    phone_number = Column(String)
    admin_user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    admin_user = relationship("User", back_populates="admin_schools", foreign_keys=[admin_user_id])
    users = relationship("User", back_populates="school")

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.school_id"), nullable=True)
    guardian_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)

    school = relationship("School", back_populates="users", foreign_keys=[school_id])
    admin_schools = relationship("School", back_populates="admin_user", foreign_keys=[School.admin_user_id])
    guardian = relationship("User", remote_side=[user_id], foreign_keys=[guardian_id])

    # Add other fields as needed

    __table_args__ = (
        UniqueConstraint('email'),
    )
