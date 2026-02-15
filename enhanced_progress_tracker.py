#!/usr/bin/env python3
"""
Enhanced Progress Tracking System
Integrates quiz results, time-on-task analytics, and mastery level tracking
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from neo4j import GraphDatabase, basic_auth
    NEO4J_AVAILABLE = True
except (ImportError, Exception):
    NEO4J_AVAILABLE = False
    GraphDatabase = None


class MasteryLevel(Enum):
    """Student mastery levels"""
    NOT_STARTED = "not_started"
    NOVICE = "novice"           # 0-40%
    DEVELOPING = "developing"   # 41-60%
    PROFICIENT = "proficient"   # 61-80%
    ADVANCED = "advanced"       # 81-95%
    MASTERED = "mastered"       # 96-100%


class ActivityType(Enum):
    """Types of learning activities"""
    LESSON_VIEW = "lesson_view"
    CONTENT_READ = "content_read"
    EXAMPLE_STUDIED = "example_studied"
    PROBLEM_ATTEMPTED = "problem_attempted"
    PROBLEM_COMPLETED = "problem_completed"
    QUIZ_STARTED = "quiz_started"
    QUIZ_COMPLETED = "quiz_completed"
    ASSESSMENT_TAKEN = "assessment_taken"
    RESOURCE_ACCESSED = "resource_accessed"


@dataclass
class QuizResult:
    """Quiz result data"""
    quiz_id: str
    lesson_id: str
    student_id: str
    score: float
    max_score: float
    percentage: float
    time_taken_seconds: int
    questions_correct: int
    questions_total: int
    attempted_at: str
    completed_at: str
    answers: List[Dict[str, Any]]


@dataclass
class LearningActivity:
    """Individual learning activity"""
    activity_id: str
    student_id: str
    lesson_id: str
    activity_type: ActivityType
    duration_seconds: int
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class MasteryMetrics:
    """Comprehensive mastery metrics"""
    lesson_id: str
    student_id: str
    mastery_level: MasteryLevel
    mastery_percentage: float
    total_time_spent_seconds: int
    activities_completed: int
    quiz_average: float
    problems_correct: int
    problems_attempted: int
    last_activity: str
    skill_scores: Dict[str, float]


class EnhancedProgressTracker:
    """
    Advanced progress tracking with quiz integration and mastery analytics
    """

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password"):
        self.uri = neo4j_uri
        self.user = neo4j_user
        self.password = neo4j_password
        self.driver = None
        
        self._connect()

    def _connect(self):
        """Connect to Neo4j"""
        if not NEO4J_AVAILABLE:
            return
        
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 7687))
            sock.close()
            
            if result != 0:
                return
            
            from neo4j import GraphDatabase, basic_auth
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=basic_auth(self.user, self.password)
            )
            print("✅ Connected to Neo4j for progress tracking")
        except Exception:
            pass

    def record_quiz_result(self, quiz_result: QuizResult):
        """Record quiz result and update mastery"""
        if not self.driver:
            print("⚠️ Neo4j not available")
            return
        
        with self.driver.session() as session:
            # Create quiz result node
            session.run("""
                MERGE (s:Student {id: $student_id})
                MERGE (l:Lesson {id: $lesson_id})
                CREATE (qr:QuizResult {
                    id: $quiz_id,
                    score: $score,
                    max_score: $max_score,
                    percentage: $percentage,
                    time_taken_seconds: $time_taken,
                    questions_correct: $questions_correct,
                    questions_total: $questions_total,
                    attempted_at: $attempted_at,
                    completed_at: $completed_at,
                    answers: $answers
                })
                MERGE (s)-[:TOOK_QUIZ]->(qr)
                MERGE (qr)-[:FOR_LESSON]->(l)
            """, {
                "student_id": quiz_result.student_id,
                "lesson_id": quiz_result.lesson_id,
                "quiz_id": quiz_result.quiz_id,
                "score": quiz_result.score,
                "max_score": quiz_result.max_score,
                "percentage": quiz_result.percentage,
                "time_taken": quiz_result.time_taken_seconds,
                "questions_correct": quiz_result.questions_correct,
                "questions_total": quiz_result.questions_total,
                "attempted_at": quiz_result.attempted_at,
                "completed_at": quiz_result.completed_at,
                "answers": [asdict(a) if hasattr(a, '__dict__') else a for a in quiz_result.answers]
            })
            
            # Update mastery level
            self._update_mastery_level(quiz_result.student_id, quiz_result.lesson_id)
            
            print(f"✅ Quiz result recorded: {quiz_result.percentage:.1f}%")

    def record_learning_activity(self, activity: LearningActivity):
        """Record a learning activity for time-on-task analytics"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            session.run("""
                MERGE (s:Student {id: $student_id})
                MERGE (l:Lesson {id: $lesson_id})
                CREATE (a:LearningActivity {
                    id: $activity_id,
                    type: $activity_type,
                    duration_seconds: $duration_seconds,
                    timestamp: $timestamp,
                    metadata: $metadata
                })
                MERGE (s)-[:PERFORMED_ACTIVITY]->(a)
                MERGE (a)-[:IN_LESSON]->(l)
            """, {
                "student_id": activity.student_id,
                "lesson_id": activity.lesson_id,
                "activity_id": activity.activity_id,
                "activity_type": activity.activity_type.value,
                "duration_seconds": activity.duration_seconds,
                "timestamp": activity.timestamp,
                "metadata": activity.metadata
            })
            
            # Update time-on-task metrics
            self._update_time_metrics(activity.student_id, activity.lesson_id)

    def _update_mastery_level(self, student_id: str, lesson_id: str):
        """Calculate and update mastery level"""
        if not self.driver:
            return
        
        metrics = self.calculate_mastery_metrics(student_id, lesson_id)
        
        if not metrics:
            return
        
        with self.driver.session() as session:
            session.run("""
                MATCH (s:Student {id: $student_id})-[r:STUDYING]->(l:Lesson {id: $lesson_id})
                SET r.mastery_level = $mastery_level,
                    r.mastery_percentage = $mastery_percentage,
                    r.last_updated = datetime()
            """, {
                "student_id": student_id,
                "lesson_id": lesson_id,
                "mastery_level": metrics.mastery_level.value,
                "mastery_percentage": metrics.mastery_percentage
            })

    def _update_time_metrics(self, student_id: str, lesson_id: str):
        """Update time-on-task metrics"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Student {id: $student_id})-[:PERFORMED_ACTIVITY]->(a:LearningActivity)-[:IN_LESSON]->(l:Lesson {id: $lesson_id})
                RETURN sum(a.duration_seconds) as total_time,
                       count(a) as activity_count
            """, {
                "student_id": student_id,
                "lesson_id": lesson_id
            })
            
            record = result.single()
            if record:
                session.run("""
                    MATCH (s:Student {id: $student_id})-[r:STUDYING]->(l:Lesson {id: $lesson_id})
                    SET r.time_spent_seconds = $total_time,
                        r.activity_count = $activity_count,
                        r.last_updated = datetime()
                """, {
                    "student_id": student_id,
                    "lesson_id": lesson_id,
                    "total_time": record['total_time'],
                    "activity_count": record['activity_count']
                })

    def calculate_mastery_metrics(self, student_id: str, lesson_id: str) -> Optional[MasteryMetrics]:
        """Calculate comprehensive mastery metrics"""
        if not self.driver:
            return None
        
        with self.driver.session() as session:
            # Get quiz scores
            quiz_result = session.run("""
                MATCH (s:Student {id: $student_id})-[:TOOK_QUIZ]->(qr:QuizResult)-[:FOR_LESSON]->(l:Lesson {id: $lesson_id})
                RETURN avg(qr.percentage) as avg_quiz_score,
                       max(qr.percentage) as best_quiz_score,
                       count(qr) as quiz_count
            """, {
                "student_id": student_id,
                "lesson_id": lesson_id
            })
            
            quiz_data = quiz_result.single()
            avg_quiz_score = quiz_data['avg_quiz_score'] if quiz_data and quiz_data['avg_quiz_score'] else 0.0
            
            # Get problem completion
            problem_result = session.run("""
                MATCH (s:Student {id: $student_id})-[:SOLVED_PROBLEM]->(p:PracticeProblem)<-[:HAS_PROBLEM]-(l:Lesson {id: $lesson_id})
                OPTIONAL MATCH (l)-[:HAS_PROBLEM]->(all_problems:PracticeProblem)
                RETURN count(DISTINCT p) as problems_solved,
                       count(DISTINCT all_problems) as total_problems
            """, {
                "student_id": student_id,
                "lesson_id": lesson_id
            })
            
            problem_data = problem_result.single()
            problems_solved = problem_data['problems_solved'] if problem_data else 0
            total_problems = problem_data['total_problems'] if problem_data else 10
            
            # Get time spent and activities
            activity_result = session.run("""
                MATCH (s:Student {id: $student_id})-[:PERFORMED_ACTIVITY]->(a:LearningActivity)-[:IN_LESSON]->(l:Lesson {id: $lesson_id})
                RETURN sum(a.duration_seconds) as total_time,
                       count(a) as activity_count,
                       max(a.timestamp) as last_activity
            """, {
                "student_id": student_id,
                "lesson_id": lesson_id
            })
            
            activity_data = activity_result.single()
            total_time = activity_data['total_time'] if activity_data and activity_data['total_time'] else 0
            activity_count = activity_data['activity_count'] if activity_data else 0
            last_activity = activity_data['last_activity'] if activity_data else datetime.now().isoformat()
            
            # Calculate mastery percentage
            quiz_weight = 0.5
            problems_weight = 0.4
            engagement_weight = 0.1
            
            quiz_score = avg_quiz_score
            problem_score = (problems_solved / total_problems * 100) if total_problems > 0 else 0
            engagement_score = min(100, (activity_count / 20) * 100)  # Cap at 20 activities
            
            mastery_percentage = (
                quiz_score * quiz_weight +
                problem_score * problems_weight +
                engagement_score * engagement_weight
            )
            
            # Determine mastery level
            if mastery_percentage >= 96:
                mastery_level = MasteryLevel.MASTERED
            elif mastery_percentage >= 81:
                mastery_level = MasteryLevel.ADVANCED
            elif mastery_percentage >= 61:
                mastery_level = MasteryLevel.PROFICIENT
            elif mastery_percentage >= 41:
                mastery_level = MasteryLevel.DEVELOPING
            elif mastery_percentage > 0:
                mastery_level = MasteryLevel.NOVICE
            else:
                mastery_level = MasteryLevel.NOT_STARTED
            
            # Calculate skill scores (simplified)
            skill_scores = {
                "comprehension": quiz_score,
                "problem_solving": problem_score,
                "engagement": engagement_score
            }
            
            return MasteryMetrics(
                lesson_id=lesson_id,
                student_id=student_id,
                mastery_level=mastery_level,
                mastery_percentage=mastery_percentage,
                total_time_spent_seconds=total_time,
                activities_completed=activity_count,
                quiz_average=avg_quiz_score,
                problems_correct=problems_solved,
                problems_attempted=problems_solved,  # Simplified
                last_activity=last_activity,
                skill_scores=skill_scores
            )

    def get_student_mastery_overview(self, student_id: str) -> List[MasteryMetrics]:
        """Get mastery overview for all lessons"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Student {id: $student_id})-[:STUDYING]->(l:Lesson)
                WHERE l.wave = 3
                RETURN l.id as lesson_id
            """, {"student_id": student_id})
            
            mastery_list = []
            for record in result:
                metrics = self.calculate_mastery_metrics(student_id, record['lesson_id'])
                if metrics:
                    mastery_list.append(metrics)
            
            return sorted(mastery_list, key=lambda m: m.mastery_percentage, reverse=True)

    def get_time_on_task_analytics(self, student_id: str, days: int = 7) -> Dict[str, Any]:
        """Get time-on-task analytics for recent period"""
        if not self.driver:
            return {}
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Student {id: $student_id})-[:PERFORMED_ACTIVITY]->(a:LearningActivity)
                WHERE a.timestamp >= $cutoff_date
                WITH a
                ORDER BY a.timestamp
                RETURN collect({
                    timestamp: a.timestamp,
                    type: a.type,
                    duration: a.duration_seconds,
                    lesson_id: [(a)-[:IN_LESSON]->(l:Lesson) | l.id][0]
                }) as activities,
                sum(a.duration_seconds) as total_time,
                count(a) as total_activities
            """, {
                "student_id": student_id,
                "cutoff_date": cutoff_date
            })
            
            record = result.single()
            
            if not record:
                return {
                    "period_days": days,
                    "total_time_seconds": 0,
                    "total_activities": 0,
                    "daily_average_seconds": 0,
                    "activities": []
                }
            
            total_time = record['total_time']
            total_activities = record['total_activities']
            
            return {
                "period_days": days,
                "total_time_seconds": total_time,
                "total_time_minutes": total_time / 60,
                "total_time_hours": total_time / 3600,
                "total_activities": total_activities,
                "daily_average_seconds": total_time / days,
                "daily_average_minutes": (total_time / days) / 60,
                "activities_per_day": total_activities / days,
                "activities": record['activities']
            }

    def recommend_next_lessons(self, student_id: str, count: int = 3) -> List[Dict[str, Any]]:
        """Recommend next lessons based on prerequisites and mastery"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                // Find lessons the student has mastered or is proficient in
                MATCH (s:Student {id: $student_id})-[r:STUDYING]->(completed:Lesson)
                WHERE r.mastery_level IN ['proficient', 'advanced', 'mastered']
                
                // Find lessons that require those as prerequisites
                MATCH (next:Lesson)-[:REQUIRES_PREREQUISITE]->(completed)
                WHERE NOT exists((s)-[:STUDYING]->(next))
                
                // Get lesson details
                RETURN DISTINCT next.id as lesson_id,
                       next.subject as subject,
                       next.title as title,
                       next.difficulty_level as difficulty,
                       count(completed) as prerequisites_met
                ORDER BY prerequisites_met DESC, next.subject
                LIMIT $count
            """, {
                "student_id": student_id,
                "count": count
            })
            
            recommendations = []
            for record in result:
                recommendations.append({
                    "lesson_id": record['lesson_id'],
                    "subject": record['subject'],
                    "title": record['title'],
                    "difficulty": record['difficulty'],
                    "prerequisites_met": record['prerequisites_met'],
                    "reason": "Prerequisites completed"
                })
            
            return recommendations

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()


