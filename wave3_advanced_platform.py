#!/usr/bin/env python3
"""
Wave 3 Advanced Features Integration
Integrates WebSocket, GraphQL, Recommendations, Gamification, and Advanced Analytics
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import uvicorn

# Import all advanced modules
try:
    from wave3_websocket import websocket_endpoint, manager, heartbeat
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

try:
    from wave3_graphql import schema
    from starlette_graphene3 import GraphQLApp
    GRAPHQL_AVAILABLE = True
except ImportError:
    GRAPHQL_AVAILABLE = False

try:
    from wave3_recommendation_engine import RecommendationEngine
    RECOMMENDATIONS_AVAILABLE = True
except ImportError:
    RECOMMENDATIONS_AVAILABLE = False

try:
    from wave3_gamification import GamificationEngine
    GAMIFICATION_AVAILABLE = True
except ImportError:
    GAMIFICATION_AVAILABLE = False

try:
    from wave3_analytics_advanced import AdvancedAnalytics
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False

try:
    from wave3_knowledge_graph import KnowledgeGraphGenerator
    KNOWLEDGE_GRAPH_AVAILABLE = True
except ImportError:
    KNOWLEDGE_GRAPH_AVAILABLE = False


def create_advanced_app() -> FastAPI:
    """Create FastAPI app with all advanced features"""
    
    # Lifespan context manager for startup/shutdown
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        if WEBSOCKET_AVAILABLE:
            task = asyncio.create_task(heartbeat())
        yield
        # Shutdown
        if WEBSOCKET_AVAILABLE:
            task.cancel()
    
    app = FastAPI(
        title="Akulearn Wave 3 - Advanced Platform",
        description="Complete learning platform with AI recommendations, gamification, and predictive analytics",
        version="3.0.0",
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize engines
    if RECOMMENDATIONS_AVAILABLE:
        app.state.recommendation_engine = RecommendationEngine()
    
    if GAMIFICATION_AVAILABLE:
        app.state.gamification_engine = GamificationEngine()
    
    if ANALYTICS_AVAILABLE:
        app.state.analytics_engine = AdvancedAnalytics()
    
    # Health check
    @app.get("/api/v3/health")
    async def health_check():
        """Health check with feature flags"""
        return {
            "status": "healthy",
            "version": "3.0.0",
            "features": {
                "websocket": WEBSOCKET_AVAILABLE,
                "graphql": GRAPHQL_AVAILABLE,
                "recommendations": RECOMMENDATIONS_AVAILABLE,
                "gamification": GAMIFICATION_AVAILABLE,
                "analytics": ANALYTICS_AVAILABLE
            }
        }
    
    # WebSocket endpoint
    if WEBSOCKET_AVAILABLE:
        @app.websocket("/ws/{student_id}")
        async def ws_endpoint(websocket: WebSocket, student_id: str):
            """Real-time updates via WebSocket"""
            await websocket_endpoint(websocket, student_id)
    
    # GraphQL endpoint
    if GRAPHQL_AVAILABLE:
        app.mount("/graphql", GraphQLApp(schema=schema, on_get=True))
    
    # Recommendation endpoints
    if RECOMMENDATIONS_AVAILABLE:
        @app.get("/api/v3/recommendations/{student_id}")
        async def get_recommendations(student_id: str, count: int = 5, method: str = "hybrid"):
            """
            Get lesson recommendations
            Methods: content, collaborative, hybrid, prerequisite
            """
            engine = app.state.recommendation_engine
            
            if method == "content":
                recs = engine.get_content_based_recommendations(student_id, count)
            elif method == "collaborative":
                recs = engine.get_collaborative_recommendations(student_id, count)
            elif method == "prerequisite":
                recs = engine.get_prerequisite_aware_recommendations(student_id, count)
            else:  # hybrid
                recs = engine.get_hybrid_recommendations(student_id, count)
            
            return {
                "student_id": student_id,
                "method": method,
                "count": len(recs),
                "recommendations": recs
            }
        
        @app.post("/api/v3/recommendations/feedback")
        async def record_recommendation_feedback(student_id: str, lesson_id: str, 
                                                interaction_score: float):
            """Record student interaction for improving recommendations"""
            engine = app.state.recommendation_engine
            engine.record_interaction(student_id, lesson_id, interaction_score)
            return {"status": "recorded", "student_id": student_id, "lesson_id": lesson_id}
    
    # Gamification endpoints
    if GAMIFICATION_AVAILABLE:
        @app.get("/api/v3/gamification/achievements/{student_id}")
        async def get_achievements(student_id: str):
            """Get student's unlocked achievements"""
            engine = app.state.gamification_engine
            achievements = engine.get_student_achievements(student_id)
            return {
                "student_id": student_id,
                "total_achievements": len(achievements),
                "achievements": achievements
            }
        
        @app.post("/api/v3/gamification/check-achievements")
        async def check_achievements(student_id: str, student_stats: dict):
            """Check and award new achievements"""
            engine = app.state.gamification_engine
            newly_earned = engine.check_and_award_achievements(student_id, student_stats)
            return {
                "student_id": student_id,
                "newly_earned": len(newly_earned),
                "achievements": [
                    {
                        "id": ach.achievement_id,
                        "title": ach.title,
                        "points": ach.points,
                        "icon": ach.icon
                    }
                    for ach in newly_earned
                ]
            }
        
        @app.get("/api/v3/gamification/leaderboard")
        async def get_leaderboard(limit: int = 10):
            """Get leaderboard rankings"""
            engine = app.state.gamification_engine
            leaderboard = engine.get_leaderboard(limit)
            return {
                "limit": limit,
                "entries": leaderboard
            }
        
        @app.get("/api/v3/gamification/streak/{student_id}")
        async def get_streak(student_id: str):
            """Get student's current streak"""
            engine = app.state.gamification_engine
            streak = engine.get_student_streak(student_id)
            if streak:
                return {
                    "student_id": student_id,
                    "current_streak": streak.current_streak,
                    "longest_streak": streak.longest_streak,
                    "last_activity": streak.last_activity_date
                }
            return {"student_id": student_id, "streak": None}
        
        @app.post("/api/v3/gamification/streak/{student_id}")
        async def update_streak(student_id: str, activity_date: str = None):
            """Update student's activity streak"""
            engine = app.state.gamification_engine
            engine.update_streak(student_id, activity_date)
            streak = engine.get_student_streak(student_id)
            return {
                "student_id": student_id,
                "current_streak": streak.current_streak if streak else 0,
                "status": "updated"
            }
    
    # Advanced analytics endpoints
    if ANALYTICS_AVAILABLE:
        @app.post("/api/v3/analytics/predict-mastery")
        async def predict_mastery(student_id: str, lesson_id: str, current_metrics: dict):
            """Predict student's mastery level"""
            engine = app.state.analytics_engine
            prediction = engine.predict_mastery(student_id, lesson_id, current_metrics)
            return {
                "lesson_id": lesson_id,
                "student_id": student_id,
                "predicted_level": prediction.predicted_mastery_level,
                "confidence": prediction.confidence,
                "estimated_hours": prediction.estimated_time_to_mastery,
                "recommendations": prediction.recommended_actions
            }
        
        @app.post("/api/v3/analytics/at-risk")
        async def identify_at_risk(student_data: dict):
            """Identify at-risk students"""
            engine = app.state.analytics_engine
            at_risk_students = engine.identify_at_risk_students(student_data)
            return {
                "total_at_risk": len(at_risk_students),
                "high_risk": len([s for s in at_risk_students if s.risk_level == "high"]),
                "medium_risk": len([s for s in at_risk_students if s.risk_level == "medium"]),
                "students": [
                    {
                        "student_id": alert.student_id,
                        "risk_level": alert.risk_level,
                        "risk_factors": alert.risk_factors,
                        "interventions": alert.intervention_recommendations,
                        "affected_subjects": alert.affected_subjects
                    }
                    for alert in at_risk_students
                ]
            }
        
        @app.post("/api/v3/analytics/optimal-study-time")
        async def get_optimal_study_time(student_id: str, activity_history: list):
            """Get optimal study time recommendation"""
            engine = app.state.analytics_engine
            recommendation = engine.recommend_optimal_study_time(student_id, activity_history)
            return {
                "student_id": student_id,
                "recommended_time": recommendation.recommended_time_of_day,
                "duration_minutes": recommendation.recommended_duration_minutes,
                "break_pattern": recommendation.recommended_break_pattern,
                "reasoning": recommendation.reasoning
            }
        
        @app.post("/api/v3/analytics/learning-velocity")
        async def analyze_velocity(student_id: str, progress_history: list):
            """Analyze learning velocity"""
            engine = app.state.analytics_engine
            velocity_data = engine.analyze_learning_velocity(student_id, progress_history)
            return {
                "student_id": student_id,
                **velocity_data
            }
    
    # Knowledge Graph endpoints
    if KNOWLEDGE_GRAPH_AVAILABLE:
        @app.get("/api/v3/knowledge-graph")
        async def get_knowledge_graph(
            subject: str = None, 
            difficulty: str = None,
            layout: str = "force",
            include_topics: bool = True
        ):
            """
            Get knowledge graph data for visualization
            Layouts: force, hierarchical, circular
            """
            generator = KnowledgeGraphGenerator()
            
            # Build sample graph (replace with real database query)
            generator.build_sample_graph()
            
            # Apply layout
            if layout == "hierarchical":
                generator.apply_hierarchical_layout()
            elif layout == "circular":
                generator.apply_circular_layout()
            else:  # force-directed
                generator.apply_force_directed_layout()
            
            # Export with filters
            graph_data = generator.export_for_visualization(
                include_topics=include_topics,
                filter_subject=subject
            )
            
            return graph_data
        
        @app.get("/api/v3/learning-paths")
        async def get_learning_paths(subject: str = None):
            """Get available learning pathways with lesson details"""
            generator = KnowledgeGraphGenerator()
            generator.build_sample_graph()
            
            # Generate learning paths
            all_paths = []
            lesson_ids = [node.id for node in generator.nodes.values() if node.type == "lesson"]
            
            if len(lesson_ids) >= 2:
                # Generate paths between lessons
                start_lessons = [l for l in lesson_ids if "1" in l or "Basic" in generator.nodes[l].label]
                end_lessons = [l for l in lesson_ids if "5" in l or "Advanced" in generator.nodes[l].label]
                
                for start in start_lessons[:3]:  # Limit to 3 starting points
                    for end in end_lessons[:2]:  # Limit to 2 end points
                        if start != end:
                            path = generator.generate_learning_path(start, end)
                            if path:
                                all_paths.append(path)
            
            # Format for frontend
            pathways = []
            lessons_dict = {}
            
            for idx, path in enumerate(all_paths[:5]):  # Limit to 5 pathways
                start_node = generator.nodes.get(path.nodes[0])
                end_node = generator.nodes.get(path.nodes[-1])
                
                pathway = {
                    "id": f"PATH_{idx+1}",
                    "name": f"{start_node.label} → {end_node.label}",
                    "description": f"Learning path from {start_node.label} to {end_node.label}",
                    "subject": start_node.subject,
                    "difficulty": start_node.difficulty,
                    "estimated_duration_hours": len(path.nodes) * 2,  # Estimate 2 hours per lesson
                    "nodes": path.nodes
                }
                pathways.append(pathway)
                
                # Add lesson details
                for node_id in path.nodes:
                    if node_id not in lessons_dict:
                        node = generator.nodes.get(node_id)
                        if node:
                            lessons_dict[node_id] = {
                                "id": node.id,
                                "title": node.label,
                                "type": node.type,
                                "subject": node.subject,
                                "difficulty": node.difficulty,
                                "duration_minutes": 45,  # Default duration
                                "topics": node.topics
                            }
            
            return {
                "pathways": pathways,
                "lessons": lessons_dict
            }
    
    # Feature documentation
    @app.get("/api/v3/features")
    async def list_features():
        """List all available advanced features"""
        features = []
        
        if WEBSOCKET_AVAILABLE:
            features.append({
                "name": "WebSocket Real-Time Updates",
                "endpoint": "/ws/{student_id}",
                "description": "Real-time streaming of progress, achievements, and notifications"
            })
        
        if GRAPHQL_AVAILABLE:
            features.append({
                "name": "GraphQL API",
                "endpoint": "/graphql",
                "description": "Flexible querying with GraphQL for complex data requirements"
            })
        
        if RECOMMENDATIONS_AVAILABLE:
            features.append({
                "name": "AI Recommendations",
                "endpoint": "/api/v3/recommendations/{student_id}",
                "description": "Intelligent lesson recommendations using collaborative and content-based filtering"
            })
        
        if GAMIFICATION_AVAILABLE:
            features.append({
                "name": "Gamification System",
                "endpoint": "/api/v3/gamification/*",
                "description": "Achievements, badges, leaderboards, and streak tracking"
            })
        
        if ANALYTICS_AVAILABLE:
            features.append({
                "name": "Advanced Analytics",
                "endpoint": "/api/v3/analytics/*",
                "description": "Predictive mastery, at-risk identification, optimal study time"
            })
        
        if KNOWLEDGE_GRAPH_AVAILABLE:
            features.append({
                "name": "Knowledge Graph Visualization",
                "endpoint": "/api/v3/knowledge-graph",
                "description": "Interactive graph showing lessons, connections, and learning pathways"
            })
            features.append({
                "name": "Learning Pathways",
                "endpoint": "/api/v3/learning-paths",
                "description": "Curated sequential learning paths with lesson details"
            })
        
        return {
            "version": "3.0.0",
            "total_features": len(features),
            "features": features
        }
    
    return app


# Create app instance
app = create_advanced_app()


if __name__ == "__main__":
    print("="*70)
    print("Wave 3 Advanced Platform - Starting Server")
    print("="*70)
    print("\nAdvanced Features:")
    print(f"  • WebSocket: {WEBSOCKET_AVAILABLE}")
    print(f"  • GraphQL: {GRAPHQL_AVAILABLE}")
    print(f"  • Recommendations: {RECOMMENDATIONS_AVAILABLE}")
    print(f"  • Gamification: {GAMIFICATION_AVAILABLE}")
    print(f"  • Analytics: {ANALYTICS_AVAILABLE}")
    print("\nEndpoints:")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • GraphQL: http://localhost:8000/graphql")
    print("  • WebSocket: ws://localhost:8000/ws/{student_id}")
    print("\nStarting server on http://0.0.0.0:8000")
    print("="*70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
