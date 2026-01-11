"""
Initialize Phase 5 authentication database.
Run this script to set up the database tables.
"""
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from backend.database.db_config import init_db, check_connection, reset_db


def main():
    """Initialize authentication database."""
    print("=" * 60)
    print("Phase 5: Authentication Database Initialization")
    print("=" * 60)
    print()
    
    # Check connection
    print("Step 1: Checking database connection...")
    if not check_connection():
        print("✗ Failed to connect to database")
        print("  Make sure DATABASE_URL is configured correctly")
        return False
    print("✓ Database connection successful")
    print()
    
    # Ask user if they want to reset (only in development)
    import os
    if os.path.exists("akulearn_auth.db"):
        response = input("Database already exists. Reset it? (y/N): ")
        if response.lower() == 'y':
            print("\nStep 2: Resetting database...")
            reset_db()
            print("✓ Database reset complete")
            print()
        else:
            print("\nStep 2: Skipping reset, using existing database")
            print()
    
    # Initialize database
    print("Step 3: Creating/updating tables...")
    init_db()
    print("✓ All tables created/updated")
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Install dependencies: pip install -r src/backend/requirements_phase5.txt")
    print("2. Start the API server: uvicorn src.backend.api.main:app --reload")
    print("3. Access Swagger docs: http://localhost:8000/docs")
    print("4. Test registration: POST /api/auth/register")
    print()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
