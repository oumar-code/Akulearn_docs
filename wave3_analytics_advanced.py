#!/usr/bin/env python3
"""
Wave 3 Advanced Analytics
Predictive mastery modeling, at-risk student identification, optimal study time recommendations
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass
import json


@dataclass
class PredictedMastery:
    """Predicted mastery outcome"""
    lesson_id: str
    student_id: str
    predicted_mastery_level: str
    confidence: float
    estimated_time_to_mastery: float  # hours
    recommended_actions: List[str]


@dataclass
class AtRiskAlert:
    """At-risk student alert"""
    student_id: str
    risk_level: str  # "low", "medium", "high"
    risk_factors: List[str]
    intervention_recommendations: List[str]
    affected_subjects: List[str]


@dataclass
class OptimalStudyTime:
    """Optimal study time recommendation"""
    student_id: str
    recommended_time_of_day: str
    recommended_duration_minutes: int
    recommended_break_pattern: str
    reasoning: str


class AdvancedAnalytics:
    """Advanced analytics for predictive insights"""
    
    def __init__(self):
        self.student_history = defaultdict(list)  # student_id -> [activity_records]
        self.performance_patterns = {}  # student_id -> performance_data
    
    def predict_mastery(self, student_id: str, lesson_id: str, 
                       current_metrics: Dict) -> PredictedMastery:
        """Predict student's likely mastery level for a lesson"""
        
        # Extract features
        quiz_score = current_metrics.get('quiz_score_percentage', 0)
        problems_completed = current_metrics.get('problems_completed_percentage', 0)
        time_spent = current_metrics.get('time_spent_minutes', 0)
        engagement = current_metrics.get('engagement_score', 0)
        
        # Simple prediction model (could be replaced with ML model)
        # Weighted scoring: quiz 40%, problems 30%, time 20%, engagement 10%
        predicted_score = (
            quiz_score * 0.4 +
            problems_completed * 0.3 +
            min(100, (time_spent / 60) * 100) * 0.2 +
            engagement * 0.1
        )
        
        # Map to mastery level
        if predicted_score >= 95:
            predicted_level = "Mastered"
            confidence = 0.9
        elif predicted_score >= 80:
            predicted_level = "Advanced"
            confidence = 0.85
        elif predicted_score >= 60:
            predicted_level = "Proficient"
            confidence = 0.8
        elif predicted_score >= 40:
            predicted_level = "Developing"
            confidence = 0.75
        else:
            predicted_level = "Novice"
            confidence = 0.7
        
        # Estimate time to mastery
        gap_to_mastery = max(0, 95 - predicted_score)
        estimated_hours = gap_to_mastery / 10  # Rough estimate: 10 points per hour
        
        # Generate recommendations
        recommendations = []
        if quiz_score < 70:
            recommendations.append("Focus on understanding core concepts through worked examples")
        if problems_completed < 50:
            recommendations.append("Complete more practice problems to reinforce learning")
        if time_spent < 30:
            recommendations.append("Spend more time reviewing the lesson content")
        if engagement < 50:
            recommendations.append("Try interactive activities and cross-subject connections")
        
        if not recommendations:
            recommendations.append("Keep up the excellent work! Review periodically to maintain mastery")
        
        return PredictedMastery(
            lesson_id=lesson_id,
            student_id=student_id,
            predicted_mastery_level=predicted_level,
            confidence=confidence,
            estimated_time_to_mastery=estimated_hours,
            recommended_actions=recommendations
        )
    
    def identify_at_risk_students(self, student_data: Dict[str, Dict]) -> List[AtRiskAlert]:
        """Identify students at risk of falling behind"""
        at_risk_students = []
        
        for student_id, metrics in student_data.items():
            risk_factors = []
            risk_score = 0
            affected_subjects = []
            
            # Check various risk indicators
            
            # 1. Low average mastery
            avg_mastery = metrics.get('average_mastery', 0)
            if avg_mastery < 40:
                risk_factors.append("Low average mastery across subjects")
                risk_score += 3
            elif avg_mastery < 60:
                risk_factors.append("Below-average mastery levels")
                risk_score += 2
            
            # 2. Declining performance trend
            recent_scores = metrics.get('recent_quiz_scores', [])
            if len(recent_scores) >= 3:
                if self._is_declining_trend(recent_scores):
                    risk_factors.append("Declining quiz performance over time")
                    risk_score += 3
            
            # 3. Low engagement
            engagement = metrics.get('engagement_score', 0)
            if engagement < 30:
                risk_factors.append("Very low engagement with learning materials")
                risk_score += 2
            elif engagement < 50:
                risk_factors.append("Below-average engagement")
                risk_score += 1
            
            # 4. Incomplete lessons
            completion_rate = metrics.get('completion_rate', 0)
            if completion_rate < 30:
                risk_factors.append("Low lesson completion rate")
                risk_score += 2
            
            # 5. Time management issues
            time_per_lesson = metrics.get('avg_time_per_lesson', 60)
            if time_per_lesson < 15:
                risk_factors.append("Spending too little time on lessons")
                risk_score += 2
            
            # 6. Broken study streak
            days_since_activity = metrics.get('days_since_last_activity', 0)
            if days_since_activity > 7:
                risk_factors.append(f"No activity for {days_since_activity} days")
                risk_score += 3
            elif days_since_activity > 3:
                risk_factors.append("Irregular study pattern")
                risk_score += 1
            
            # 7. Subject-specific struggles
            subject_performance = metrics.get('subject_performance', {})
            for subject, score in subject_performance.items():
                if score < 40:
                    affected_subjects.append(subject)
            
            if affected_subjects:
                risk_factors.append(f"Struggling in: {', '.join(affected_subjects)}")
                risk_score += len(affected_subjects)
            
            # Determine risk level
            if risk_score >= 8:
                risk_level = "high"
            elif risk_score >= 4:
                risk_level = "medium"
            elif risk_score >= 2:
                risk_level = "low"
            else:
                continue  # Not at risk
            
            # Generate intervention recommendations
            interventions = self._generate_interventions(risk_factors, affected_subjects)
            
            at_risk_students.append(AtRiskAlert(
                student_id=student_id,
                risk_level=risk_level,
                risk_factors=risk_factors,
                intervention_recommendations=interventions,
                affected_subjects=affected_subjects
            ))
        
        # Sort by risk level
        risk_order = {"high": 0, "medium": 1, "low": 2}
        at_risk_students.sort(key=lambda x: risk_order[x.risk_level])
        
        return at_risk_students
    
    def recommend_optimal_study_time(self, student_id: str, 
                                     activity_history: List[Dict]) -> OptimalStudyTime:
        """Recommend optimal study time based on personal patterns"""
        
        if not activity_history:
            # Default recommendations for new students
            return OptimalStudyTime(
                student_id=student_id,
                recommended_time_of_day="Evening (6-8 PM)",
                recommended_duration_minutes=45,
                recommended_break_pattern="Pomodoro (25 min study, 5 min break)",
                reasoning="Based on typical student performance patterns"
            )
        
        # Analyze performance by time of day
        time_performance = defaultdict(list)
        for activity in activity_history:
            timestamp = activity.get('timestamp')
            score = activity.get('score', 0)
            if timestamp and score:
                hour = datetime.fromisoformat(timestamp).hour
                time_of_day = self._categorize_time_of_day(hour)
                time_performance[time_of_day].append(score)
        
        # Find best performing time
        best_time = "Evening (6-8 PM)"
        best_avg = 0
        for time_cat, scores in time_performance.items():
            avg = np.mean(scores)
            if avg > best_avg:
                best_avg = avg
                best_time = time_cat
        
        # Analyze optimal session duration
        duration_performance = []
        for activity in activity_history:
            duration = activity.get('duration_minutes', 0)
            score = activity.get('score', 0)
            if duration and score:
                duration_performance.append((duration, score))
        
        # Find sweet spot (diminishing returns after certain duration)
        optimal_duration = 45  # default
        if duration_performance:
            # Group by duration ranges
            short = [s for d, s in duration_performance if d < 30]
            medium = [s for d, s in duration_performance if 30 <= d < 60]
            long = [s for d, s in duration_performance if 60 <= d < 90]
            very_long = [s for d, s in duration_performance if d >= 90]
            
            avgs = {}
            if short:
                avgs[20] = np.mean(short)
            if medium:
                avgs[45] = np.mean(medium)
            if long:
                avgs[75] = np.mean(long)
            if very_long:
                avgs[90] = np.mean(very_long)
            
            if avgs:
                optimal_duration = max(avgs, key=avgs.get)
        
        # Determine break pattern
        if optimal_duration <= 30:
            break_pattern = "Short sessions (25 min study, 5 min break)"
        elif optimal_duration <= 60:
            break_pattern = "Pomodoro (25 min study, 5 min break, 4 cycles)"
        else:
            break_pattern = "Extended (50 min study, 10 min break)"
        
        # Generate reasoning
        reasoning = f"Your performance is {best_avg:.0f}% higher during {best_time}. "
        reasoning += f"Optimal session length: {optimal_duration} minutes for maximum retention."
        
        return OptimalStudyTime(
            student_id=student_id,
            recommended_time_of_day=best_time,
            recommended_duration_minutes=optimal_duration,
            recommended_break_pattern=break_pattern,
            reasoning=reasoning
        )
    
    def analyze_learning_velocity(self, student_id: str, 
                                  progress_history: List[Dict]) -> Dict:
        """Analyze how fast student is progressing"""
        if not progress_history:
            return {"velocity": 0, "trend": "insufficient_data"}
        
        # Calculate mastery gained over time
        sorted_history = sorted(progress_history, key=lambda x: x.get('timestamp', ''))
        
        if len(sorted_history) < 2:
            return {"velocity": 0, "trend": "insufficient_data"}
        
        first = sorted_history[0]
        last = sorted_history[-1]
        
        first_date = datetime.fromisoformat(first['timestamp'])
        last_date = datetime.fromisoformat(last['timestamp'])
        days_elapsed = (last_date - first_date).days
        
        if days_elapsed == 0:
            return {"velocity": 0, "trend": "insufficient_time"}
        
        # Calculate velocity (mastery points per day)
        mastery_gained = last.get('total_mastery', 0) - first.get('total_mastery', 0)
        velocity = mastery_gained / days_elapsed
        
        # Determine trend
        if len(sorted_history) >= 4:
            recent_velocity = self._calculate_recent_velocity(sorted_history[-4:])
            older_velocity = self._calculate_recent_velocity(sorted_history[:4])
            
            if recent_velocity > older_velocity * 1.2:
                trend = "accelerating"
            elif recent_velocity < older_velocity * 0.8:
                trend = "decelerating"
            else:
                trend = "steady"
        else:
            trend = "steady"
        
        return {
            "velocity": velocity,
            "trend": trend,
            "days_tracked": days_elapsed,
            "mastery_gained": mastery_gained,
            "projected_completion_days": self._project_completion(velocity, last.get('total_mastery', 0))
        }
    
    def _is_declining_trend(self, scores: List[float]) -> bool:
        """Check if scores show declining trend"""
        if len(scores) < 3:
            return False
        
        # Simple linear regression slope
        n = len(scores)
        x = list(range(n))
        y = scores
        
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        slope = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n)) / sum((x[i] - x_mean)**2 for i in range(n))
        
        return slope < -2  # Declining if slope is significantly negative
    
    def _categorize_time_of_day(self, hour: int) -> str:
        """Categorize hour into time of day"""
        if 5 <= hour < 9:
            return "Early Morning (5-9 AM)"
        elif 9 <= hour < 12:
            return "Late Morning (9-12 PM)"
        elif 12 <= hour < 15:
            return "Afternoon (12-3 PM)"
        elif 15 <= hour < 18:
            return "Late Afternoon (3-6 PM)"
        elif 18 <= hour < 21:
            return "Evening (6-9 PM)"
        else:
            return "Night (9 PM-5 AM)"
    
    def _generate_interventions(self, risk_factors: List[str], 
                               affected_subjects: List[str]) -> List[str]:
        """Generate intervention recommendations based on risk factors"""
        interventions = []
        
        if any("mastery" in factor.lower() for factor in risk_factors):
            interventions.append("Schedule one-on-one tutoring sessions")
            interventions.append("Review foundational concepts with worked examples")
        
        if any("engagement" in factor.lower() for factor in risk_factors):
            interventions.append("Introduce gamification elements to increase motivation")
            interventions.append("Connect learning to real-world applications")
        
        if any("completion" in factor.lower() for factor in risk_factors):
            interventions.append("Set smaller, achievable goals")
            interventions.append("Implement progress tracking dashboard")
        
        if any("time" in factor.lower() or "activity" in factor.lower() for factor in risk_factors):
            interventions.append("Establish consistent study schedule")
            interventions.append("Send reminder notifications")
        
        if any("declining" in factor.lower() for factor in risk_factors):
            interventions.append("Investigate external factors affecting performance")
            interventions.append("Consider adjusting difficulty level")
        
        if affected_subjects:
            interventions.append(f"Focus support on struggling subjects: {', '.join(affected_subjects)}")
            interventions.append("Pair with peer mentor in weak subjects")
        
        if not interventions:
            interventions.append("Monitor progress closely")
        
        return interventions
    
    def _calculate_recent_velocity(self, records: List[Dict]) -> float:
        """Calculate velocity from recent records"""
        if len(records) < 2:
            return 0
        
        first = records[0]
        last = records[-1]
        
        first_date = datetime.fromisoformat(first['timestamp'])
        last_date = datetime.fromisoformat(last['timestamp'])
        days = (last_date - first_date).days
        
        if days == 0:
            return 0
        
        mastery_change = last.get('total_mastery', 0) - first.get('total_mastery', 0)
        return mastery_change / days
    
    def _project_completion(self, velocity: float, current_mastery: float) -> int:
        """Project days to complete all lessons"""
        if velocity <= 0:
            return 999  # Won't complete at current rate
        
        remaining_mastery = 2100 - current_mastery  # Assuming 21 lessons * 100 mastery each
        days_to_complete = remaining_mastery / velocity
        
        return int(days_to_complete)


