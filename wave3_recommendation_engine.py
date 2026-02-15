#!/usr/bin/env python3
"""
Wave 3 Recommendation Engine
Implements collaborative filtering, content-based, and hybrid recommendation approaches
"""

import json
from typing import List, Dict, Tuple
from pathlib import Path
from collections import defaultdict
import math


class RecommendationEngine:
    """Intelligent lesson recommendation system"""
    
    def __init__(self):
        self.lessons_cache = {}
        self.student_interactions = defaultdict(dict)  # student_id -> {lesson_id: score}
        self.lesson_features = {}  # lesson_id -> feature_vector
        self._load_lessons()
        self._extract_lesson_features()
    
    def _load_lessons(self):
        """Load all lessons"""
        rendered_dir = Path("rendered_lessons")
        if rendered_dir.exists():
            for lesson_file in rendered_dir.glob("lesson_*.json"):
                try:
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.lessons_cache[data['id']] = data
                except Exception:
                    continue
    
    def _extract_lesson_features(self):
        """Extract features from lessons for content-based filtering"""
        for lesson_id, lesson in self.lessons_cache.items():
            features = {
                'subject': lesson.get('subject', ''),
                'grade_level': lesson.get('grade_level', ''),
                'topics': set(),
                'skills': set(),
                'difficulty': self._estimate_difficulty(lesson),
                'duration': lesson.get('duration', 60)
            }
            
            # Extract topics from content
            intro = lesson.get('introduction', '').lower()
            for section in lesson.get('content_sections', []):
                intro += ' ' + section.get('content', '').lower()
            
            # Extract key terms
            for term in lesson.get('glossary', []):
                features['topics'].add(term.get('term', '').lower())
            
            # Extract skills from objectives
            for obj in lesson.get('learning_objectives', []):
                bloom_level = obj.get('bloom_level', '')
                if bloom_level:
                    features['skills'].add(bloom_level.lower())
            
            self.lesson_features[lesson_id] = features
    
    def _estimate_difficulty(self, lesson: dict) -> float:
        """Estimate lesson difficulty (0-1 scale)"""
        difficulty = 0.5  # Default medium
        
        # More worked examples = easier
        worked_examples = len(lesson.get('worked_examples', []))
        if worked_examples > 3:
            difficulty -= 0.1
        elif worked_examples < 2:
            difficulty += 0.1
        
        # More practice problems = harder
        practice_problems = len(lesson.get('practice_problems', []))
        if practice_problems > 5:
            difficulty += 0.1
        
        # Advanced bloom levels = harder
        for obj in lesson.get('learning_objectives', []):
            bloom = obj.get('bloom_level', '').lower()
            if bloom in ['analyze', 'evaluate', 'create']:
                difficulty += 0.05
        
        return max(0.0, min(1.0, difficulty))
    
    def record_interaction(self, student_id: str, lesson_id: str, score: float):
        """Record student interaction with a lesson (0-1 scale)"""
        self.student_interactions[student_id][lesson_id] = score
    
    def get_content_based_recommendations(self, student_id: str, count: int = 5) -> List[Dict]:
        """Content-based recommendations based on lesson similarity"""
        recommendations = []
        
        # Get student's completed lessons
        completed = self.student_interactions.get(student_id, {})
        if not completed:
            # Cold start: recommend popular/introductory lessons
            return self._get_cold_start_recommendations(count)
        
        # Calculate average feature vector from completed lessons
        avg_features = self._get_student_profile(student_id)
        
        # Find similar lessons
        candidates = []
        for lesson_id, lesson_features in self.lesson_features.items():
            if lesson_id in completed:
                continue  # Skip already completed
            
            similarity = self._calculate_content_similarity(avg_features, lesson_features)
            candidates.append((lesson_id, similarity))
        
        # Sort by similarity
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Build recommendations
        for lesson_id, similarity in candidates[:count]:
            lesson = self.lessons_cache.get(lesson_id)
            if lesson:
                recommendations.append({
                    'lesson_id': lesson_id,
                    'title': lesson.get('title'),
                    'subject': lesson.get('subject'),
                    'score': similarity,
                    'reason': f"Similar to lessons you've completed ({similarity:.0%} match)"
                })
        
        return recommendations
    
    def get_collaborative_recommendations(self, student_id: str, count: int = 5) -> List[Dict]:
        """Collaborative filtering based on similar students"""
        recommendations = []
        
        # Get student's completed lessons
        student_completed = self.student_interactions.get(student_id, {})
        if not student_completed:
            return self._get_cold_start_recommendations(count)
        
        # Find similar students
        similar_students = self._find_similar_students(student_id)
        
        # Aggregate recommendations from similar students
        candidate_scores = defaultdict(float)
        candidate_counts = defaultdict(int)
        
        for similar_student_id, similarity in similar_students[:10]:  # Top 10 similar
            their_lessons = self.student_interactions.get(similar_student_id, {})
            for lesson_id, score in their_lessons.items():
                if lesson_id not in student_completed:
                    candidate_scores[lesson_id] += score * similarity
                    candidate_counts[lesson_id] += 1
        
        # Calculate average scores
        candidates = []
        for lesson_id, total_score in candidate_scores.items():
            avg_score = total_score / candidate_counts[lesson_id]
            candidates.append((lesson_id, avg_score))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Build recommendations
        for lesson_id, score in candidates[:count]:
            lesson = self.lessons_cache.get(lesson_id)
            if lesson:
                recommendations.append({
                    'lesson_id': lesson_id,
                    'title': lesson.get('title'),
                    'subject': lesson.get('subject'),
                    'score': score,
                    'reason': f"Students like you also studied this ({score:.0%} confidence)"
                })
        
        return recommendations
    
    def get_hybrid_recommendations(self, student_id: str, count: int = 5) -> List[Dict]:
        """Hybrid approach combining content-based and collaborative filtering"""
        # Get recommendations from both methods
        content_recs = self.get_content_based_recommendations(student_id, count * 2)
        collab_recs = self.get_collaborative_recommendations(student_id, count * 2)
        
        # Combine with weights (60% content, 40% collaborative)
        combined_scores = defaultdict(lambda: {'score': 0, 'count': 0, 'lesson': None})
        
        for rec in content_recs:
            lesson_id = rec['lesson_id']
            combined_scores[lesson_id]['score'] += rec['score'] * 0.6
            combined_scores[lesson_id]['count'] += 1
            combined_scores[lesson_id]['lesson'] = rec
        
        for rec in collab_recs:
            lesson_id = rec['lesson_id']
            combined_scores[lesson_id]['score'] += rec['score'] * 0.4
            combined_scores[lesson_id]['count'] += 1
            if not combined_scores[lesson_id]['lesson']:
                combined_scores[lesson_id]['lesson'] = rec
        
        # Sort by combined score
        candidates = [(lid, data['score'], data['lesson']) 
                     for lid, data in combined_scores.items() if data['lesson']]
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Build final recommendations with hybrid reasoning
        recommendations = []
        for lesson_id, score, lesson_data in candidates[:count]:
            recommendations.append({
                'lesson_id': lesson_id,
                'title': lesson_data['title'],
                'subject': lesson_data['subject'],
                'score': score,
                'reason': f"Recommended based on your learning pattern (confidence: {score:.0%})"
            })
        
        return recommendations
    
    def get_prerequisite_aware_recommendations(self, student_id: str, count: int = 5) -> List[Dict]:
        """Recommendations that respect prerequisite relationships"""
        recommendations = []
        
        # Get completed lessons
        completed = set(self.student_interactions.get(student_id, {}).keys())
        
        # Find lessons where prerequisites are met
        candidates = []
        for lesson_id, lesson in self.lessons_cache.items():
            if lesson_id in completed:
                continue
            
            prerequisites = lesson.get('prerequisites', [])
            prerequisites_met = all(prereq in completed for prereq in prerequisites)
            
            if prerequisites_met:
                # Calculate readiness score
                readiness = 1.0 if not prerequisites else 0.8
                candidates.append((lesson_id, readiness))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        for lesson_id, readiness in candidates[:count]:
            lesson = self.lessons_cache.get(lesson_id)
            if lesson:
                recommendations.append({
                    'lesson_id': lesson_id,
                    'title': lesson.get('title'),
                    'subject': lesson.get('subject'),
                    'score': readiness,
                    'reason': "You're ready for this lesson (prerequisites completed)"
                })
        
        return recommendations
    
    def _get_student_profile(self, student_id: str) -> Dict:
        """Build student profile from completed lessons"""
        completed = self.student_interactions.get(student_id, {})
        
        profile = {
            'subjects': defaultdict(float),
            'topics': defaultdict(float),
            'skills': defaultdict(float),
            'avg_difficulty': 0.0,
            'avg_duration': 0.0
        }
        
        if not completed:
            return profile
        
        total_weight = sum(completed.values())
        for lesson_id, score in completed.items():
            features = self.lesson_features.get(lesson_id, {})
            weight = score / total_weight
            
            profile['subjects'][features.get('subject', '')] += weight
            profile['avg_difficulty'] += features.get('difficulty', 0.5) * weight
            profile['avg_duration'] += features.get('duration', 60) * weight
            
            for topic in features.get('topics', set()):
                profile['topics'][topic] += weight
            
            for skill in features.get('skills', set()):
                profile['skills'][skill] += weight
        
        return profile
    
    def _calculate_content_similarity(self, profile: Dict, lesson_features: Dict) -> float:
        """Calculate similarity between student profile and lesson"""
        similarity = 0.0
        
        # Subject match (30% weight)
        if lesson_features.get('subject') in profile.get('subjects', {}):
            similarity += 0.3 * profile['subjects'][lesson_features['subject']]
        
        # Topic overlap (40% weight)
        lesson_topics = lesson_features.get('topics', set())
        profile_topics = set(profile.get('topics', {}).keys())
        if lesson_topics and profile_topics:
            topic_overlap = len(lesson_topics & profile_topics) / len(lesson_topics | profile_topics)
            similarity += 0.4 * topic_overlap
        
        # Skill match (20% weight)
        lesson_skills = lesson_features.get('skills', set())
        profile_skills = set(profile.get('skills', {}).keys())
        if lesson_skills and profile_skills:
            skill_overlap = len(lesson_skills & profile_skills) / len(lesson_skills | profile_skills)
            similarity += 0.2 * skill_overlap
        
        # Difficulty match (10% weight)
        lesson_difficulty = lesson_features.get('difficulty', 0.5)
        profile_difficulty = profile.get('avg_difficulty', 0.5)
        difficulty_match = 1.0 - abs(lesson_difficulty - profile_difficulty)
        similarity += 0.1 * difficulty_match
        
        return similarity
    
    def _find_similar_students(self, student_id: str) -> List[Tuple[str, float]]:
        """Find students with similar learning patterns"""
        student_lessons = self.student_interactions.get(student_id, {})
        if not student_lessons:
            return []
        
        similarities = []
        for other_id, other_lessons in self.student_interactions.items():
            if other_id == student_id:
                continue
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(student_lessons, other_lessons)
            if similarity > 0:
                similarities.append((other_id, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
    
    def _cosine_similarity(self, dict1: Dict[str, float], dict2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two interaction dictionaries"""
        common_keys = set(dict1.keys()) & set(dict2.keys())
        if not common_keys:
            return 0.0
        
        dot_product = sum(dict1[k] * dict2[k] for k in common_keys)
        magnitude1 = math.sqrt(sum(v**2 for v in dict1.values()))
        magnitude2 = math.sqrt(sum(v**2 for v in dict2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _get_cold_start_recommendations(self, count: int) -> List[Dict]:
        """Recommendations for new students with no history"""
        recommendations = []
        
        # Recommend introductory lessons from various subjects
        intro_keywords = ['introduction', 'basic', 'fundamentals', 'overview']
        
        candidates = []
        for lesson_id, lesson in self.lessons_cache.items():
            title_lower = lesson.get('title', '').lower()
            if any(keyword in title_lower for keyword in intro_keywords):
                difficulty = self.lesson_features.get(lesson_id, {}).get('difficulty', 0.5)
                candidates.append((lesson_id, 1.0 - difficulty))  # Prefer easier lessons
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        for lesson_id, score in candidates[:count]:
            lesson = self.lessons_cache.get(lesson_id)
            if lesson:
                recommendations.append({
                    'lesson_id': lesson_id,
                    'title': lesson.get('title'),
                    'subject': lesson.get('subject'),
                    'score': score,
                    'reason': "Great starting point for new learners"
                })
        
        return recommendations


if __name__ == "__main__":
    print("="*70)
    print("Wave 3 Recommendation Engine Demo")
    print("="*70)
    
    engine = RecommendationEngine()
    print(f"\nLoaded {len(engine.lessons_cache)} lessons")
    
    # Simulate some student interactions
    print("\nSimulating student interactions...")
    engine.record_interaction("STU001", "Chemistry:lesson_01_atomic_structure_and_chemical_bonding", 0.85)
    engine.record_interaction("STU001", "Chemistry:lesson_02_chemical_equations_and_stoichiometry", 0.75)
    engine.record_interaction("STU001", "Biology:lesson_01_cell_structure_and_functions", 0.90)
    
    # Get recommendations
    print("\nContent-Based Recommendations:")
    content_recs = engine.get_content_based_recommendations("STU001", 3)
    for i, rec in enumerate(content_recs, 1):
        print(f"{i}. {rec['title']}")
        print(f"   {rec['reason']}")
    
    print("\nHybrid Recommendations:")
    hybrid_recs = engine.get_hybrid_recommendations("STU001", 5)
    for i, rec in enumerate(hybrid_recs, 1):
        print(f"{i}. {rec['title']}")
        print(f"   Score: {rec['score']:.2f} - {rec['reason']}")
