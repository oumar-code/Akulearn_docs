"""
Database configuration and session management for Phase 5 authentication.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import os
from pathlib import Path

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./akulearn_auth.db"  # Default to SQLite for MVP
)

# For SQLite, use check_same_thread=False to allow FastAPI async usage
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """
    Dependency function to get database session.
    Use with FastAPI Depends().
    
    Example:
        @app.get("/users/me")
        def get_current_user(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database session.
    Use for non-FastAPI code.
    
    Example:
        with get_db_context() as db:
            user = db.query(User).first()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables.
    Should be called on application startup.
    """
    from .auth_models import Base, create_tables
    
    # Create database directory if using SQLite
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Create tables
    create_tables(engine)
    print(f"✓ Database initialized: {DATABASE_URL}")


def reset_db():
    """
    Drop and recreate all tables.
    WARNING: This will delete all data!
    Only use in development.
    """
    from .auth_models import Base, drop_tables, create_tables
    
    print("⚠️  WARNING: Dropping all tables...")
    drop_tables(engine)
    print("✓ All tables dropped")
    
    print("Creating fresh tables...")
    create_tables(engine)
    print("✓ Database reset complete")


def check_connection():
    """
    Test database connection.
    Returns True if connection is successful.
    """
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test database connection
    print("Testing database connection...")
    if check_connection():
        print("✓ Database connection successful!")
        
        # Initialize database
        print("\nInitializing database...")
        init_db()
        print("✓ Database ready!")
    else:
        print("✗ Failed to connect to database")
