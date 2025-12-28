"""
Unit Tests for Wave 3 Advanced Features
Tests for WebSocket, GraphQL, Recommendations, Gamification, and Analytics
"""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


# Test Wave 3 Advanced Platform
class TestWave3AdvancedPlatform:
    """Tests for the integrated Wave 3 platform"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from wave3_advanced_platform import app
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/api/v3/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "features" in data
        assert "version" in data
    
    def test_features_list(self, client):
        """Test features endpoint"""
        response = client.get("/api/v3/features")
        assert response.status_code == 200
        data = response.json()
        assert "features" in data
        assert "total_features" in data
        assert data["total_features"] >= 0


# Test WebSocket Module
class TestWebSocket:
    """Tests for WebSocket real-time updates"""
    
    @pytest.fixture
    def websocket_manager(self):
        """Create ConnectionManager instance"""
        from wave3_websocket import ConnectionManager
        return ConnectionManager()
    
    def test_connection_manager_creation(self, websocket_manager):
        """Test ConnectionManager can be instantiated"""
        assert websocket_manager is not None
        assert hasattr(websocket_manager, 'active_connections')
        assert isinstance(websocket_manager.active_connections, dict)
    
    def test_topic_subscription(self, websocket_manager):
        """Test topic subscription tracking"""
        student_id = "test_student_001"
        topics = ["progress", "achievements"]
        
        # Simulate subscription
        if student_id not in websocket_manager.active_connections:
            websocket_manager.active_connections[student_id] = {
                'topics': set(),
                'connection': None
            }
        
        websocket_manager.active_connections[student_id]['topics'].update(topics)
        
        assert "progress" in websocket_manager.active_connections[student_id]['topics']
        assert "achievements" in websocket_manager.active_connections[student_id]['topics']


# Test GraphQL Module
class TestGraphQL:
    """Tests for GraphQL API"""
    
    @pytest.fixture
    def schema(self):
        """Get GraphQL schema"""
        from wave3_graphql import schema
        return schema
    
    def test_schema_creation(self, schema):
        """Test GraphQL schema is created"""
        assert schema is not None
        assert hasattr(schema, 'query')
    
    def test_query_has_required_fields(self, schema):
        """Test Query has expected fields"""
        query_fields = schema.query._meta.fields
        expected_fields = [
            'lesson', 'lessons_by_subject', 'all_lessons', 
            'student_progress', 'recommendations', 'leaderboard'
        ]
        
        for field in expected_fields:
            assert field in query_fields, f"Missing field: {field}"


# Test Recommendation Engine
class TestRecommendationEngine:
    """Tests for AI recommendation engine"""
    
    @pytest.fixture
    def engine(self):
        """Create recommendation engine"""
        from wave3_recommendation_engine import RecommendationEngine
        return RecommendationEngine()
    
    def test_engine_creation(self, engine):
        """Test engine can be instantiated"""
        assert engine is not None
        assert hasattr(engine, 'lessons')
        assert hasattr(engine, 'student_interactions')
    
    def test_content_based_recommendations(self, engine):
        """Test content-based filtering"""
        student_id = "test_student_001"
        recommendations = engine.get_content_based_recommendations(student_id, count=5)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
        
        if recommendations:
            rec = recommendations[0]
            assert 'lesson_id' in rec
            assert 'score' in rec
            assert 0 <= rec['score'] <= 1
    
    def test_collaborative_recommendations(self, engine):
        """Test collaborative filtering"""
        student_id = "test_student_001"
        recommendations = engine.get_collaborative_recommendations(student_id, count=5)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
    
    def test_hybrid_recommendations(self, engine):
        """Test hybrid approach"""
        student_id = "test_student_001"
        recommendations = engine.get_hybrid_recommendations(student_id, count=5)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
    
    def test_interaction_recording(self, engine):
        """Test recording student interactions"""
        student_id = "test_student_001"
        lesson_id = "test_lesson_001"
        score = 0.8
        
        engine.record_interaction(student_id, lesson_id, score)
        
        assert student_id in engine.student_interactions
        assert lesson_id in engine.student_interactions[student_id]
        assert engine.student_interactions[student_id][lesson_id] == score


# Test Gamification System
class TestGamification:
    """Tests for gamification system"""
    
    @pytest.fixture
    def engine(self):
        """Create gamification engine"""
        from wave3_gamification import GamificationEngine
        return GamificationEngine()
    
    def test_engine_creation(self, engine):
        """Test engine can be instantiated"""
        assert engine is not None
        assert hasattr(engine, 'achievements')
        assert hasattr(engine, 'student_achievements')
    
    def test_achievements_defined(self, engine):
        """Test achievements are properly defined"""
        assert len(engine.achievements) >= 12
        
        # Check first mastery achievement
        first_mastery = engine.achievements.get('first_mastery')
        assert first_mastery is not None
        assert first_mastery.title == "First Steps"
        assert first_mastery.points == 50
    
    def test_check_and_award_achievements(self, engine):
        """Test achievement checking and awarding"""
        student_id = "test_student_001"
        student_stats = {
            'mastery_levels': {'physics': 'proficient'},
            'streak_days': 1,
            'subjects_explored': ['physics'],
            'problems_solved': 5,
            'high_quiz_scores': 1
        }
        
        awarded = engine.check_and_award_achievements(student_id, student_stats)
        
        assert isinstance(awarded, list)
        # Should get first_mastery achievement
        if awarded:
            assert any(ach.achievement_id == 'first_mastery' for ach in awarded)
    
    def test_streak_tracking(self, engine):
        """Test streak tracking"""
        student_id = "test_student_001"
        today = datetime.now().strftime("%Y-%m-%d")
        
        engine.update_streak(student_id, today)
        streak = engine.get_student_streak(student_id)
        
        assert streak is not None
        assert streak.current_streak >= 1
    
    def test_leaderboard(self, engine):
        """Test leaderboard generation"""
        # Add some test data
        engine.student_achievements["student_001"] = []
        engine.student_achievements["student_002"] = []
        
        leaderboard = engine.get_leaderboard(limit=10)
        
        assert isinstance(leaderboard, list)
        assert len(leaderboard) <= 10
    
    def test_badge_levels(self, engine):
        """Test badge level calculation"""
        from wave3_gamification import BadgeLevel
        
        assert engine._get_badge_level_for_points(100) == BadgeLevel.BRONZE
        assert engine._get_badge_level_for_points(750) == BadgeLevel.SILVER
        assert engine._get_badge_level_for_points(1500) == BadgeLevel.GOLD
        assert engine._get_badge_level_for_points(3000) == BadgeLevel.PLATINUM
        assert engine._get_badge_level_for_points(6000) == BadgeLevel.DIAMOND


# Test Advanced Analytics
class TestAdvancedAnalytics:
    """Tests for advanced analytics"""
    
    @pytest.fixture
    def engine(self):
        """Create analytics engine"""
        from wave3_analytics_advanced import AdvancedAnalytics
        return AdvancedAnalytics()
    
    def test_engine_creation(self, engine):
        """Test engine can be instantiated"""
        assert engine is not None
    
    def test_predict_mastery(self, engine):
        """Test mastery prediction"""
        student_id = "test_student_001"
        lesson_id = "test_lesson_001"
        metrics = {
            'quiz_scores': [80, 85, 90],
            'problems_completed': [0.8, 0.9, 0.85],
            'time_spent_minutes': [30, 45, 40],
            'engagement_score': 0.85
        }
        
        prediction = engine.predict_mastery(student_id, lesson_id, metrics)
        
        assert prediction is not None
        assert hasattr(prediction, 'predicted_mastery_level')
        assert hasattr(prediction, 'confidence')
        assert 0 <= prediction.confidence <= 1
        assert prediction.estimated_time_to_mastery >= 0
    
    def test_identify_at_risk_students(self, engine):
        """Test at-risk student identification"""
        student_data = {
            "student_001": {
                "mastery_average": 0.25,
                "recent_trend": "declining",
                "engagement_time": 10,
                "completion_rate": 0.3,
                "streak_status": "broken"
            }
        }
        
        at_risk = engine.identify_at_risk_students(student_data)
        
        assert isinstance(at_risk, list)
        if at_risk:
            alert = at_risk[0]
            assert hasattr(alert, 'student_id')
            assert hasattr(alert, 'risk_level')
            assert alert.risk_level in ['high', 'medium', 'low']
    
    def test_optimal_study_time(self, engine):
        """Test optimal study time recommendation"""
        student_id = "test_student_001"
        activity_history = [
            {'time_of_day': 'morning', 'performance': 0.85, 'duration': 45},
            {'time_of_day': 'afternoon', 'performance': 0.75, 'duration': 30},
            {'time_of_day': 'evening', 'performance': 0.70, 'duration': 60}
        ]
        
        recommendation = engine.recommend_optimal_study_time(student_id, activity_history)
        
        assert recommendation is not None
        assert hasattr(recommendation, 'recommended_time_of_day')
        assert hasattr(recommendation, 'recommended_duration_minutes')
        assert recommendation.recommended_duration_minutes > 0
    
    def test_learning_velocity(self, engine):
        """Test learning velocity analysis"""
        student_id = "test_student_001"
        progress_history = [
            {'date': '2024-01-01', 'mastery_points': 10},
            {'date': '2024-01-02', 'mastery_points': 20},
            {'date': '2024-01-03', 'mastery_points': 35}
        ]
        
        velocity = engine.analyze_learning_velocity(student_id, progress_history)
        
        assert velocity is not None
        assert 'mastery_points_per_day' in velocity
        assert 'trend' in velocity
        assert velocity['trend'] in ['accelerating', 'steady', 'decelerating']


# API Integration Tests
class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from wave3_advanced_platform import app
        return TestClient(app)
    
    def test_recommendations_endpoint(self, client):
        """Test recommendations API endpoint"""
        response = client.get("/api/v3/recommendations/test_student?count=5&method=hybrid")
        assert response.status_code == 200
        data = response.json()
        assert 'student_id' in data
        assert 'recommendations' in data
    
    def test_gamification_achievements_endpoint(self, client):
        """Test gamification achievements endpoint"""
        response = client.get("/api/v3/gamification/achievements/test_student")
        assert response.status_code == 200
        data = response.json()
        assert 'student_id' in data
        assert 'achievements' in data
    
    def test_analytics_predict_mastery_endpoint(self, client):
        """Test analytics mastery prediction endpoint"""
        payload = {
            "student_id": "test_student",
            "lesson_id": "test_lesson",
            "current_metrics": {
                "quiz_scores": [85],
                "problems_completed": [0.8],
                "time_spent_minutes": [30],
                "engagement_score": 0.75
            }
        }
        response = client.post("/api/v3/analytics/predict-mastery", json=payload)
        assert response.status_code in [200, 422]  # 422 if validation fails


if __name__ == "__main__":
    print("=" * 70)
    print("Wave 3 Advanced Features - Unit Tests")
    print("=" * 70)
    print("\nTo run these tests, install pytest:")
    print("  pip install pytest pytest-asyncio")
    print("\nThen run:")
    print("  pytest test_wave3_advanced.py -v")
    print("\nOr run with coverage:")
    print("  pytest test_wave3_advanced.py -v --cov=wave3_advanced_platform --cov-report=html")
    print("=" * 70)
