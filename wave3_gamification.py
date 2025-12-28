#!/usr/bin/env python3
"""
Wave 3 Gamification System
Achievements, badges, leaderboards, streaks, and point systems
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import json


class AchievementCategory(Enum):
    """Achievement categories"""
    MASTERY = "mastery"
    STREAK = "streak"
    EXPLORATION = "exploration"
    COLLABORATION = "collaboration"
    MILESTONE = "milestone"
    SPECIAL = "special"


class BadgeLevel(Enum):
    """Badge progression levels"""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


@dataclass
class Achievement:
    """Achievement definition"""
    achievement_id: str
    title: str
    description: str
    category: AchievementCategory
    points: int
    badge_level: BadgeLevel
    criteria: Dict  # Flexible criteria for unlocking
    icon: str = "🏆"


@dataclass
class StudentAchievement:
    """Student's unlocked achievement"""
    achievement_id: str
    student_id: str
    unlocked_at: str
    progress: float = 1.0  # 0-1 for partially completed


@dataclass
class Streak:
    """Learning streak tracking"""
    student_id: str
    streak_type: str  # "daily", "weekly", "lesson_completion"
    current_streak: int
    longest_streak: int
    last_activity_date: str
    started_at: str


@dataclass
class LeaderboardEntry:
    """Leaderboard entry"""
    rank: int
    student_id: str
    student_name: str
    total_points: int
    achievements_count: int
    mastery_average: float
    badge_level: BadgeLevel


