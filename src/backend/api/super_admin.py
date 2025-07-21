from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.backend.database.models import User, School, UserRole, Base
from src.backend.dependencies import get_db, is_super_admin, get_password_hash
from pydantic import BaseModel, EmailStr
import uuid

router = APIRouter(prefix="/admin", tags=["Super Admin"])

class SchoolAdminCreateRequest(BaseModel):
    school_name: str
    school_address: str
    school_city: str
    school_state: str
    school_contact_email: EmailStr
    school_phone_number: str
    admin_email: EmailStr
    admin_password: str
    admin_first_name: str
    admin_last_name: str

class SchoolAdminCreateResponse(BaseModel):
    school_id: uuid.UUID
    school_admin_user_id: uuid.UUID
    message: str

class SchoolResponse(BaseModel):
    school_id: uuid.UUID
    name: str
    city: str
    state: str
    is_active: bool

@router.post("/schools", response_model=SchoolAdminCreateResponse, dependencies=[Depends(is_super_admin)])
def create_school_and_admin(request: SchoolAdminCreateRequest, db: Session = Depends(get_db)):
    try:
        # Start transaction
        with db.begin():
            # Check if admin user exists
            admin_user = db.query(User).filter(User.email == request.admin_email).first()
            if admin_user:
                admin_user.role = UserRole.school_admin
                admin_user.password_hash = get_password_hash(request.admin_password)
                admin_user.first_name = request.admin_first_name
                admin_user.last_name = request.admin_last_name
            else:
                admin_user = User(
                    email=request.admin_email,
                    password_hash=get_password_hash(request.admin_password),
                    role=UserRole.school_admin,
                    first_name=request.admin_first_name,
                    last_name=request.admin_last_name
                )
                db.add(admin_user)
                db.flush()  # Get user_id
            # Create school
            school = School(
                name=request.school_name,
                address=request.school_address,
                city=request.school_city,
                state=request.school_state,
                contact_email=request.school_contact_email,
                phone_number=request.school_phone_number,
                admin_user_id=admin_user.user_id,
                is_active=True
            )
            db.add(school)
            db.flush()  # Get school_id
            # Link user to school
            admin_user.school_id = school.school_id
            db.commit()
        return SchoolAdminCreateResponse(
            school_id=school.school_id,
            school_admin_user_id=admin_user.user_id,
            message="School and School Admin created/updated successfully."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/schools", response_model=list[SchoolResponse], dependencies=[Depends(is_super_admin)])
def get_all_schools(db: Session = Depends(get_db)):
    try:
        schools = db.query(School).all()
        return [SchoolResponse(
            school_id=s.school_id,
            name=s.name,
            city=s.city,
            state=s.state,
            is_active=s.is_active
        ) for s in schools]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
