# Unit Tests for Akulearn Backend Services
# Run with: pytest test_services.py -v

import pytest
import json
import os
from datetime import datetime

# Import services
from auth_service import auth_service
from questions_service import questions_service
from progress_service import progress_service


class TestAuthService:
    """Test authentication service."""
    
    def test_register_valid(self):
        """Test valid user registration."""
        result = auth_service.register(
            email="testuser@example.com",
            password="SecurePass123",
            full_name="Test User",
            phone="08012345678",
            exam_board="WAEC",
            target_subjects=["Mathematics"]
        )
        
        assert result["success"] == True
        assert "user_id" in result
        assert result["email"] == "testuser@example.com"
    
    def test_register_invalid_email(self):
        """Test registration with invalid email."""
        result = auth_service.register(
            email="invalid_email",
            password="SecurePass123",
            full_name="Test User"
        )
        
        assert result["success"] == False
        assert "email" in result["error"].lower()
    
    def test_register_weak_password(self):
        """Test registration with weak password."""
        result = auth_service.register(
            email="test@example.com",
            password="weak",
            full_name="Test User"
        )
        
        assert result["success"] == False
        assert "password" in result["error"].lower()
    
    def test_register_duplicate_email(self):
        """Test registration with existing email."""
        # Register first user
        auth_service.register(
            email="duplicate@example.com",
            password="SecurePass123",
            full_name="User 1"
        )
        
        # Try to register with same email
        result = auth_service.register(
            email="duplicate@example.com",
            password="SecurePass123",
            full_name="User 2"
        )
        
        assert result["success"] == False
        assert "already registered" in result["error"].lower()
    
    def test_verify_otp_valid(self):
        """Test valid OTP verification."""
        # Register user
        register_result = auth_service.register(
            email="otp_test@example.com",
            password="SecurePass123",
            full_name="OTP Test User"
        )
        
        otp = register_result["verification_token"]
        
        # Verify OTP
        result = auth_service.verify_otp(
            email="otp_test@example.com",
            otp=otp
        )
        
        assert result["success"] == True
    
    def test_verify_otp_invalid(self):
        """Test invalid OTP."""
        result = auth_service.verify_otp(
            email="nonexistent@example.com",
            otp="999999"
        )
        
        assert result["success"] == False
    
    def test_login_valid(self):
        """Test valid login."""
        # Register and verify
        register_result = auth_service.register(
            email="login_test@example.com",
            password="SecurePass123",
            full_name="Login Test User"
        )
        
        otp = register_result["verification_token"]
        auth_service.verify_otp("login_test@example.com", otp)
        
        # Login
        result = auth_service.login(
            email="login_test@example.com",
            password="SecurePass123"
        )
        
        assert result["success"] == True
        assert "access_token" in result
        assert "refresh_token" in result
        assert result["user_id"] == register_result["user_id"]
    
    def test_login_invalid_password(self):
        """Test login with wrong password."""
        result = auth_service.login(
            email="login_test@example.com",
            password="WrongPassword123"
        )
        
        assert result["success"] == False
        assert "invalid" in result["error"].lower()
    
    def test_login_unverified_email(self):
        """Test login without email verification."""
        # Register but don't verify
        auth_service.register(
            email="unverified@example.com",
            password="SecurePass123",
            full_name="Unverified User"
        )
        
        result = auth_service.login(
            email="unverified@example.com",
            password="SecurePass123"
        )
        
        assert result["success"] == False
        assert "verified" in result["error"].lower()
    
    def test_refresh_token(self):
        """Test token refresh."""
        # Get refresh token from login
        register_result = auth_service.register(
            email="refresh_test@example.com",
            password="SecurePass123",
            full_name="Refresh Test"
        )
        
        auth_service.verify_otp(
            "refresh_test@example.com",
            register_result["verification_token"]
        )
        
        login_result = auth_service.login(
            email="refresh_test@example.com",
            password="SecurePass123"
        )
        
        # Refresh
        result = auth_service.refresh_token(
            refresh_token=login_result["refresh_token"]
        )
        
        assert result["success"] == True
        assert "access_token" in result


class TestQuestionsService:
    """Test questions service."""
    
    @classmethod
    def setup_class(cls):
        """Load questions before running tests."""
        result = questions_service.load_questions()
        assert result["success"] == True
    
    def test_load_questions(self):
        """Test loading questions from JSON."""
        assert questions_service.is_loaded() == True
        
        result = questions_service.get_statistics()
        assert result["success"] == True
        assert result["statistics"]["total_questions"] == 1350
    
    def test_search_by_exam_board(self):
        """Test searching by exam board."""
        result = questions_service.search(exam_board="WAEC")
        
        assert result["success"] == True
        assert result["total"] > 0
        assert all(q["exam_board"] == "WAEC" for q in result["questions"])
    
    def test_search_by_subject(self):
        """Test searching by subject."""
        result = questions_service.search(subject="Mathematics")
        
        assert result["success"] == True
        assert result["total"] > 0
        assert all(q["subject"] == "Mathematics" for q in result["questions"])
    
    def test_search_by_topic(self):
        """Test searching by topic."""
        result = questions_service.search(topic="Algebra")
        
        assert result["success"] == True
        assert all(q["topic"] == "Algebra" for q in result["questions"])
    
    def test_search_keyword(self):
        """Test keyword search."""
        result = questions_service.search(q="equation")
        
        assert result["success"] == True
        assert result["total"] > 0
    
    def test_search_with_pagination(self):
        """Test pagination."""
        result1 = questions_service.search(limit=10, offset=0)
        result2 = questions_service.search(limit=10, offset=10)
        
        assert len(result1["questions"]) == 10
        assert len(result2["questions"]) == 10
        # Questions should be different
        assert result1["questions"][0] != result2["questions"][0]
    
    def test_get_question(self):
        """Test getting full question details."""
        # Get first question
        search_result = questions_service.search(limit=1)
        question_id = search_result["questions"][0]["id"]
        
        result = questions_service.get_question(question_id)
        
        assert result["success"] == True
        assert result["question"]["id"] == question_id
        assert "correct_answer" in result["question"]
    
    def test_get_random_questions(self):
        """Test getting random questions."""
        result = questions_service.get_random_questions(count=15)
        
        assert result["success"] == True
        assert result["count"] == 15
        assert len(result["questions"]) == 15
        # Verify answers are hidden
        assert all("correct_answer" not in q for q in result["questions"])
    
    def test_get_filters(self):
        """Test getting available filters."""
        result = questions_service.get_filters()
        
        assert result["success"] == True
        assert "exam_boards" in result["filters"]
        assert "subjects" in result["filters"]
        assert "topics" in result["filters"]
        assert "years" in result["filters"]
        assert "difficulties" in result["filters"]
        
        # Verify expected values
        assert "WAEC" in result["filters"]["exam_boards"]
        assert "Mathematics" in result["filters"]["subjects"]


