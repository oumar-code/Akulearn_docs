#!/usr/bin/env python3
"""
Wave 3 Progress Tracking Service
Tracks student progress, completion rates, and learning analytics
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class StudentProgress:
    """Student progress for a content item"""
    student_id: str
    content_id: str
    status: str  # 'not_started', 'in_progress', 'completed'
    progress_percentage: float
    time_spent_minutes: int
    started_at: str
    completed_at: Optional[str]
    last_accessed: str
    quiz_score: Optional[float]
    notes: str


class ProgressTrackingService:
    """Service for tracking student learning progress"""
    
    def __init__(self, database_file: str = "wave3_progress_database.json"):
        self.database_file = database_file
        self.progress_data = {}
        self.load_database()
    
    def load_database(self) -> bool:
        """Load progress data from JSON file"""
        try:
            if os.path.exists(self.database_file):
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.progress_data = data.get('progress', {})
                return True
            else:
                self.progress_data = {}
                self._save_database()
                return True
        except Exception as e:
            print(f"❌ Error loading progress database: {str(e)}")
            return False
    
    def _save_database(self) -> bool:
        """Save progress data to JSON file"""
        try:
            database = {
                "metadata": {
                    "version": "3.0.0",
                    "last_updated": datetime.now().isoformat(),
                    "total_records": sum(len(records) for records in self.progress_data.values())
                },
                "progress": self.progress_data
            }
            
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving progress database: {str(e)}")
            return False
    
    def start_content(self, student_id: str, content_id: str) -> Dict[str, Any]:
        """Record when a student starts a content item"""
        if student_id not in self.progress_data:
            self.progress_data[student_id] = {}
        
        progress = {
            "student_id": student_id,
            "content_id": content_id,
            "status": "in_progress",
            "progress_percentage": 0.0,
            "time_spent_minutes": 0,
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "last_accessed": datetime.now().isoformat(),
            "quiz_score": None,
            "notes": ""
        }
        
        self.progress_data[student_id][content_id] = progress
        self._save_database()
        
        return progress
    
    def update_progress(self, student_id: str, content_id: str, 
                       progress_percentage: float, time_spent_minutes: int = 0) -> Dict[str, Any]:
        """Update progress for a content item"""
        if student_id not in self.progress_data:
            self.progress_data[student_id] = {}
        
        if content_id not in self.progress_data[student_id]:
            # Start if not exists
            return self.start_content(student_id, content_id)
        
        progress = self.progress_data[student_id][content_id]
        progress['progress_percentage'] = min(progress_percentage, 100.0)
        progress['time_spent_minutes'] += time_spent_minutes
        progress['last_accessed'] = datetime.now().isoformat()
        
        # Auto-complete if 100%
        if progress_percentage >= 100.0 and progress['status'] != 'completed':
            progress['status'] = 'completed'
            progress['completed_at'] = datetime.now().isoformat()
        
        self._save_database()
        return progress
    
    def complete_content(self, student_id: str, content_id: str, 
                        quiz_score: Optional[float] = None) -> Dict[str, Any]:
        """Mark content as completed"""
        if student_id not in self.progress_data:
            self.progress_data[student_id] = {}
        
        if content_id not in self.progress_data[student_id]:
            progress = self.start_content(student_id, content_id)
        else:
            progress = self.progress_data[student_id][content_id]
        
        progress['status'] = 'completed'
        progress['progress_percentage'] = 100.0
        progress['completed_at'] = datetime.now().isoformat()
        progress['last_accessed'] = datetime.now().isoformat()
        
        if quiz_score is not None:
            progress['quiz_score'] = quiz_score
        
        self._save_database()
        return progress
    
    def get_student_progress(self, student_id: str, content_id: str = None) -> Optional[Dict[str, Any]]:
        """Get progress for a specific student and optionally a specific content"""
        if student_id not in self.progress_data:
            return None
        
        if content_id:
            return self.progress_data[student_id].get(content_id)
        else:
            return self.progress_data[student_id]
    
    def get_all_progress_for_student(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all progress records for a student"""
        if student_id not in self.progress_data:
            return []
        
        return list(self.progress_data[student_id].values())
    
    def get_completed_content(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all completed content for a student"""
        if student_id not in self.progress_data:
            return []
        
        return [
            progress for progress in self.progress_data[student_id].values()
            if progress['status'] == 'completed'
        ]
    
    def get_in_progress_content(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all in-progress content for a student"""
        if student_id not in self.progress_data:
            return []
        
        return [
            progress for progress in self.progress_data[student_id].values()
            if progress['status'] == 'in_progress'
        ]
    
    def get_statistics(self, student_id: str) -> Dict[str, Any]:
        """Get learning statistics for a student"""
        if student_id not in self.progress_data:
            return {
                "total_started": 0,
                "total_completed": 0,
                "total_in_progress": 0,
                "total_time_spent_minutes": 0,
                "average_quiz_score": 0.0,
                "completion_rate": 0.0
            }
        
        progress_list = list(self.progress_data[student_id].values())
        completed = [p for p in progress_list if p['status'] == 'completed']
        in_progress = [p for p in progress_list if p['status'] == 'in_progress']
        
        total_time = sum(p['time_spent_minutes'] for p in progress_list)
        quiz_scores = [p['quiz_score'] for p in completed if p['quiz_score'] is not None]
        avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
        
        return {
            "total_started": len(progress_list),
            "total_completed": len(completed),
            "total_in_progress": len(in_progress),
            "total_time_spent_minutes": total_time,
            "average_quiz_score": round(avg_score, 2),
            "completion_rate": round((len(completed) / len(progress_list) * 100) if progress_list else 0.0, 2)
        }
    
    def get_subject_statistics(self, student_id: str, subject: str, content_service) -> Dict[str, Any]:
        """Get statistics for a specific subject"""
        if student_id not in self.progress_data:
            return {"error": "No progress data for student"}
        
        # Get all content for subject
        subject_content = content_service.get_content_by_subject(subject, limit=1000)
        subject_content_ids = [c['id'] for c in subject_content]
        
        # Filter progress for this subject
        subject_progress = [
            p for cid, p in self.progress_data[student_id].items()
            if cid in subject_content_ids
        ]
        
        completed = [p for p in subject_progress if p['status'] == 'completed']
        
        return {
            "subject": subject,
            "total_content": len(subject_content),
            "started": len(subject_progress),
            "completed": len(completed),
            "completion_rate": round((len(completed) / len(subject_content) * 100) if subject_content else 0.0, 2)
        }
    
    def add_note(self, student_id: str, content_id: str, note: str) -> bool:
        """Add or update notes for content"""
        if student_id not in self.progress_data:
            return False
        
        if content_id not in self.progress_data[student_id]:
            return False
        
        self.progress_data[student_id][content_id]['notes'] = note
        self._save_database()
        return True
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard of top students by completion"""
        leaderboard = []
        
        for student_id, progress in self.progress_data.items():
            completed = sum(1 for p in progress.values() if p['status'] == 'completed')
            total_time = sum(p['time_spent_minutes'] for p in progress.values())
            
            leaderboard.append({
                "student_id": student_id,
                "completed_count": completed,
                "total_time_minutes": total_time,
                "total_started": len(progress)
            })
        
        # Sort by completed count
        leaderboard.sort(key=lambda x: x['completed_count'], reverse=True)
        
        return leaderboard[:limit]


# Global service instance
progress_service = ProgressTrackingService()


def get_progress_service() -> ProgressTrackingService:
    """Get global progress service instance"""
    return progress_service
