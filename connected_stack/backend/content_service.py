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

class ContentService:
    """
    Manages learning content for the Akulearn platform.
    Provides content storage, retrieval, and progress tracking.
    """

    def __init__(self):
        self.content_db: Dict[str, LearningContent] = {}
        self.progress_db: Dict[str, Dict[str, ContentProgress]] = {}  # user_id -> content_id -> progress
        self._load_content()

    def _load_content(self):
        """Load content from JSON files or database"""
        # For MVP, we'll use in-memory storage
        # In production, this would load from database
        self._initialize_sample_content()

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


# Global content service instance
content_service = ContentService()