class TestProgressService:
    """Test progress tracking service."""
    
    def test_record_attempt(self):
        """Test recording an attempt."""
        result = progress_service.record_attempt(
            user_id="test_user_1",
            question_id="waec_math_2020_001",
            user_answer="B",
            correct_answer="B",
            time_taken_seconds=45,
            exam_board="WAEC",
            subject="Mathematics",
            topic="Algebra"
        )
        
        assert result["success"] == True
        assert result["is_correct"] == True
        assert result["score"] == 1
    
    def test_record_incorrect_attempt(self):
        """Test recording a wrong answer."""
        result = progress_service.record_attempt(
            user_id="test_user_2",
            question_id="waec_phys_2020_001",
            user_answer="A",
            correct_answer="B",
            time_taken_seconds=30,
            exam_board="WAEC",
            subject="Physics",
            topic="Mechanics"
        )
        
        assert result["success"] == True
        assert result["is_correct"] == False
        assert result["score"] == 0
    
    def test_get_progress(self):
        """Test getting user progress."""
        user_id = "test_user_3"
        
        # Record multiple attempts
        progress_service.record_attempt(
            user_id=user_id,
            question_id="q1",
            user_answer="A",
            correct_answer="A",
            exam_board="WAEC",
            subject="Mathematics",
            topic="Algebra"
        )
        
        progress_service.record_attempt(
            user_id=user_id,
            question_id="q2",
            user_answer="B",
            correct_answer="C",
            exam_board="WAEC",
            subject="Mathematics",
            topic="Algebra"
        )
        
        # Get progress
        result = progress_service.get_progress(user_id)
        
        assert result["success"] == True
        assert result["total_questions_attempted"] == 2
        assert result["total_correct"] == 1
        assert result["accuracy_percent"] == 50.0
    
    def test_get_progress_empty_user(self):
        """Test getting progress for new user."""
        result = progress_service.get_progress("new_user_123")
        
        assert result["success"] == True
        assert result["total_questions_attempted"] == 0
        assert result["accuracy_percent"] == 0.0
    
    def test_weak_topics_detection(self):
        """Test weak topic detection."""
        user_id = "weak_topics_user"
        
        # Record many failed attempts on one topic
        for i in range(5):
            progress_service.record_attempt(
                user_id=user_id,
                question_id=f"trig_{i}",
                user_answer="A",
                correct_answer="B",
                exam_board="WAEC",
                subject="Mathematics",
                topic="Trigonometry"
            )
        
        # Get weak topics
        result = progress_service.get_weak_topics(user_id)
        
        assert result["success"] == True
        assert len(result["weak_topics"]) > 0
        assert result["weak_topics"][0]["topic"] == "Trigonometry"
        assert result["weak_topics"][0]["accuracy_percent"] == 0.0
    
    def test_bookmark_question(self):
        """Test bookmarking a question."""
        user_id = "bookmark_user"
        question_id = "waec_math_2020_001"
        
        result = progress_service.bookmark_question(user_id, question_id)
        
        assert result["success"] == True
        assert result["bookmarked"] == True
    
    def test_get_bookmarks(self):
        """Test getting bookmarked questions."""
        user_id = "bookmark_user_2"
        
        # Bookmark multiple questions
        progress_service.bookmark_question(user_id, "q1")
        progress_service.bookmark_question(user_id, "q2")
        progress_service.bookmark_question(user_id, "q3")
        
        result = progress_service.get_bookmarks(user_id)
        
        assert result["success"] == True
        assert result["total"] == 3
        assert "q1" in result["bookmark_ids"]
        assert "q2" in result["bookmark_ids"]
        assert "q3" in result["bookmark_ids"]
    
    def test_record_assessment(self):
        """Test recording an assessment."""
        result = progress_service.record_assessment(
            user_id="assess_user",
            assessment_id="assess_123",
            exam_board="WAEC",
            correct_count=12,
            total_count=15,
            answers=[
                {"question_id": "q1", "is_correct": True},
                {"question_id": "q2", "is_correct": True},
                # ... more answers
            ]
        )
        
        assert result["success"] == True
        assert result["score"] == 12
        assert result["total_questions"] == 15
        assert result["accuracy_percent"] == 80.0


# Test fixtures and runners
if __name__ == "__main__":
    print("Run with: pytest test_services.py -v")
    print("\nQuick test without pytest:")
    print("- AuthService tests")
    print("- QuestionsService tests")
    print("- ProgressService tests")
