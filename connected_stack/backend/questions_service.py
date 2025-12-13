# Questions Service for Akulearn Backend
# Manages loading, searching, filtering, and retrieving exam questions

import json
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import random


class QuestionsService:
    """
    Manages exam questions data and search functionality.
    
    Data source: data/exam_papers/all_questions.json
    """
    
    # In-memory question store
    _questions_db = []
    _questions_index = {}  # question_id -> question for fast lookup
    _topics_index = {}  # topic -> [question_ids]
    _subjects_index = {}  # subject -> [question_ids]
    _exam_boards_index = {}  # exam_board -> [question_ids]
    
    # Statistics
    _stats = {
        "total_questions": 0,
        "by_exam_board": {},
        "by_subject": {},
        "by_topic": {},
        "by_difficulty": {},
        "by_year": {}
    }
    
    _loaded = False
    
    @classmethod
    def load_questions(cls, data_file_path: str = None) -> Dict:
        """
        Load questions from JSON file.
        
        Args:
            data_file_path: Path to all_questions.json
            
        Returns:
            Dict with success status and statistics
        """
        if data_file_path is None:
            # Default path relative to backend directory
            data_file_path = os.path.join(
                os.path.dirname(__file__),
                "../../data/exam_papers/all_questions.json"
            )
        
        if not os.path.exists(data_file_path):
            return {
                "success": False,
                "error": f"Data file not found: {data_file_path}"
            }
        
        try:
            with open(data_file_path, 'r') as f:
                questions_data = json.load(f)
            
            # Handle both list and dict formats
            if isinstance(questions_data, dict):
                questions_list = questions_data.get("questions", [])
            else:
                questions_list = questions_data
            
            # Load questions into memory
            for question in questions_list:
                cls._questions_db.append(question)
                
                # Build indices
                question_id = question.get("id")
                cls._questions_index[question_id] = question
                
                # Topic index
                topic = question.get("topic")
                if topic:
                    if topic not in cls._topics_index:
                        cls._topics_index[topic] = []
                    cls._topics_index[topic].append(question_id)
                
                # Subject index
                subject = question.get("subject")
                if subject:
                    if subject not in cls._subjects_index:
                        cls._subjects_index[subject] = []
                    cls._subjects_index[subject].append(question_id)
                
                # Exam board index
                exam_board = question.get("exam_board")
                if exam_board:
                    if exam_board not in cls._exam_boards_index:
                        cls._exam_boards_index[exam_board] = []
                    cls._exam_boards_index[exam_board].append(question_id)
                
                # Update statistics
                cls._stats["total_questions"] += 1
                
                # By exam board
                if exam_board:
                    cls._stats["by_exam_board"][exam_board] = \
                        cls._stats["by_exam_board"].get(exam_board, 0) + 1
                
                # By subject
                if subject:
                    cls._stats["by_subject"][subject] = \
                        cls._stats["by_subject"].get(subject, 0) + 1
                
                # By topic
                if topic:
                    cls._stats["by_topic"][topic] = \
                        cls._stats["by_topic"].get(topic, 0) + 1
                
                # By difficulty
                difficulty = question.get("difficulty", "unknown")
                cls._stats["by_difficulty"][difficulty] = \
                    cls._stats["by_difficulty"].get(difficulty, 0) + 1
                
                # By year
                year = question.get("year", "unknown")
                cls._stats["by_year"][str(year)] = \
                    cls._stats["by_year"].get(str(year), 0) + 1
            
            cls._loaded = True
            
            return {
                "success": True,
                "message": f"Loaded {cls._stats['total_questions']} questions",
                "statistics": cls._stats
            }
        
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Error loading questions: {str(e)}"}
    
    @classmethod
    def is_loaded(cls) -> bool:
        """Check if questions are loaded."""
        return cls._loaded
    
    @classmethod
    def search(cls, query: str = None, exam_board: str = None, subject: str = None,
               topic: str = None, year: int = None, difficulty: str = None,
               limit: int = 20, offset: int = 0) -> Dict:
        """
        Search for questions with multiple filters.
        
        Args:
            query: Keyword search (case-insensitive)
            exam_board: Filter by exam board
            subject: Filter by subject
            topic: Filter by topic
            year: Filter by year
            difficulty: Filter by difficulty
            limit: Max results to return
            offset: Pagination offset
            
        Returns:
            Dict with search results and pagination info
        """
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        # Start with all questions
        results = cls._questions_db.copy()
        
        # Apply filters
        if exam_board:
            results = [q for q in results if q.get("exam_board") == exam_board]
        
        if subject:
            results = [q for q in results if q.get("subject") == subject]
        
        if topic:
            results = [q for q in results if q.get("topic") == topic]
        
        if year:
            results = [q for q in results if q.get("year") == year]
        
        if difficulty:
            results = [q for q in results if q.get("difficulty") == difficulty]
        
        # Keyword search (search in question text and topic)
        if query:
            query_lower = query.lower()
            results = [
                q for q in results
                if query_lower in q.get("question_text", "").lower() or
                   query_lower in q.get("topic", "").lower() or
                   query_lower in q.get("subject", "").lower()
            ]
        
        # Get total count before pagination
        total = len(results)
        
        # Apply pagination
        results = results[offset:offset + limit]
        
        # Remove sensitive data (correct answer) from preview
        for q in results:
            q_copy = q.copy()
            q_copy.pop("correct_answer", None)
            q_copy.pop("explanation", None)
            q_copy["preview"] = q.get("question_text", "")[:100] + "..."
            results[results.index(q)] = q_copy
        
        return {
            "success": True,
            "total": total,
            "limit": limit,
            "offset": offset,
            "questions": results
        }
    
    @classmethod
    def get_question(cls, question_id: str, include_answer: bool = True) -> Dict:
        """
        Get full question details by ID.
        
        Args:
            question_id: ID of the question
            include_answer: Whether to include correct answer (for logged-in users)
            
        Returns:
            Dict with question details
        """
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        if question_id not in cls._questions_index:
            return {"success": False, "error": "Question not found"}
        
        question = cls._questions_index[question_id].copy()
        
        # Hide answer if not requested
        if not include_answer:
            question.pop("correct_answer", None)
            question.pop("explanation", None)
        
        return {"success": True, "question": question}
    
    @classmethod
    def get_random_questions(cls, count: int = 15, exam_board: str = None,
                            subject: str = None, difficulty: str = None) -> Dict:
        """
        Get random questions for quiz/assessment.
        
        Args:
            count: Number of questions to return
            exam_board: Filter by exam board
            subject: Filter by subject
            difficulty: Filter by difficulty
            
        Returns:
            Dict with random questions (without correct answers)
        """
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        # Limit count
        count = min(count, 100)
        
        # Filter questions
        filtered = cls._questions_db.copy()
        
        if exam_board:
            filtered = [q for q in filtered if q.get("exam_board") == exam_board]
        
        if subject:
            filtered = [q for q in filtered if q.get("subject") == subject]
        
        if difficulty:
            filtered = [q for q in filtered if q.get("difficulty") == difficulty]
        
        # Check if we have enough questions
        if len(filtered) < count:
            return {
                "success": False,
                "error": f"Only {len(filtered)} questions available, requested {count}"
            }
        
        # Sample random questions
        questions = random.sample(filtered, count)
        
        # Remove answers
        for q in questions:
            q.pop("correct_answer", None)
            q.pop("explanation", None)
        
        return {
            "success": True,
            "count": len(questions),
            "questions": questions
        }
    
    @classmethod
    def get_by_topic(cls, topic: str, limit: int = 20, offset: int = 0) -> Dict:
        """Get all questions for a specific topic."""
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        if topic not in cls._topics_index:
            return {"success": False, "error": f"Topic not found: {topic}"}
        
        question_ids = cls._topics_index[topic]
        total = len(question_ids)
        
        # Pagination
        paginated_ids = question_ids[offset:offset + limit]
        questions = [cls._questions_index[qid] for qid in paginated_ids]
        
        return {
            "success": True,
            "topic": topic,
            "total": total,
            "limit": limit,
            "offset": offset,
            "questions": questions
        }
    
    @classmethod
    def get_by_subject(cls, subject: str, limit: int = 20, offset: int = 0) -> Dict:
        """Get all questions for a specific subject."""
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        if subject not in cls._subjects_index:
            return {"success": False, "error": f"Subject not found: {subject}"}
        
        question_ids = cls._subjects_index[subject]
        total = len(question_ids)
        
        # Pagination
        paginated_ids = question_ids[offset:offset + limit]
        questions = [cls._questions_index[qid] for qid in paginated_ids]
        
        return {
            "success": True,
            "subject": subject,
            "total": total,
            "limit": limit,
            "offset": offset,
            "questions": questions
        }
    
    @classmethod
    def get_statistics(cls) -> Dict:
        """Get overall statistics about questions."""
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        return {
            "success": True,
            "statistics": cls._stats
        }
    
    @classmethod
    def get_filters(cls) -> Dict:
        """
        Get available filter options for UI.
        
        Returns all valid values for exam boards, subjects, topics, years, difficulties
        """
        if not cls._loaded:
            return {"success": False, "error": "Questions not loaded"}
        
        return {
            "success": True,
            "filters": {
                "exam_boards": list(cls._exam_boards_index.keys()),
                "subjects": list(cls._subjects_index.keys()),
                "topics": list(cls._topics_index.keys()),
                "years": sorted([int(y) for y in cls._stats["by_year"].keys() 
                               if y != "unknown"]),
                "difficulties": list(cls._stats["by_difficulty"].keys())
            }
        }


# Global instance
questions_service = QuestionsService()