class GamificationEngine:
    """Manages all gamification features"""
    
    def __init__(self):
        self.achievements = self._define_achievements()
        self.student_achievements = defaultdict(list)  # student_id -> [StudentAchievement]
        self.student_points = defaultdict(int)  # student_id -> total_points
        self.student_streaks = {}  # student_id -> Streak
        self.daily_activities = defaultdict(list)  # student_id -> [activity_dates]
    
    def _define_achievements(self) -> Dict[str, Achievement]:
        """Define all available achievements"""
        achievements = {}
        
        # Mastery Achievements
        achievements["first_mastery"] = Achievement(
            achievement_id="first_mastery",
            title="First Steps",
            description="Achieve mastery level on your first lesson",
            category=AchievementCategory.MASTERY,
            points=50,
            badge_level=BadgeLevel.BRONZE,
            criteria={"mastered_lessons": 1},
            icon="🎯"
        )
        
        achievements["subject_master"] = Achievement(
            achievement_id="subject_master",
            title="Subject Master",
            description="Master all lessons in a subject",
            category=AchievementCategory.MASTERY,
            points=500,
            badge_level=BadgeLevel.GOLD,
            criteria={"mastered_lessons_per_subject": 5},
            icon="⭐"
        )
        
        achievements["polymath"] = Achievement(
            achievement_id="polymath",
            title="Polymath",
            description="Master lessons in 5 different subjects",
            category=AchievementCategory.MASTERY,
            points=1000,
            badge_level=BadgeLevel.PLATINUM,
            criteria={"subjects_mastered": 5},
            icon="🌟"
        )
        
        # Streak Achievements
        achievements["week_warrior"] = Achievement(
            achievement_id="week_warrior",
            title="Week Warrior",
            description="Maintain a 7-day study streak",
            category=AchievementCategory.STREAK,
            points=100,
            badge_level=BadgeLevel.BRONZE,
            criteria={"daily_streak": 7},
            icon="🔥"
        )
        
        achievements["month_master"] = Achievement(
            achievement_id="month_master",
            title="Month Master",
            description="Maintain a 30-day study streak",
            category=AchievementCategory.STREAK,
            points=300,
            badge_level=BadgeLevel.SILVER,
            criteria={"daily_streak": 30},
            icon="🔥"
        )
        
        achievements["unstoppable"] = Achievement(
            achievement_id="unstoppable",
            title="Unstoppable",
            description="Maintain a 100-day study streak",
            category=AchievementCategory.STREAK,
            points=1000,
            badge_level=BadgeLevel.DIAMOND,
            criteria={"daily_streak": 100},
            icon="💎"
        )
        
        # Exploration Achievements
        achievements["explorer"] = Achievement(
            achievement_id="explorer",
            title="Explorer",
            description="Start lessons in 3 different subjects",
            category=AchievementCategory.EXPLORATION,
            points=50,
            badge_level=BadgeLevel.BRONZE,
            criteria={"subjects_explored": 3},
            icon="🧭"
        )
        
        achievements["renaissance_learner"] = Achievement(
            achievement_id="renaissance_learner",
            title="Renaissance Learner",
            description="Complete at least one lesson in every subject",
            category=AchievementCategory.EXPLORATION,
            points=400,
            badge_level=BadgeLevel.GOLD,
            criteria={"all_subjects_touched": True},
            icon="📚"
        )
        
        # Milestone Achievements
        achievements["century_club"] = Achievement(
            achievement_id="century_club",
            title="Century Club",
            description="Complete 100 practice problems",
            category=AchievementCategory.MILESTONE,
            points=200,
            badge_level=BadgeLevel.SILVER,
            criteria={"problems_completed": 100},
            icon="💯"
        )
        
        achievements["quiz_master"] = Achievement(
            achievement_id="quiz_master",
            title="Quiz Master",
            description="Score 90% or higher on 10 quizzes",
            category=AchievementCategory.MILESTONE,
            points=300,
            badge_level=BadgeLevel.GOLD,
            criteria={"high_quiz_scores": 10},
            icon="📝"
        )
        
        achievements["night_owl"] = Achievement(
            achievement_id="night_owl",
            title="Night Owl",
            description="Complete 10 study sessions after 9 PM",
            category=AchievementCategory.SPECIAL,
            points=100,
            badge_level=BadgeLevel.BRONZE,
            criteria={"night_sessions": 10},
            icon="🦉"
        )
        
        achievements["early_bird"] = Achievement(
            achievement_id="early_bird",
            title="Early Bird",
            description="Complete 10 study sessions before 7 AM",
            category=AchievementCategory.SPECIAL,
            points=100,
            badge_level=BadgeLevel.BRONZE,
            criteria={"morning_sessions": 10},
            icon="🐦"
        )
        
        return achievements
    
    def check_and_award_achievements(self, student_id: str, student_stats: Dict) -> List[Achievement]:
        """Check if student earned new achievements"""
        newly_earned = []
        
        for achievement_id, achievement in self.achievements.items():
            # Skip if already unlocked
            if self._has_achievement(student_id, achievement_id):
                continue
            
            # Check criteria
            if self._meets_criteria(student_stats, achievement.criteria):
                self._award_achievement(student_id, achievement)
                newly_earned.append(achievement)
        
        return newly_earned
    
    def _meets_criteria(self, stats: Dict, criteria: Dict) -> bool:
        """Check if student stats meet achievement criteria"""
        for key, required_value in criteria.items():
            actual_value = stats.get(key, 0)
            
            if isinstance(required_value, bool):
                if actual_value != required_value:
                    return False
            elif isinstance(required_value, (int, float)):
                if actual_value < required_value:
                    return False
        
        return True
    
    def _has_achievement(self, student_id: str, achievement_id: str) -> bool:
        """Check if student has unlocked an achievement"""
        for ach in self.student_achievements[student_id]:
            if ach.achievement_id == achievement_id:
                return True
        return False
    
    def _award_achievement(self, student_id: str, achievement: Achievement):
        """Award achievement to student"""
        student_achievement = StudentAchievement(
            achievement_id=achievement.achievement_id,
            student_id=student_id,
            unlocked_at=datetime.now().isoformat()
        )
        self.student_achievements[student_id].append(student_achievement)
        self.student_points[student_id] += achievement.points
    
    def update_streak(self, student_id: str, activity_date: Optional[str] = None):
        """Update student's daily streak"""
        if activity_date is None:
            activity_date = datetime.now().date().isoformat()
        
        if student_id not in self.student_streaks:
            # Initialize streak
            self.student_streaks[student_id] = Streak(
                student_id=student_id,
                streak_type="daily",
                current_streak=1,
                longest_streak=1,
                last_activity_date=activity_date,
                started_at=activity_date
            )
        else:
            streak = self.student_streaks[student_id]
            last_date = datetime.fromisoformat(streak.last_activity_date).date()
            current_date = datetime.fromisoformat(activity_date).date()
            
            # Check if consecutive day
            if current_date == last_date + timedelta(days=1):
                streak.current_streak += 1
                streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            elif current_date > last_date + timedelta(days=1):
                # Streak broken
                streak.current_streak = 1
                streak.started_at = activity_date
            # Same day activities don't affect streak
            
            streak.last_activity_date = activity_date
    
    def get_student_streak(self, student_id: str) -> Optional[Streak]:
        """Get student's current streak"""
        return self.student_streaks.get(student_id)
    
    def calculate_points(self, student_id: str) -> int:
        """Calculate total points for student"""
        total = self.student_points.get(student_id, 0)
        
        # Add streak bonus
        streak = self.get_student_streak(student_id)
        if streak:
            total += streak.current_streak * 10  # 10 points per streak day
        
        return total
    
    def get_student_achievements(self, student_id: str) -> List[Dict]:
        """Get all achievements for a student"""
        result = []
        for ach in self.student_achievements[student_id]:
            achievement_def = self.achievements.get(ach.achievement_id)
            if achievement_def:
                result.append({
                    'achievement_id': ach.achievement_id,
                    'title': achievement_def.title,
                    'description': achievement_def.description,
                    'category': achievement_def.category.value,
                    'points': achievement_def.points,
                    'badge_level': achievement_def.badge_level.value,
                    'icon': achievement_def.icon,
                    'unlocked_at': ach.unlocked_at
                })
        return result
    
    def get_leaderboard(self, limit: int = 10, timeframe: str = "all_time") -> List[Dict]:
        """Get leaderboard rankings"""
        # Calculate rankings
        rankings = []
        for student_id in self.student_points.keys():
            total_points = self.calculate_points(student_id)
            achievements_count = len(self.student_achievements[student_id])
            
            # Determine badge level based on points
            badge_level = self._get_badge_level_for_points(total_points)
            
            rankings.append({
                'student_id': student_id,
                'student_name': f"Student {student_id}",  # Would come from user service
                'total_points': total_points,
                'achievements_count': achievements_count,
                'mastery_average': 0.0,  # Would come from progress tracker
                'badge_level': badge_level.value
            })
        
        # Sort by points
        rankings.sort(key=lambda x: x['total_points'], reverse=True)
        
        # Add ranks
        for i, entry in enumerate(rankings[:limit], 1):
            entry['rank'] = i
        
        return rankings[:limit]
    
    def _get_badge_level_for_points(self, points: int) -> BadgeLevel:
        """Determine badge level based on total points"""
        if points >= 5000:
            return BadgeLevel.DIAMOND
        elif points >= 2000:
            return BadgeLevel.PLATINUM
        elif points >= 1000:
            return BadgeLevel.GOLD
        elif points >= 500:
            return BadgeLevel.SILVER
        else:
            return BadgeLevel.BRONZE
    
    def get_achievement_progress(self, student_id: str, achievement_id: str, 
                                 current_stats: Dict) -> Dict:
        """Get progress towards an achievement"""
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return {}
        
        # Check if already unlocked
        if self._has_achievement(student_id, achievement_id):
            return {
                'achievement_id': achievement_id,
                'title': achievement.title,
                'completed': True,
                'progress': 1.0
            }
        
        # Calculate progress
        progress = 0.0
        progress_details = {}
        
        for key, required in achievement.criteria.items():
            current = current_stats.get(key, 0)
            if isinstance(required, (int, float)):
                criterion_progress = min(1.0, current / required)
                progress_details[key] = {
                    'current': current,
                    'required': required,
                    'progress': criterion_progress
                }
                progress += criterion_progress / len(achievement.criteria)
            elif isinstance(required, bool):
                criterion_met = current == required
                progress_details[key] = {
                    'met': criterion_met
                }
                if criterion_met:
                    progress += 1.0 / len(achievement.criteria)
        
        return {
            'achievement_id': achievement_id,
            'title': achievement.title,
            'description': achievement.description,
            'points': achievement.points,
            'completed': False,
            'progress': progress,
            'details': progress_details
        }


