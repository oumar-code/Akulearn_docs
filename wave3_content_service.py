#!/usr/bin/env python3
"""
Wave 3 Content Service
Provides API endpoints for educational content management
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class ContentService:
    """Service for managing educational content"""
    
    def __init__(self, database_file: str = "wave3_content_database.json"):
        self.database_file = database_file
        self.database = None
        self.content_index = {}  # For fast lookups
        self.load_database()
    
    def load_database(self) -> bool:
        """Load content database from JSON file"""
        try:
            if not os.path.exists(self.database_file):
                print(f"⚠️  Database file not found: {self.database_file}")
                self.database = {
                    "metadata": {
                        "version": "3.0.0",
                        "total_items": 0
                    },
                    "content": [],
                    "subjects": [],
                    "content_types": []
                }
                return False
            
            with open(self.database_file, 'r', encoding='utf-8') as f:
                self.database = json.load(f)
            
            # Build index for fast lookups
            self._build_index()
            
            return True
        
        except Exception as e:
            print(f"❌ Error loading database: {str(e)}")
            return False
    
    def _build_index(self):
        """Build index for fast content lookups"""
        self.content_index = {}
        
        for item in self.database.get('content', []):
            content_id = item.get('id')
            if content_id:
                self.content_index[content_id] = item
    
    def get_all_content(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get all content with pagination"""
        content = self.database.get('content', [])
        total = len(content)
        
        # Apply pagination
        start = offset
        end = min(offset + limit, total)
        paginated_content = content[start:end]
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "count": len(paginated_content),
            "content": paginated_content
        }
    
    def get_content_by_id(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Get specific content item by ID"""
        return self.content_index.get(content_id)
    
    def get_content_by_subject(self, subject: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get content filtered by subject"""
        content = self.database.get('content', [])
        filtered = [item for item in content if item.get('subject', '').lower() == subject.lower()]
        return filtered[:limit]
    
    def get_content_by_topic(self, subject: str, topic: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get content filtered by subject and topic"""
        content = self.database.get('content', [])
        filtered = [
            item for item in content 
            if item.get('subject', '').lower() == subject.lower() 
            and item.get('topic', '').lower() == topic.lower()
        ]
        return filtered[:limit]
    
    def get_content_by_difficulty(self, difficulty: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get content filtered by difficulty level"""
        content = self.database.get('content', [])
        filtered = [item for item in content if item.get('difficulty', '').lower() == difficulty.lower()]
        return filtered[:limit]
    
    def get_content_by_type(self, content_type: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get content filtered by content type"""
        content = self.database.get('content', [])
        filtered = [item for item in content if item.get('content_type', '').lower() == content_type.lower()]
        return filtered[:limit]
    
    def search_content(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search content by title, topic, or tags"""
        query_lower = query.lower()
        content = self.database.get('content', [])
        
        results = []
        for item in content:
            # Search in title, topic, subtopic, tags
            if (query_lower in item.get('title', '').lower() or
                query_lower in item.get('topic', '').lower() or
                query_lower in item.get('subtopic', '').lower() or
                any(query_lower in tag.lower() for tag in item.get('tags', []))):
                results.append(item)
        
        return results[:limit]
    
    def get_subjects(self) -> List[str]:
        """Get list of all subjects"""
        return self.database.get('subjects', [])
    
    def get_topics_by_subject(self, subject: str) -> List[str]:
        """Get list of topics for a subject"""
        content = self.database.get('content', [])
        topics = set()
        
        for item in content:
            if item.get('subject', '').lower() == subject.lower():
                topic = item.get('topic')
                if topic:
                    topics.add(topic)
        
        return sorted(list(topics))
    
    def get_content_statistics(self) -> Dict[str, Any]:
        """Get content statistics"""
        return self.database.get('metadata', {}).get('statistics', {})
    
    def update_content_views(self, content_id: str) -> bool:
        """Increment view count for content"""
        content = self.get_content_by_id(content_id)
        if content:
            content['views'] = content.get('views', 0) + 1
            self._save_database()
            return True
        return False
    
    def update_content_likes(self, content_id: str, increment: int = 1) -> bool:
        """Update like count for content"""
        content = self.get_content_by_id(content_id)
        if content:
            content['likes'] = content.get('likes', 0) + increment
            self._save_database()
            return True
        return False
    
    def update_completion_rate(self, content_id: str, completion_rate: float) -> bool:
        """Update completion rate for content"""
        content = self.get_content_by_id(content_id)
        if content:
            # Average with existing rate if present
            existing_rate = content.get('completion_rate', 0.0)
            content['completion_rate'] = (existing_rate + completion_rate) / 2
            self._save_database()
            return True
        return False
    
    def _save_database(self) -> bool:
        """Save database back to file"""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving database: {str(e)}")
            return False
    
    def get_recommended_content(self, student_level: str = "SS2", 
                                subject: str = None, 
                                limit: int = 5) -> List[Dict[str, Any]]:
        """Get recommended content based on student level and subject"""
        content = self.database.get('content', [])
        
        # Filter by subject if provided
        if subject:
            content = [item for item in content if item.get('subject', '').lower() == subject.lower()]
        
        # Sort by difficulty and views
        difficulty_order = {"basic": 1, "intermediate": 2, "advanced": 3}
        
        sorted_content = sorted(
            content,
            key=lambda x: (
                difficulty_order.get(x.get('difficulty', 'intermediate'), 2),
                -x.get('views', 0)
            )
        )
        
        return sorted_content[:limit]


# Global service instance
content_service = ContentService()


def get_content_service() -> ContentService:
    """Get global content service instance"""
    return content_service
