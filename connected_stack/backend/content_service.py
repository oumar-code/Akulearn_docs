# Content Service for Akulearn Backend
# Manages learning materials, study guides, and educational content

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ContentType(Enum):
    STUDY_GUIDE = "study_guide"
    REFERENCE = "reference"
    SUMMARY = "summary"
    EXERCISE = "exercise"

class Difficulty(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class LearningContent:
    id: str
    title: str
    subject: str
    topic: str
    content_type: ContentType
    difficulty: Difficulty
    exam_board: str
    content: str
    estimated_read_time: int  # minutes
    prerequisites: List[str]  # content IDs
    related_questions: List[str]  # question IDs
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    author: str = ""
    version: int = 1

@dataclass
class ContentProgress:
    user_id: str
    content_id: str
    read_status: str  # 'not_started', 'in_progress', 'completed'
    time_spent: int  # seconds
    last_read_at: datetime
    completed_at: Optional[datetime] = None



    # ============================================================================
    # KNOWLEDGE GRAPH INTEGRATION
    # ============================================================================

    def get_knowledge_graph_recommendations(self, student_id: str, subject: str = None) -> Dict[str, Any]:
        """
        Get personalized recommendations from knowledge graph

        Args:
            student_id: Unique student identifier
            subject: Optional subject filter

        Returns:
            Dictionary with recommendations
        """
        try:
            from knowledge_graph_neo4j import AkulearnKnowledgeGraph

            kg = AkulearnKnowledgeGraph()
            student_profile = self.get_student_profile(student_id)

            if not student_profile:
                return {"error": "Student profile not found"}

            # Get recommendations
            recommendations = kg.recommend_content({
                "current_level": student_profile.get("level", "intermediate"),
                "target_subjects": [subject] if subject else student_profile.get("subjects", []),
                "completed_topics": student_profile.get("completed_topics", [])
            })

            # Get prerequisites
            prerequisites = []
            if subject:
                prereqs = kg.find_prerequisites(subject)
                prerequisites = [p["name"] for p in prereqs]

            # Get related topics
            related_topics = kg.find_related_topics(
                [subject] if subject else student_profile.get("subjects", [])
            )

            kg.close()

            return {
                "recommendations": recommendations,
                "prerequisites": prerequisites,
                "related_topics": related_topics,
                "learning_paths": self.get_suggested_learning_paths(student_id)
            }

        except Exception as e:
            return {"error": f"Knowledge graph integration failed: {str(e)}"}

    def get_learning_path_progress(self, student_id: str, path_id: str) -> Dict[str, Any]:
        """
        Get progress on a specific learning path

        Args:
            student_id: Student identifier
            path_id: Learning path identifier

        Returns:
            Progress information
        """
        try:
            from knowledge_graph_neo4j import AkulearnKnowledgeGraph

            kg = AkulearnKnowledgeGraph()
            path_info = kg.get_learning_path(path_id)

            if not path_info:
                return {"error": "Learning path not found"}

            # Calculate progress based on completed topics
            student_profile = self.get_student_profile(student_id)
            completed_topics = set(student_profile.get("completed_topics", []))

            path_subjects = path_info["subjects"]
            total_topics = 0
            completed_count = 0

            # Count topics in path subjects
            for subject in path_subjects:
                subject_topics = kg.subject_hierarchy.get(subject, {}).get("topics", {})
                for topic, subtopics in subject_topics.items():
                    total_topics += len(subtopics)
                    for subtopic in subtopics:
                        if subtopic in completed_topics:
                            completed_count += 1

            progress_percentage = (completed_count / total_topics * 100) if total_topics > 0 else 0

            kg.close()

            return {
                "path_name": path_info["name"],
                "progress_percentage": progress_percentage,
                "completed_topics": completed_count,
                "total_topics": total_topics,
                "remaining_subjects": [s for s in path_subjects if s not in completed_topics],
                "estimated_completion": f"{(total_topics - completed_count) * 2} hours"
            }

        except Exception as e:
            return {"error": f"Progress calculation failed: {str(e)}"}

    def get_suggested_learning_paths(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Suggest appropriate learning paths for a student

        Args:
            student_id: Student identifier

        Returns:
            List of suggested learning paths
        """
        student_profile = self.get_student_profile(student_id)
        if not student_profile:
            return []

        student_level = student_profile.get("level", "intermediate")
        target_goals = student_profile.get("goals", [])

        # Simple rule-based suggestions
        suggestions = []

        if "waec" in target_goals or "examination" in target_goals:
            if student_level in ["intermediate", "advanced"]:
                suggestions.append({
                    "path_id": "waec_science_track",
                    "name": "WAEC Science Track",
                    "reason": "Comprehensive preparation for WAEC science subjects"
                })

        if "engineering" in target_goals:
            suggestions.append({
                "path_id": "engineering_foundation",
                "name": "Engineering Foundation",
                "reason": "Essential preparation for engineering studies"
            })

        if "medical" in target_goals or "health" in target_goals:
            suggestions.append({
                "path_id": "medical_sciences",
                "name": "Medical Sciences",
                "reason": "Foundation for medical and health sciences"
            })

        return suggestions

    def get_student_profile(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student profile (placeholder - integrate with actual student service)

        Args:
            student_id: Student identifier

        Returns:
            Student profile dictionary
        """
        # Placeholder implementation
        # In real implementation, this would fetch from student database
        return {
            "id": student_id,
            "level": "intermediate",
            "subjects": ["Mathematics", "Physics", "Chemistry"],
            "completed_topics": ["Basic Algebra", "Mechanics"],
            "goals": ["waec", "engineering"],
            "preferences": ["visual_learning", "practice_problems"]
        }


class ContentService:
    """
    Manages learning content for the Akulearn platform.
    Provides content storage, retrieval, and progress tracking.
    """

    def __init__(self):
        self.content_db: Dict[str, LearningContent] = {}
        self.progress_db: Dict[str, Dict[str, ContentProgress]] = {}  # user_id -> content_id -> progress
        self.data_file = os.path.join(os.path.dirname(__file__), 'content_data.json')
        self._load_content()

    def _load_content(self):
        """Load content from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Load content
                for content_data in data.get('content', []):
                    # Convert string timestamps back to datetime
                    content_data['created_at'] = datetime.fromisoformat(content_data['created_at'])
                    content_data['updated_at'] = datetime.fromisoformat(content_data['updated_at'])

                    # Convert enums
                    content_data['content_type'] = ContentType(content_data['content_type'])
                    content_data['difficulty'] = Difficulty(content_data['difficulty'])

                    content = LearningContent(**content_data)
                    self.content_db[content.id] = content

                # Load progress
                for user_id, progress_data in data.get('progress', {}).items():
                    self.progress_db[user_id] = {}
                    for content_id, prog_data in progress_data.items():
                        prog_data['last_read_at'] = datetime.fromisoformat(prog_data['last_read_at'])
                        if prog_data.get('completed_at'):
                            prog_data['completed_at'] = datetime.fromisoformat(prog_data['completed_at'])
                        self.progress_db[user_id][content_id] = ContentProgress(**prog_data)

            else:
                self._initialize_sample_content()
        except Exception as e:
            print(f"Error loading content data: {e}")
            self._initialize_sample_content()

    def _save_content(self):
        """Save content to JSON file"""
        try:
            data = {
                'content': [],
                'progress': {}
            }

            # Save content
            for content in self.content_db.values():
                content_dict = asdict(content)
                # Convert datetime to ISO format
                content_dict['created_at'] = content.created_at.isoformat()
                content_dict['updated_at'] = content.updated_at.isoformat()
                # Convert enums to strings
                content_dict['content_type'] = content.content_type.value
                content_dict['difficulty'] = content.difficulty.value
                data['content'].append(content_dict)

            # Save progress
            for user_id, user_progress in self.progress_db.items():
                data['progress'][user_id] = {}
                for content_id, progress in user_progress.items():
                    prog_dict = asdict(progress)
                    prog_dict['last_read_at'] = progress.last_read_at.isoformat()
                    if progress.completed_at:
                        prog_dict['completed_at'] = progress.completed_at.isoformat()
                    data['progress'][user_id][content_id] = prog_dict

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Error saving content data: {e}")

    def _initialize_sample_content(self):
        """Create sample content for demonstration"""

    def _initialize_sample_content(self):
        """Create sample content for demonstration"""
        # Mathematics - Algebra Study Guide
        algebra_guide = LearningContent(
            id="math_algebra_guide_001",
            title="Introduction to Quadratic Equations",
            subject="Mathematics",
            topic="Algebra",
            content_type=ContentType.STUDY_GUIDE,
            difficulty=Difficulty.INTERMEDIATE,
            exam_board="WAEC",
            content="""
# Quadratic Equations

## Learning Objectives
By the end of this guide, you should be able to:
- Define quadratic equations
- Solve quadratic equations using different methods
- Apply quadratic equations to real-world problems

## What is a Quadratic Equation?

A quadratic equation is a polynomial equation of degree 2, with the general form:
**ax² + bx + c = 0**

Where:
- **a** ≠ 0 (coefficient of x²)
- **b** = coefficient of x
- **c** = constant term

### Examples of Quadratic Equations:
- x² + 5x + 6 = 0
- 2x² - 7x + 3 = 0
- x² = 10

## Methods of Solving Quadratic Equations

### 1. Factorization Method
Express the quadratic as a product of two binomials.

**Example:** Solve x² + 5x + 6 = 0
- Find factors of 6 that add to 5: 2 and 3
- (x + 2)(x + 3) = 0
- x = -2 or x = -3

### 2. Quadratic Formula
For ax² + bx + c = 0, the solutions are:
**x = [-b ± √(b² - 4ac)] / 2a**

**Example:** Solve x² - 5x + 6 = 0
- a = 1, b = -5, c = 6
- x = [5 ± √(25 - 24)] / 2
- x = [5 ± √1] / 2
- x = [5 ± 1] / 2
- x = 3 or x = 2

### 3. Completing the Square
Rewrite the equation in the form (x + h)² = k

**Example:** Solve x² + 6x + 5 = 0
- x² + 6x = -5
- x² + 6x + 9 = -5 + 9
- (x + 3)² = 4
- x + 3 = ±2
- x = -3 ± 2
- x = -1 or x = -5

## Applications of Quadratic Equations

### 1. Projectile Motion
The height of a projectile is given by: h = -16t² + v₀t + h₀

### 2. Area Problems
Finding dimensions when area is given.

### 3. Revenue Optimization
Finding maximum profit: Revenue = price × quantity

## Common Mistakes to Avoid

1. **Forgetting the ± sign** in quadratic formula
2. **Incorrect discriminant calculation**
3. **Not checking solutions** by substitution
4. **Division by zero** (a ≠ 0)

## Practice Problems

1. Solve: x² - 7x + 12 = 0
2. Solve: 2x² + 5x - 3 = 0
3. Find the roots: x² - 4x - 5 = 0

## Exam Tips

- Always show your working clearly
- Check your answers by substitution
- Use the most efficient method for each problem
- Practice different types of quadratic equations
            """,
            estimated_read_time=15,
            prerequisites=[],
            related_questions=["waec_math_2020_001", "waec_math_2021_045"],
            tags=["algebra", "quadratic", "equations", "factorization", "formula"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Mathematics Expert",
            version=1
        )

        # Physics - Mechanics Reference
        mechanics_ref = LearningContent(
            id="physics_mechanics_ref_001",
            title="Newton's Laws Quick Reference",
            subject="Physics",
            topic="Mechanics",
            content_type=ContentType.REFERENCE,
            difficulty=Difficulty.BASIC,
            exam_board="WAEC",
            content="""
# Newton's Laws of Motion

## First Law (Law of Inertia)
**An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction unless acted upon by an unbalanced force.**

- Also called: Law of Inertia
- Inertia = resistance to change in motion
- Measured by: mass

## Second Law (F = ma)
**Force equals mass times acceleration.**
**F = ma**

- Force is measured in Newtons (N)
- Mass is measured in kilograms (kg)
- Acceleration is measured in m/s²
- 1 N = 1 kg·m/s²

## Third Law (Action-Reaction)
**For every action, there is an equal and opposite reaction.**

- Forces always come in pairs
- Equal magnitude, opposite direction
- Same type of force

## Key Formulas
- **Weight:** W = mg
- **Friction:** f ≤ μN
- **Momentum:** p = mv
- **Impulse:** J = FΔt = Δp

## Important Notes
- Net force = sum of all forces
- Balanced forces = no acceleration
- Unbalanced forces = acceleration
- Free-body diagrams help visualize forces
            """,
            estimated_read_time=5,
            prerequisites=[],
            related_questions=["waec_physics_2020_012", "waec_physics_2021_023"],
            tags=["physics", "mechanics", "newton", "laws", "motion"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Physics Expert",
            version=1
        )

        # English - Summary
        english_summary = LearningContent(
            id="english_grammar_summary_001",
            title="Parts of Speech Summary",
            subject="English Language",
            topic="Grammar",
            content_type=ContentType.SUMMARY,
            difficulty=Difficulty.BASIC,
            exam_board="WAEC",
            content="""
# Parts of Speech

## Nouns
- **Common nouns:** book, city, teacher
- **Proper nouns:** Lagos, Nigeria, Shakespeare
- **Abstract nouns:** love, freedom, happiness
- **Collective nouns:** team, family, crowd

## Pronouns
- **Personal:** I, you, he, she, it, we, they
- **Possessive:** my, your, his, her, its, our, their
- **Reflexive:** myself, yourself, himself, herself
- **Demonstrative:** this, that, these, those

## Verbs
- **Action verbs:** run, eat, sleep
- **Linking verbs:** be, seem, appear
- **Helping verbs:** is, are, was, were, has, have

## Adjectives
- **Descriptive:** big, small, beautiful
- **Quantitative:** some, many, few
- **Demonstrative:** this, that, these, those

## Adverbs
- **Manner:** quickly, slowly, carefully
- **Time:** now, then, yesterday
- **Place:** here, there, everywhere

## Prepositions
- **Time:** at, on, in, during, before, after
- **Place:** in, on, at, under, over, beside
- **Direction:** to, from, towards, through

## Conjunctions
- **Coordinating:** and, but, or, so, yet, for
- **Subordinating:** because, although, if, when, since

## Interjections
- Express emotion: oh!, wow!, hey!, ouch!

## Exam Focus
- Identify parts of speech in sentences
- Use correct grammar in writing
- Understand word classes for comprehension
            """,
            estimated_read_time=8,
            prerequisites=[],
            related_questions=["waec_english_2020_005", "waec_english_2021_018"],
            tags=["english", "grammar", "parts", "speech", "vocabulary"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="English Expert",
            version=1
        )

        # Store sample content
        self.content_db = {
            algebra_guide.id: algebra_guide,
            mechanics_ref.id: mechanics_ref,
            english_summary.id: english_summary
        }

    def get_subjects(self) -> List[str]:
        """Get list of all subjects"""
        return list(set(content.subject for content in self.content_db.values()))

    def get_topics_by_subject(self, subject: str) -> List[str]:
        """Get topics for a specific subject"""
        return list(set(
            content.topic for content in self.content_db.values()
            if content.subject == subject
        ))

    def get_content_by_subject_topic(self, subject: str, topic: str) -> List[LearningContent]:
        """Get all content for a subject-topic combination"""
        return [
            content for content in self.content_db.values()
            if content.subject == subject and content.topic == topic
        ]

    def get_content_by_id(self, content_id: str) -> Optional[LearningContent]:
        """Get specific content by ID"""
        return self.content_db.get(content_id)

    def search_content(self, query: str, subject: str = None, content_type: str = None) -> List[LearningContent]:
        """Search content by keyword"""
        results = []
        query_lower = query.lower()

        for content in self.content_db.values():
            if subject and content.subject != subject:
                continue
            if content_type and content.content_type.value != content_type:
                continue

            # Search in title, content, and tags
            searchable_text = (
                content.title + " " +
                content.content + " " +
                " ".join(content.tags)
            ).lower()

            if query_lower in searchable_text:
                results.append(content)

        return results

    def get_recommendations(self, user_id: str, subject: str = None, limit: int = 10) -> List[LearningContent]:
        """Get personalized content recommendations"""
        # For MVP, return recent content or by subject
        if subject:
            content_list = [
                content for content in self.content_db.values()
                if content.subject == subject
            ]
        else:
            content_list = list(self.content_db.values())

        # Sort by creation date (most recent first)
        content_list.sort(key=lambda x: x.created_at, reverse=True)
        return content_list[:limit]

    def update_progress(self, user_id: str, content_id: str, time_spent: int, completed: bool = False):
        """Update user progress on content"""
        if user_id not in self.progress_db:
            self.progress_db[user_id] = {}

        progress = self.progress_db[user_id].get(content_id)
        if not progress:
            progress = ContentProgress(
                user_id=user_id,
                content_id=content_id,
                read_status="not_started",
                time_spent=0,
                last_read_at=datetime.now()
            )

        progress.time_spent += time_spent
        progress.last_read_at = datetime.now()

        if completed and progress.read_status != "completed":
            progress.read_status = "completed"
            progress.completed_at = datetime.now()
        elif progress.time_spent > 0 and progress.read_status == "not_started":
            progress.read_status = "in_progress"

        self.progress_db[user_id][content_id] = progress

    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's content progress summary"""
        if user_id not in self.progress_db:
            return {
                "total_content_viewed": 0,
                "total_time_spent": 0,
                "completed_content": 0,
                "content_progress": {}
            }

        user_progress = self.progress_db[user_id]
        total_time = sum(p.time_spent for p in user_progress.values())
        completed_count = sum(1 for p in user_progress.values() if p.read_status == "completed")

        return {
            "total_content_viewed": len(user_progress),
            "total_time_spent": total_time,
            "completed_content": completed_count,
            "content_progress": {
                content_id: {
                    "status": progress.read_status,
                    "time_spent": progress.time_spent,
                    "completed_at": progress.completed_at.isoformat() if progress.completed_at else None
                }
                for content_id, progress in user_progress.items()
            }
        }

    def get_content_stats(self) -> Dict[str, Any]:
        """Get content statistics"""
        subjects = {}
        content_types = {}

        for content in self.content_db.values():
            # Count by subject
            if content.subject not in subjects:
                subjects[content.subject] = 0
            subjects[content.subject] += 1

            # Count by content type
            ct_key = content.content_type.value
            if ct_key not in content_types:
                content_types[ct_key] = 0
            content_types[ct_key] += 1

        return {
            "total_content": len(self.content_db),
            "subjects": subjects,
            "content_types": content_types,
            "last_updated": max(c.updated_at for c in self.content_db.values()).isoformat()
        }

    def add_content(self, content_data: Dict[str, Any]) -> bool:
        """Add new content to the database"""
        try:
            # Convert string enums to proper enum objects
            content_type = ContentType(content_data['content_type'])
            difficulty = Difficulty(content_data['difficulty'])

            # Parse timestamps
            created_at = datetime.fromisoformat(content_data.get('created_at', datetime.now().isoformat()))
            updated_at = datetime.fromisoformat(content_data.get('updated_at', datetime.now().isoformat()))

            # Create LearningContent object
            content = LearningContent(
                id=content_data['id'],
                title=content_data['title'],
                subject=content_data['subject'],
                topic=content_data['topic'],
                content_type=content_type,
                difficulty=difficulty,
                exam_board=content_data['exam_board'],
                content=content_data['content'],
                estimated_read_time=content_data.get('estimated_read_time', 10),
                prerequisites=content_data.get('prerequisites', []),
                related_questions=content_data.get('related_questions', []),
                tags=content_data.get('tags', []),
                created_at=created_at,
                updated_at=updated_at,
                author=content_data.get('author', ''),
                version=content_data.get('version', 1)
            )

            # Store in database
            self.content_db[content.id] = content
            self._save_content()  # Persist changes
            return True

        except Exception as e:
            print(f"Error adding content: {e}")
            return False


# Global content service instance
content_service = ContentService()