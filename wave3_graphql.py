#!/usr/bin/env python3
"""
Wave 3 GraphQL API
Provides flexible querying with GraphQL for complex data requirements
"""

import graphene
from graphene import ObjectType, String, Int, Float, List, Field, Boolean, Enum
from typing import Optional
import json
from pathlib import Path


# Enums
class MasteryLevelEnum(Enum):
    NOT_STARTED = "Not Started"
    NOVICE = "Novice"
    DEVELOPING = "Developing"
    PROFICIENT = "Proficient"
    ADVANCED = "Advanced"
    MASTERED = "Mastered"


class SubjectEnum(Enum):
    CHEMISTRY = "Chemistry"
    BIOLOGY = "Biology"
    COMPUTER_SCIENCE = "Computer Science"
    ECONOMICS = "Economics"
    ENGLISH_LANGUAGE = "English Language"
    GEOGRAPHY = "Geography"
    HISTORY = "History"


# Types
class LearningObjectiveType(ObjectType):
    """Learning objective within a lesson"""
    objective = String()
    bloom_level = String()


class ContentSectionType(ObjectType):
    """Content section within a lesson"""
    title = String()
    content = String()
    subsections = List(String)


class WorkedExampleType(ObjectType):
    """Worked example in a lesson"""
    title = String()
    problem = String()
    solution = String()
    explanation = String()


class PracticeProblemType(ObjectType):
    """Practice problem in a lesson"""
    problem = String()
    difficulty = String()
    hints = List(String)


class GlossaryTermType(ObjectType):
    """Glossary term definition"""
    term = String()
    definition = String()


class ResourceType(ObjectType):
    """Additional resource"""
    title = String()
    type = String()
    url = String()
    description = String()


class AssessmentType(ObjectType):
    """Assessment information"""
    formative_questions = List(String)
    summative_questions = List(String)


class LessonType(ObjectType):
    """Complete lesson object"""
    id = String()
    title = String()
    subject = String()
    grade_level = String()
    term = String()
    week = Int()
    duration = Int()
    
    # Curriculum alignment
    nerdc_code = String()
    waec_topics = List(String)
    
    # Content
    introduction = String()
    learning_objectives = List(LearningObjectiveType)
    content_sections = List(ContentSectionType)
    worked_examples = List(WorkedExampleType)
    practice_problems = List(PracticeProblemType)
    glossary = List(GlossaryTermType)
    resources = List(ResourceType)
    assessment = Field(AssessmentType)
    
    # Metadata
    prerequisites = List(String)
    connections = List(String)
    
    @staticmethod
    def resolve_lesson(lesson_id):
        """Load lesson from file"""
        try:
            lesson_file = Path("rendered_lessons") / f"{lesson_id}.json"
            if lesson_file.exists():
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None


class MasteryMetricsType(ObjectType):
    """Student mastery metrics for a lesson"""
    lesson_id = String()
    mastery_level = Field(MasteryLevelEnum)
    mastery_percentage = Float()
    quiz_score_percentage = Float()
    problems_completed_percentage = Float()
    engagement_score = Float()
    time_spent_minutes = Float()


class ProgressOverviewType(ObjectType):
    """Student progress overview"""
    student_id = String()
    total_lessons = Int()
    completed_lessons = Int()
    in_progress_lessons = Int()
    average_mastery = Float()
    total_time_hours = Float()
    total_quizzes_taken = Int()
    achievements_count = Int()


class RecommendationType(ObjectType):
    """Lesson recommendation"""
    lesson_id = String()
    title = String()
    subject = String()
    score = Float()
    reason = String()


class LearningPathType(ObjectType):
    """Thematic learning path"""
    path_id = String()
    name = String()
    description = String()
    lessons = List(String)
    duration_weeks = Int()
    skills = List(String)


class AchievementType(ObjectType):
    """Student achievement"""
    achievement_id = String()
    title = String()
    description = String()
    points = Int()
    unlocked_at = String()
    category = String()


class LeaderboardEntryType(ObjectType):
    """Leaderboard entry"""
    rank = Int()
    student_id = String()
    student_name = String()
    total_points = Int()
    achievements_count = Int()
    mastery_average = Float()


