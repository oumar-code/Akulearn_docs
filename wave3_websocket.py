#!/usr/bin/env python3
"""
Wave 3 WebSocket Real-Time Updates
Provides real-time streaming of progress updates, notifications, and live data
"""

from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json
import asyncio


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.student_subscriptions: Dict[str, Set[str]] = {}  # student_id -> set of subscribed topics
    
    async def connect(self, websocket: WebSocket, student_id: str):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        if student_id not in self.active_connections:
            self.active_connections[student_id] = []
            self.student_subscriptions[student_id] = set()
        self.active_connections[student_id].append(websocket)
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Connected to Akulearn Wave 3 real-time updates"
        }, student_id)
    
    def disconnect(self, websocket: WebSocket, student_id: str):
        """Remove a WebSocket connection"""
        if student_id in self.active_connections:
            self.active_connections[student_id].remove(websocket)
            if not self.active_connections[student_id]:
                del self.active_connections[student_id]
                if student_id in self.student_subscriptions:
                    del self.student_subscriptions[student_id]
    
    async def send_personal_message(self, message: dict, student_id: str):
        """Send message to a specific student's connections"""
        if student_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[student_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for conn in disconnected:
                self.disconnect(conn, student_id)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for student_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, student_id)
    
    async def broadcast_to_topic(self, message: dict, topic: str):
        """Broadcast to all students subscribed to a topic"""
        for student_id, topics in self.student_subscriptions.items():
            if topic in topics:
                await self.send_personal_message(message, student_id)
    
    def subscribe(self, student_id: str, topic: str):
        """Subscribe student to a topic"""
        if student_id not in self.student_subscriptions:
            self.student_subscriptions[student_id] = set()
        self.student_subscriptions[student_id].add(topic)
    
    def unsubscribe(self, student_id: str, topic: str):
        """Unsubscribe student from a topic"""
        if student_id in self.student_subscriptions:
            self.student_subscriptions[student_id].discard(topic)


# Global connection manager
manager = ConnectionManager()


async def handle_websocket_message(websocket: WebSocket, student_id: str, data: dict):
    """Handle incoming WebSocket messages"""
    message_type = data.get("type")
    
    if message_type == "subscribe":
        topic = data.get("topic")
        if topic:
            manager.subscribe(student_id, topic)
            await manager.send_personal_message({
                "type": "subscription_confirmed",
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }, student_id)
    
    elif message_type == "unsubscribe":
        topic = data.get("topic")
        if topic:
            manager.unsubscribe(student_id, topic)
            await manager.send_personal_message({
                "type": "unsubscription_confirmed",
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }, student_id)
    
    elif message_type == "ping":
        await manager.send_personal_message({
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        }, student_id)
    
    elif message_type == "get_status":
        await manager.send_personal_message({
            "type": "status",
            "student_id": student_id,
            "connected": True,
            "subscriptions": list(manager.student_subscriptions.get(student_id, set())),
            "timestamp": datetime.now().isoformat()
        }, student_id)