if __name__ == "__main__":
    print("="*70)
    print("Wave 3 Advanced Analytics Demo")
    print("="*70)
    
    analytics = AdvancedAnalytics()
    
    # Predict mastery
    print("\n1. Predictive Mastery Modeling")
    print("-" * 70)
    current_metrics = {
        'quiz_score_percentage': 75,
        'problems_completed_percentage': 60,
        'time_spent_minutes': 45,
        'engagement_score': 70
    }
    prediction = analytics.predict_mastery("STU001", "lesson_01", current_metrics)
    print(f"Predicted Level: {prediction.predicted_mastery_level}")
    print(f"Confidence: {prediction.confidence:.0%}")
    print(f"Time to Mastery: {prediction.estimated_time_to_mastery:.1f} hours")
    print("Recommendations:")
    for rec in prediction.recommended_actions:
        print(f"  - {rec}")
    
    # At-risk identification
    print("\n2. At-Risk Student Identification")
    print("-" * 70)
    student_data = {
        "STU002": {
            "average_mastery": 35,
            "recent_quiz_scores": [60, 55, 45, 40],
            "engagement_score": 25,
            "completion_rate": 20,
            "days_since_last_activity": 10,
            "subject_performance": {"Chemistry": 30, "Biology": 35}
        }
    }
    at_risk = analytics.identify_at_risk_students(student_data)
    for alert in at_risk:
        print(f"\nStudent: {alert.student_id} - Risk Level: {alert.risk_level.upper()}")
        print("Risk Factors:")
        for factor in alert.risk_factors:
            print(f"  - {factor}")
        print("Interventions:")
        for intervention in alert.intervention_recommendations[:3]:
            print(f"  - {intervention}")
    
    # Optimal study time
    print("\n3. Optimal Study Time Recommendation")
    print("-" * 70)
    activity_history = [
        {"timestamp": "2025-01-01T18:00:00", "score": 85, "duration_minutes": 45},
        {"timestamp": "2025-01-02T19:00:00", "score": 90, "duration_minutes": 50},
        {"timestamp": "2025-01-03T10:00:00", "score": 70, "duration_minutes": 30},
    ]
    optimal_time = analytics.recommend_optimal_study_time("STU001", activity_history)
    print(f"Best Time: {optimal_time.recommended_time_of_day}")
    print(f"Duration: {optimal_time.recommended_duration_minutes} minutes")
    print(f"Break Pattern: {optimal_time.recommended_break_pattern}")
    print(f"Reasoning: {optimal_time.reasoning}")