if __name__ == "__main__":
    print("="*70)
    print("Wave 3 Gamification System Demo")
    print("="*70)
    
    engine = GamificationEngine()
    print(f"\nTotal achievements defined: {len(engine.achievements)}")
    
    # Simulate student activity
    student_id = "STU001"
    
    # Simulate earning achievements
    print(f"\nSimulating activities for {student_id}...")
    
    # Update streak
    for i in range(8):
        date = (datetime.now() - timedelta(days=7-i)).date().isoformat()
        engine.update_streak(student_id, date)
    
    streak = engine.get_student_streak(student_id)
    print(f"Current streak: {streak.current_streak} days")
    
    # Check for achievements
    student_stats = {
        'mastered_lessons': 5,
        'subjects_explored': 4,
        'daily_streak': 7,
        'problems_completed': 120,
        'high_quiz_scores': 12
    }
    
    newly_earned = engine.check_and_award_achievements(student_id, student_stats)
    print(f"\nAchievements earned: {len(newly_earned)}")
    for ach in newly_earned:
        print(f"  {ach.icon} {ach.title} (+{ach.points} points)")
    
    # Display leaderboard
    print("\nLeaderboard:")
    leaderboard = engine.get_leaderboard(5)
    for entry in leaderboard:
        print(f"  {entry['rank']}. {entry['student_name']} - {entry['total_points']} points")
    
    # Show achievement progress
    print("\nAchievement Progress:")
    progress = engine.get_achievement_progress(student_id, "polymath", student_stats)
    if not progress.get('completed'):
        print(f"  {progress['title']}: {progress['progress']:.0%} complete")