# Query Root
class Query(ObjectType):
    """GraphQL query root"""
    
    # Lesson queries
    lesson = Field(LessonType, lesson_id=String(required=True))
    lessons_by_subject = List(LessonType, subject=String(required=True))
    all_lessons = List(LessonType)
    search_lessons = List(LessonType, keyword=String(required=True))
    
    # Progress queries
    student_progress = Field(ProgressOverviewType, student_id=String(required=True))
    lesson_mastery = Field(MasteryMetricsType, 
                          student_id=String(required=True), 
                          lesson_id=String(required=True))
    
    # Recommendation queries
    recommendations = List(RecommendationType, 
                          student_id=String(required=True), 
                          count=Int(default_value=5))
    
    # Learning path queries
    learning_paths = List(LearningPathType)
    learning_path = Field(LearningPathType, path_id=String(required=True))
    
    # Gamification queries
    student_achievements = List(AchievementType, student_id=String(required=True))
    leaderboard = List(LeaderboardEntryType, limit=Int(default_value=10))
    
    # Resolvers
    def resolve_lesson(self, info, lesson_id):
        """Get a specific lesson"""
        data = LessonType.resolve_lesson(lesson_id)
        if data:
            return LessonType(**data)
        return None
    
    def resolve_lessons_by_subject(self, info, subject):
        """Get all lessons for a subject"""
        lessons = []
        rendered_dir = Path("rendered_lessons")
        if rendered_dir.exists():
            for lesson_file in rendered_dir.glob("lesson_*.json"):
                try:
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get("subject") == subject:
                            lessons.append(LessonType(**data))
                except Exception:
                    continue
        return lessons
    
    def resolve_all_lessons(self, info):
        """Get all lessons"""
        lessons = []
        rendered_dir = Path("rendered_lessons")
        if rendered_dir.exists():
            for lesson_file in rendered_dir.glob("lesson_*.json"):
                try:
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        lessons.append(LessonType(**data))
                except Exception:
                    continue
        return lessons
    
    def resolve_search_lessons(self, info, keyword):
        """Search lessons by keyword"""
        lessons = []
        keyword_lower = keyword.lower()
        rendered_dir = Path("rendered_lessons")
        if rendered_dir.exists():
            for lesson_file in rendered_dir.glob("lesson_*.json"):
                try:
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Search in title, introduction, and content
                        searchable = f"{data.get('title', '')} {data.get('introduction', '')}".lower()
                        if keyword_lower in searchable:
                            lessons.append(LessonType(**data))
                except Exception:
                    continue
        return lessons
    
    def resolve_student_progress(self, info, student_id):
        """Get student progress overview"""
        try:
            from enhanced_progress_tracker import EnhancedProgressTracker
            tracker = EnhancedProgressTracker()
            overview = tracker.get_student_mastery_overview(student_id)
            return ProgressOverviewType(
                student_id=student_id,
                total_lessons=overview.get("total_lessons", 0),
                completed_lessons=overview.get("completed_lessons", 0),
                in_progress_lessons=overview.get("in_progress_lessons", 0),
                average_mastery=overview.get("average_mastery", 0),
                total_time_hours=overview.get("total_time_hours", 0),
                total_quizzes_taken=overview.get("total_quizzes_taken", 0),
                achievements_count=overview.get("achievements_count", 0)
            )
        except Exception:
            return None
    
    def resolve_lesson_mastery(self, info, student_id, lesson_id):
        """Get mastery metrics for a specific lesson"""
        try:
            from enhanced_progress_tracker import EnhancedProgressTracker
            tracker = EnhancedProgressTracker()
            metrics = tracker.calculate_mastery_metrics(student_id, lesson_id)
            return MasteryMetricsType(
                lesson_id=lesson_id,
                mastery_level=metrics.mastery_level.value,
                mastery_percentage=metrics.mastery_percentage,
                quiz_score_percentage=metrics.quiz_score_percentage,
                problems_completed_percentage=metrics.problems_completed_percentage,
                engagement_score=metrics.engagement_score,
                time_spent_minutes=metrics.time_spent_minutes
            )
        except Exception:
            return None
    
    def resolve_recommendations(self, info, student_id, count):
        """Get lesson recommendations"""
        try:
            from wave3_recommendation_engine import RecommendationEngine
            engine = RecommendationEngine()
            recs = engine.get_hybrid_recommendations(student_id, count)
            return [RecommendationType(**rec) for rec in recs]
        except Exception:
            return []
    
    def resolve_learning_paths(self, info):
        """Get all learning paths"""
        try:
            from cross_subject_expander import CrossSubjectExpander
            expander = CrossSubjectExpander()
            return [LearningPathType(
                path_id=path.path_id,
                name=path.name,
                description=path.description,
                lessons=path.lessons,
                duration_weeks=path.duration_weeks,
                skills=[skill.value for skill in path.skills]
            ) for path in expander.learning_paths]
        except Exception:
            return []
    
    def resolve_learning_path(self, info, path_id):
        """Get specific learning path"""
        try:
            from cross_subject_expander import CrossSubjectExpander
            expander = CrossSubjectExpander()
            for path in expander.learning_paths:
                if path.path_id == path_id:
                    return LearningPathType(
                        path_id=path.path_id,
                        name=path.name,
                        description=path.description,
                        lessons=path.lessons,
                        duration_weeks=path.duration_weeks,
                        skills=[skill.value for skill in path.skills]
                    )
        except Exception:
            pass
        return None
    
    def resolve_student_achievements(self, info, student_id):
        """Get student achievements"""
        try:
            from wave3_gamification import GamificationEngine
            engine = GamificationEngine()
            achievements = engine.get_student_achievements(student_id)
            return [AchievementType(**ach) for ach in achievements]
        except Exception:
            return []
    
    def resolve_leaderboard(self, info, limit):
        """Get leaderboard"""
        try:
            from wave3_gamification import GamificationEngine
            engine = GamificationEngine()
            leaderboard = engine.get_leaderboard(limit)
            return [LeaderboardEntryType(**entry) for entry in leaderboard]
        except Exception:
            return []


# Create schema
schema = graphene.Schema(query=Query)


if __name__ == "__main__":
    print("GraphQL schema created successfully!")
    print("\nExample queries:")
    print("""
# Get lesson
query {
  lesson(lessonId: "lesson_01_atomic_structure_and_chemical_bonding") {
    title
    subject
    introduction
    learningObjectives {
      objective
      bloomLevel
    }
  }
}

# Get student progress
query {
  studentProgress(studentId: "STU001") {
    totalLessons
    completedLessons
    averageMastery
  }
}

# Get recommendations
query {
  recommendations(studentId: "STU001", count: 5) {
    lessonId
    title
    score
    reason
  }
}
    """)
