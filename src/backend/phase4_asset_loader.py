#!/usr/bin/env python3
"""Phase 4 Asset Loader - Practice Questions

Extends ExtendedAssetLoader to include Phase 4 practice questions:
1. Multiple Choice Questions
2. True/False Questions
3. Fill-in-the-Blank Questions
4. Matching Questions
5. Short Answer Questions
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from src.backend.extended_asset_loader import ExtendedAssetLoader


@dataclass
class QuestionAsset:
    """Represents a Phase 4 question asset."""
    question_id: str
    subject: str
    topic: str
    grade: str
    question_type: str
    difficulty: str
    question_data: Dict[str, Any]
    points: int
    estimated_time: int
    tags: List[str]


class Phase4AssetLoader(ExtendedAssetLoader):
    """Extended asset loader with Phase 4 practice question support."""
    
    def __init__(self, assets_dir: str = "generated_assets"):
        super().__init__(assets_dir)
        self.phase4_manifest_path = self.assets_dir / "phase4_manifest.json"
        self.phase4_questions_path = self.assets_dir / "questions" / "phase4_questions.json"
        self._phase4_manifest = None
        self._questions_data = None
        self._question_cache = {}
    
    # ====================
    # DATA LOADING
    # ====================
    
    def load_phase4_manifest(self) -> Dict[str, Any]:
        """Load Phase 4 manifest file."""
        if self._phase4_manifest is None:
            if self.phase4_manifest_path.exists():
                with self.phase4_manifest_path.open("r", encoding="utf-8") as f:
                    self._phase4_manifest = json.load(f)
            else:
                self._phase4_manifest = {
                    "metadata": {"total_questions": 0, "subjects": 0},
                    "questions_by_subject": {}
                }
        return self._phase4_manifest
    
    def load_questions_data(self) -> Dict[str, Any]:
        """Load questions database."""
        if self._questions_data is None:
            if self.phase4_questions_path.exists():
                with self.phase4_questions_path.open("r", encoding="utf-8") as f:
                    self._questions_data = json.load(f)
            else:
                self._questions_data = {
                    "metadata": {"total_questions": 0},
                    "questions": []
                }
        return self._questions_data
    
    # ====================
    # QUESTION RETRIEVAL
    # ====================
    
    def get_questions_for_lesson(self, lesson_id: str, limit: Optional[int] = None) -> List[QuestionAsset]:
        """Get all questions for a specific lesson/topic."""
        data = self.load_questions_data()
        questions = []
        
        for q in data.get("questions", []):
            # Match by topic or subject
            if lesson_id.lower() in q.get("topic", "").lower() or \
               lesson_id.lower() in q.get("subject", "").lower():
                questions.append(self._create_question_asset(q))
        
        if limit:
            questions = questions[:limit]
        
        return questions
    
    def get_question_by_id(self, question_id: str) -> Optional[QuestionAsset]:
        """Get a specific question by ID."""
        if question_id in self._question_cache:
            return self._question_cache[question_id]
        
        data = self.load_questions_data()
        
        for q in data.get("questions", []):
            if q.get("id") == question_id:
                asset = self._create_question_asset(q)
                self._question_cache[question_id] = asset
                return asset
        
        return None
    
    def get_questions_by_type(self, question_type: str, limit: Optional[int] = 10) -> List[QuestionAsset]:
        """Get questions of a specific type."""
        data = self.load_questions_data()
        questions = []
        
        for q in data.get("questions", []):
            if q.get("question_type") == question_type:
                questions.append(self._create_question_asset(q))
        
        if limit:
            questions = questions[:limit]
        
        return questions
    
    def get_questions_by_subject(self, subject: str, limit: Optional[int] = None) -> List[QuestionAsset]:
        """Get all questions for a specific subject."""
        data = self.load_questions_data()
        questions = []
        
        for q in data.get("questions", []):
            if q.get("subject", "").lower() == subject.lower():
                questions.append(self._create_question_asset(q))
        
        if limit:
            questions = questions[:limit]
        
        return questions
    
    def get_questions_by_difficulty(self, difficulty: str, limit: Optional[int] = None) -> List[QuestionAsset]:
        """Get questions of a specific difficulty level."""
        data = self.load_questions_data()
        questions = []
        
        for q in data.get("questions", []):
            if q.get("difficulty", "").lower() == difficulty.lower():
                questions.append(self._create_question_asset(q))
        
        if limit:
            questions = questions[:limit]
        
        return questions
    
    def get_random_questions(self, count: int = 10, subject: Optional[str] = None, 
                           difficulty: Optional[str] = None) -> List[QuestionAsset]:
        """Get random questions with optional filters."""
        import random
        
        data = self.load_questions_data()
        questions = data.get("questions", [])
        
        # Apply filters
        if subject:
            questions = [q for q in questions if q.get("subject", "").lower() == subject.lower()]
        
        if difficulty:
            questions = [q for q in questions if q.get("difficulty", "").lower() == difficulty.lower()]
        
        # Shuffle and limit
        random.shuffle(questions)
        selected = questions[:count]
        
        return [self._create_question_asset(q) for q in selected]
    
    # ====================
    # ANSWER VALIDATION
    # ====================
    
    def validate_answer(self, question_id: str, user_answer: Any) -> Dict[str, Any]:
        """Validate a user's answer to a question."""
        question = self.get_question_by_id(question_id)
        
        if not question:
            return {
                "valid": False,
                "error": "Question not found",
                "question_id": question_id
            }
        
        q_data = question.question_data
        q_type = question.question_type
        
        # Validation logic by question type
        if q_type == "multiple_choice":
            correct = q_data.get("correct_answer")
            is_correct = user_answer == correct
            return {
                "valid": True,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct,
                "explanation": q_data.get("explanation", ""),
                "points_earned": question.points if is_correct else 0,
                "points_possible": question.points
            }
        
        elif q_type == "true_false":
            correct = q_data.get("correct_answer")
            is_correct = bool(user_answer) == bool(correct)
            return {
                "valid": True,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct,
                "explanation": q_data.get("explanation", ""),
                "points_earned": question.points if is_correct else 0,
                "points_possible": question.points
            }
        
        elif q_type == "fill_blank":
            correct = q_data.get("correct_answer", "").lower()
            alternatives = [a.lower() for a in q_data.get("alternative_answers", [])]
            user_ans = str(user_answer).lower().strip()
            
            is_correct = user_ans == correct or user_ans in alternatives
            return {
                "valid": True,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": q_data.get("correct_answer"),
                "explanation": q_data.get("explanation", ""),
                "points_earned": question.points if is_correct else 0,
                "points_possible": question.points
            }
        
        elif q_type == "matching":
            correct_pairs = q_data.get("correct_pairs", {})
            # user_answer should be dict like {0: 1, 1: 2, ...}
            if not isinstance(user_answer, dict):
                return {
                    "valid": False,
                    "error": "Invalid answer format for matching question"
                }
            
            total = len(correct_pairs)
            correct_count = sum(1 for k, v in user_answer.items() 
                              if str(correct_pairs.get(int(k))) == str(v))
            
            is_correct = correct_count == total
            partial_points = (correct_count / total) * question.points if total > 0 else 0
            
            return {
                "valid": True,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct_pairs,
                "correct_count": correct_count,
                "total_pairs": total,
                "explanation": q_data.get("explanation", ""),
                "points_earned": partial_points,
                "points_possible": question.points
            }
        
        elif q_type == "short_answer":
            # Short answer requires manual grading or keyword matching
            sample_answer = q_data.get("sample_answer", "")
            marking_criteria = q_data.get("marking_criteria", [])
            
            return {
                "valid": True,
                "requires_manual_grading": True,
                "user_answer": user_answer,
                "sample_answer": sample_answer,
                "marking_criteria": marking_criteria,
                "points_possible": question.points,
                "note": "This answer requires manual grading by an instructor"
            }
        
        return {
            "valid": False,
            "error": f"Unknown question type: {q_type}"
        }
    
    # ====================
    # STATISTICS
    # ====================
    
    def get_phase4_stats(self) -> Dict[str, Any]:
        """Get Phase 4 statistics."""
        data = self.load_questions_data()
        manifest = self.load_phase4_manifest()
        
        metadata = data.get("metadata", {})
        
        # Count by type
        questions = data.get("questions", [])
        type_counts = {}
        difficulty_counts = {}
        subject_counts = {}
        
        for q in questions:
            q_type = q.get("question_type", "unknown")
            difficulty = q.get("difficulty", "unknown")
            subject = q.get("subject", "unknown")
            
            type_counts[q_type] = type_counts.get(q_type, 0) + 1
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            subject_counts[subject] = subject_counts.get(subject, 0) + 1
        
        return {
            "total_questions": metadata.get("total_questions", 0),
            "question_types": metadata.get("question_types", 0),
            "subjects": metadata.get("subjects", 0),
            "total_points": metadata.get("total_points", 0),
            "total_time_minutes": metadata.get("total_time_minutes", 0),
            "type_breakdown": type_counts,
            "difficulty_breakdown": difficulty_counts,
            "subject_breakdown": subject_counts,
            "generated_at": metadata.get("generated_at")
        }
    
    def get_subject_stats(self, subject: str) -> Dict[str, Any]:
        """Get statistics for a specific subject."""
        questions = self.get_questions_by_subject(subject)
        
        if not questions:
            return {
                "subject": subject,
                "total_questions": 0,
                "error": "No questions found for this subject"
            }
        
        type_counts = {}
        difficulty_counts = {}
        total_points = 0
        total_time = 0
        
        for q in questions:
            type_counts[q.question_type] = type_counts.get(q.question_type, 0) + 1
            difficulty_counts[q.difficulty] = difficulty_counts.get(q.difficulty, 0) + 1
            total_points += q.points
            total_time += q.estimated_time
        
        return {
            "subject": subject,
            "total_questions": len(questions),
            "total_points": total_points,
            "total_time_minutes": total_time // 60,
            "type_breakdown": type_counts,
            "difficulty_breakdown": difficulty_counts
        }
    
    # ====================
    # HELPERS
    # ====================
    
    def _create_question_asset(self, q: Dict[str, Any]) -> QuestionAsset:
        """Create QuestionAsset from question data."""
        return QuestionAsset(
            question_id=q.get("id", ""),
            subject=q.get("subject", ""),
            topic=q.get("topic", ""),
            grade=q.get("grade", ""),
            question_type=q.get("question_type", ""),
            difficulty=q.get("difficulty", ""),
            question_data=q,
            points=q.get("points", 0),
            estimated_time=q.get("estimated_time", 0),
            tags=q.get("tags", [])
        )


# ============================================================================
# GLOBAL LOADER INSTANCE
# ============================================================================

_phase4_loader: Optional[Phase4AssetLoader] = None


def initialize_phase4_loader(assets_dir: str = "generated_assets") -> Phase4AssetLoader:
    """Initialize the global Phase 4 asset loader."""
    global _phase4_loader
    _phase4_loader = Phase4AssetLoader(assets_dir)
    return _phase4_loader


def get_phase4_loader() -> Optional[Phase4AssetLoader]:
    """Get the global Phase 4 asset loader instance."""
    return _phase4_loader