async def stream_progress_updates(student_id: str, lesson_id: str = None):
    """Stream progress updates for a student"""
    try:
        from enhanced_progress_tracker import EnhancedProgressTracker
        tracker = EnhancedProgressTracker()
        
        # Get current progress
        if lesson_id:
            metrics = tracker.calculate_mastery_metrics(student_id, lesson_id)
            await manager.send_personal_message({
                "type": "progress_update",
                "lesson_id": lesson_id,
                "mastery_level": metrics.mastery_level.value,
                "mastery_percentage": metrics.mastery_percentage,
                "quiz_score": metrics.quiz_score_percentage,
                "problems_completed": metrics.problems_completed_percentage,
                "timestamp": datetime.now().isoformat()
            }, student_id)
        else:
            overview = tracker.get_student_mastery_overview(student_id)
            await manager.send_personal_message({
                "type": "progress_overview",
                "total_lessons": overview.get("total_lessons", 0),
                "completed_lessons": overview.get("completed_lessons", 0),
                "average_mastery": overview.get("average_mastery", 0),
                "timestamp": datetime.now().isoformat()
            }, student_id)
    except Exception as e:
        await manager.send_personal_message({
            "type": "error",
            "message": f"Error streaming progress: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }, student_id)


async def send_achievement_notification(student_id: str, achievement: dict):
    """Send achievement unlock notification"""
    await manager.send_personal_message({
        "type": "achievement_unlocked",
        "achievement_id": achievement.get("id"),
        "title": achievement.get("title"),
        "description": achievement.get("description"),
        "points": achievement.get("points"),
        "timestamp": datetime.now().isoformat()
    }, student_id)


async def send_recommendation_update(student_id: str, recommendations: List[dict]):
    """Send updated lesson recommendations"""
    await manager.send_personal_message({
        "type": "recommendations_updated",
        "count": len(recommendations),
        "recommendations": recommendations[:5],  # Top 5
        "timestamp": datetime.now().isoformat()
    }, student_id)


async def send_mastery_level_up(student_id: str, lesson_id: str, old_level: str, new_level: str):
    """Notify student of mastery level increase"""
    await manager.send_personal_message({
        "type": "mastery_level_up",
        "lesson_id": lesson_id,
        "old_level": old_level,
        "new_level": new_level,
        "timestamp": datetime.now().isoformat()
    }, student_id)


async def send_streak_update(student_id: str, streak_days: int, streak_type: str):
    """Send streak milestone notification"""
    await manager.send_personal_message({
        "type": "streak_update",
        "streak_type": streak_type,
        "streak_days": streak_days,
        "timestamp": datetime.now().isoformat()
    }, student_id)


async def send_leaderboard_update(student_id: str, rank: int, total_students: int, points: int):
    """Send leaderboard position update"""
    await manager.send_personal_message({
        "type": "leaderboard_update",
        "rank": rank,
        "total_students": total_students,
        "points": points,
        "timestamp": datetime.now().isoformat()
    }, student_id)


async def send_quiz_result_notification(student_id: str, quiz_result: dict):
    """Send quiz result notification"""
    await manager.send_personal_message({
        "type": "quiz_completed",
        "quiz_id": quiz_result.get("quiz_id"),
        "score": quiz_result.get("score"),
        "max_score": quiz_result.get("max_score"),
        "percentage": (quiz_result.get("score", 0) / quiz_result.get("max_score", 1) * 100),
        "timestamp": datetime.now().isoformat()
    }, student_id)


async def broadcast_new_lesson(lesson_data: dict):
    """Broadcast new lesson availability to all students"""
    await manager.broadcast_to_topic({
        "type": "new_lesson_available",
        "lesson_id": lesson_data.get("id"),
        "subject": lesson_data.get("subject"),
        "title": lesson_data.get("title"),
        "timestamp": datetime.now().isoformat()
    }, "new_content")


# WebSocket endpoint (to be integrated into FastAPI app)
async def websocket_endpoint(websocket: WebSocket, student_id: str):
    """Main WebSocket endpoint"""
    await manager.connect(websocket, student_id)
    try:
        # Start streaming progress updates
        asyncio.create_task(stream_progress_updates(student_id))
        
        while True:
            # Receive and handle messages
            data = await websocket.receive_json()
            await handle_websocket_message(websocket, student_id, data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, student_id)
    except Exception as e:
        print(f"WebSocket error for student {student_id}: {e}")
        manager.disconnect(websocket, student_id)


# Heartbeat to keep connections alive
async def heartbeat():
    """Send periodic heartbeat to all connected clients"""
    while True:
        await asyncio.sleep(30)  # Every 30 seconds
        await manager.broadcast({
            "type": "heartbeat",
            "timestamp": datetime.now().isoformat(),
            "server_time": datetime.now().isoformat()
        })


if __name__ == "__main__":
    print("WebSocket module loaded. Integrate into FastAPI app.")
    print("\nExample integration:")
    print("""
from wave3_websocket import websocket_endpoint, manager

@app.websocket("/ws/{student_id}")
async def ws_endpoint(websocket: WebSocket, student_id: str):
    await websocket_endpoint(websocket, student_id)

# On startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(heartbeat())
    """)