def main():
    """Example usage"""
    print("=" * 60)
    print("Enhanced Progress Tracking System")
    print("=" * 60)
    
    tracker = EnhancedProgressTracker()
    
    if not tracker.driver:
        print("\n⚠️ Neo4j not available. Start with:")
        print("docker-compose -f docker-compose-neo4j.yaml up -d")
        return
    
    # Example: Record quiz result
    quiz = QuizResult(
        quiz_id="quiz_chem_l1_001",
        lesson_id="lesson_01_atomic_structure_and_chemical_bonding",
        student_id="STU001",
        score=8.5,
        max_score=10.0,
        percentage=85.0,
        time_taken_seconds=600,
        questions_correct=17,
        questions_total=20,
        attempted_at=datetime.now().isoformat(),
        completed_at=datetime.now().isoformat(),
        answers=[]
    )
    
    print("\n1. Recording quiz result...")
    tracker.record_quiz_result(quiz)
    
    # Example: Record learning activity
    activity = LearningActivity(
        activity_id=f"act_{datetime.now().timestamp()}",
        student_id="STU001",
        lesson_id="lesson_01_atomic_structure_and_chemical_bonding",
        activity_type=ActivityType.CONTENT_READ,
        duration_seconds=1200,
        timestamp=datetime.now().isoformat(),
        metadata={"section": "atomic_structure"}
    )
    
    print("\n2. Recording learning activity...")
    tracker.record_learning_activity(activity)
    
    # Get mastery metrics
    print("\n3. Calculating mastery metrics...")
    metrics = tracker.calculate_mastery_metrics("STU001", "lesson_01_atomic_structure_and_chemical_bonding")
    
    if metrics:
        print(f"\n   Mastery Level: {metrics.mastery_level.value}")
        print(f"   Mastery Percentage: {metrics.mastery_percentage:.1f}%")
        print(f"   Time Spent: {metrics.total_time_spent_seconds / 60:.1f} minutes")
        print(f"   Activities: {metrics.activities_completed}")
        print(f"   Quiz Average: {metrics.quiz_average:.1f}%")
        print(f"   Problems Solved: {metrics.problems_correct}")
    
    # Get time analytics
    print("\n4. Time-on-task analytics (7 days)...")
    analytics = tracker.get_time_on_task_analytics("STU001", days=7)
    print(f"   Total Time: {analytics.get('total_time_hours', 0):.2f} hours")
    print(f"   Daily Average: {analytics.get('daily_average_minutes', 0):.1f} minutes")
    print(f"   Total Activities: {analytics.get('total_activities', 0)}")
    
    # Get recommendations
    print("\n5. Recommended next lessons...")
    recommendations = tracker.recommend_next_lessons("STU001", count=3)
    for rec in recommendations:
        print(f"   • {rec['subject']}: {rec['title']}")
        print(f"     Reason: {rec['reason']}")
    
    print("\n" + "=" * 60)
    print("✅ Progress Tracking Demo Complete")
    print("=" * 60)
    
    tracker.close()


if __name__ == "__main__":
    main()
