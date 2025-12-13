# Progress Tracking Service for Akulearn Backend
# Manages user attempts, progress tracking, and weak topic identification

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict


class ProgressService:
    """
    Tracks user attempts, calculates accuracy, identifies weak topics.
    
    For MVP: Uses in-memory storage. Production should use PostgreSQL.
    """
    
    # In-memory attempt store
    _user_attempts = defaultdict(list)  # user_id -> [attempts]
    _user_bookmarks = defaultdict(set)  # user_id -> {question_ids}
    _user_assessments = defaultdict(list)  # user_id -> [assessments]
    
    @staticmethod
    def record_attempt(user_id: str, question_id: str, user_answer: str,
                      correct_answer: str, time_taken_seconds: int = 0,
                      exam_board: str = None, subject: str = None,
                      topic: str = None) -> Dict:
        """
        Record a user's attempt at a question.
        
        Args:
            user_id: ID of the user
            question_id: ID of the question
            user_answer: User's selected answer
            correct_answer: Correct answer to the question
            time_taken_seconds: Time spent on this question
            exam_board: Exam board of the question
            subject: Subject of the question
            topic: Topic of the question
            
        Returns:
            Dict with attempt result
        """
        is_correct = user_answer.upper() == correct_answer.upper()
        score = 1 if is_correct else 0
        
        attempt = {
            "question_id": question_id,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "score": score,
            "time_taken_seconds": time_taken_seconds,
            "exam_board": exam_board,
            "subject": subject,
            "topic": topic,
            "attempted_at": datetime.utcnow().isoformat()
        }
        
        ProgressService._user_attempts[user_id].append(attempt)
        
        return {
            "success": True,
            "question_id": question_id,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "score": score
        }
    
    @staticmethod
    def get_progress(user_id: str) -> Dict:
        """
        Get user's overall progress statistics.
        
        Returns:
            Dict with accuracy by exam board, subject, topic, and weak topics
        """
        if user_id not in ProgressService._user_attempts:
            return {
                "success": True,
                "user_id": user_id,
                "total_questions_attempted": 0,
                "total_correct": 0,
                "accuracy_percent": 0.0,
                "by_exam_board": {},
                "by_subject": {},
                "weak_topics": [],
                "streak_days": 0,
                "last_activity": None
            }
        
        attempts = ProgressService._user_attempts[user_id]
        
        # Calculate overall stats
        total = len(attempts)
        correct = sum(1 for a in attempts if a["is_correct"])
        accuracy = (correct / total * 100) if total > 0 else 0
        
        # Calculate by exam board
        by_exam_board = defaultdict(lambda: {"attempted": 0, "correct": 0})
        for attempt in attempts:
            exam_board = attempt.get("exam_board", "Unknown")
            by_exam_board[exam_board]["attempted"] += 1
            if attempt["is_correct"]:
                by_exam_board[exam_board]["correct"] += 1
        
        # Calculate accuracy per exam board
        for board in by_exam_board:
            stats = by_exam_board[board]
            stats["accuracy_percent"] = (
                stats["correct"] / stats["attempted"] * 100
                if stats["attempted"] > 0 else 0
            )
        
        # Calculate by subject
        by_subject = defaultdict(lambda: {"attempted": 0, "correct": 0})
        for attempt in attempts:
            subject = attempt.get("subject", "Unknown")
            by_subject[subject]["attempted"] += 1
            if attempt["is_correct"]:
                by_subject[subject]["correct"] += 1
        
        # Calculate accuracy per subject
        for subject in by_subject:
            stats = by_subject[subject]
            stats["accuracy_percent"] = (
                stats["correct"] / stats["attempted"] * 100
                if stats["attempted"] > 0 else 0
            )
        
        # Identify weak topics (accuracy < 65%)
        by_topic = defaultdict(lambda: {"attempted": 0, "correct": 0})
        for attempt in attempts:
            topic = attempt.get("topic", "Unknown")
            by_topic[topic]["attempted"] += 1
            if attempt["is_correct"]:
                by_topic[topic]["correct"] += 1
        
        weak_topics = []
        for topic, stats in by_topic.items():
            accuracy = (
                stats["correct"] / stats["attempted"] * 100
                if stats["attempted"] > 0 else 0
            )
            stats["accuracy_percent"] = accuracy
            
            # Mark as weak if accuracy < 65% and at least 3 attempts
            if accuracy < 65 and stats["attempted"] >= 3:
                weak_topics.append({
                    "topic": topic,
                    "accuracy_percent": round(accuracy, 1),
                    "questions_attempted": stats["attempted"]
                })
        
        # Sort weak topics by accuracy (lowest first)
        weak_topics.sort(key=lambda x: x["accuracy_percent"])
        
        # Calculate streak (consecutive days of activity)
        streak_days = ProgressService._calculate_streak(attempts)
        
        # Get last activity
        last_activity = attempts[-1]["attempted_at"] if attempts else None
        
        return {
            "success": True,
            "user_id": user_id,
            "total_questions_attempted": total,
            "total_correct": correct,
            "accuracy_percent": round(accuracy, 1),
            "by_exam_board": dict(by_exam_board),
            "by_subject": dict(by_subject),
            "weak_topics": weak_topics[:5],  # Top 5 weak topics
            "streak_days": streak_days,
            "last_activity": last_activity
        }
    
    @staticmethod
    def _calculate_streak(attempts: List[Dict]) -> int:
        """Calculate consecutive days of activity."""
        if not attempts:
            return 0
        
        # Parse dates from attempts
        dates = set()
        for attempt in attempts:
            date_str = attempt["attempted_at"].split("T")[0]
            dates.add(date_str)
        
        # Sort dates
        sorted_dates = sorted(dates, reverse=True)
        
        if not sorted_dates:
            return 0
        
        # Check consecutive days
        streak = 1
        current_date = datetime.fromisoformat(sorted_dates[0]).date()
        
        for date_str in sorted_dates[1:]:
            date = datetime.fromisoformat(date_str).date()
            if (current_date - date).days == 1:
                streak += 1
                current_date = date
            else:
                break
        
        return streak
    
    @staticmethod
    def get_weak_topics(user_id: str) -> Dict:
        """
        Get topics where user is struggling (accuracy < 65%).
        
        Returns:
            Dict with weak topics and recommendations
        """
        progress = ProgressService.get_progress(user_id)
        
        weak_topics = []
        for topic_data in progress.get("weak_topics", []):
            topic = topic_data["topic"]
            accuracy = topic_data["accuracy_percent"]
            
            # Generate recommendation based on accuracy
            if accuracy < 40:
                recommendation = f"URGENT: Struggling with {topic}. Spend 3-4 hours reviewing core concepts."
            elif accuracy < 55:
                recommendation = f"Review {topic} comprehensively before exam."
            else:
                recommendation = f"Practice more {topic} problems to improve accuracy."
            
            weak_topics.append({
                "subject": "Multiple",  # Could be enhanced by subject mapping
                "topic": topic,
                "accuracy_percent": accuracy,
                "questions_attempted": topic_data["questions_attempted"],
                "recommendation": recommendation
            })
        
        return {
            "success": True,
            "user_id": user_id,
            "weak_topics": weak_topics
        }
    
    @staticmethod
    def bookmark_question(user_id: str, question_id: str) -> Dict:
        """Bookmark a question for later review."""
        ProgressService._user_bookmarks[user_id].add(question_id)
        
        return {
            "success": True,
            "bookmarked": True,
            "question_id": question_id
        }
    
    @staticmethod
    def unbookmark_question(user_id: str, question_id: str) -> Dict:
        """Remove a bookmark."""
        if question_id in ProgressService._user_bookmarks[user_id]:
            ProgressService._user_bookmarks[user_id].discard(question_id)
        
        return {
            "success": True,
            "bookmarked": False,
            "question_id": question_id
        }
    
    @staticmethod
    def get_bookmarks(user_id: str) -> Dict:
        """Get all bookmarked questions."""
        bookmarks = list(ProgressService._user_bookmarks.get(user_id, set()))
        
        return {
            "success": True,
            "user_id": user_id,
            "total": len(bookmarks),
            "bookmark_ids": bookmarks
        }
    
    @staticmethod
    def record_assessment(user_id: str, assessment_id: str, exam_board: str,
                         correct_count: int, total_count: int,
                         answers: List[Dict]) -> Dict:
        """
        Record a readiness assessment.
        
        Args:
            user_id: ID of the user
            assessment_id: ID of the assessment
            exam_board: Which exam board the assessment is for
            correct_count: Number of questions answered correctly
            total_count: Total questions in assessment
            answers: List of {question_id, user_answer, correct_answer, is_correct}
            
        Returns:
            Dict with assessment recorded
        """
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        
        # Calculate pass probability (simplified formula)
        # Based on accuracy and typical cutoff scores
        if accuracy >= 80:
            pass_probability = 85
        elif accuracy >= 70:
            pass_probability = 75
        elif accuracy >= 60:
            pass_probability = 60
        else:
            pass_probability = 40
        
        assessment = {
            "assessment_id": assessment_id,
            "exam_board": exam_board,
            "score": correct_count,
            "total_questions": total_count,
            "accuracy_percent": round(accuracy, 1),
            "pass_probability_percent": pass_probability,
            "answers": answers,
            "completed_at": datetime.utcnow().isoformat()
        }
        
        ProgressService._user_assessments[user_id].append(assessment)
        
        return {
            "success": True,
            "assessment_id": assessment_id,
            "score": correct_count,
            "total_questions": total_count,
            "accuracy_percent": round(accuracy, 1),
            "pass_probability_percent": pass_probability
        }
    
    @staticmethod
    def get_assessment_history(user_id: str, limit: int = 10) -> Dict:
        """Get user's assessment history."""
        assessments = ProgressService._user_assessments.get(user_id, [])
        
        # Return most recent assessments
        recent = assessments[-limit:] if assessments else []
        
        return {
            "success": True,
            "user_id": user_id,
            "total_assessments": len(assessments),
            "recent_assessments": recent
        }


# Global instance
progress_service = ProgressService()
