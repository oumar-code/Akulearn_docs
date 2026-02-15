#!/usr/bin/env python3
"""Lesson Enrichment Service

Automatically enriches lessons with generated Phase 1 assets
"""

from typing import Dict, List, Any, Optional
from src.backend.asset_loader import get_global_asset_loader
import logging

logger = logging.getLogger(__name__)


class LessonEnrichmentService:
    """Service to enrich lessons with generated assets."""
    
    @staticmethod
    def enrich_lesson(lesson: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a single lesson with generated assets."""
        loader = get_global_asset_loader()
        if not loader:
            return lesson
        
        try:
            return loader.enrich_lesson(lesson)
        except Exception as e:
            logger.warning(f"Failed to enrich lesson {lesson.get('id')}: {e}")
            return lesson
    
    @staticmethod
    def enrich_lessons(lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich multiple lessons with generated assets."""
        return [LessonEnrichmentService.enrich_lesson(lesson) for lesson in lessons]
    
    @staticmethod
    def enrich_lesson_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich a lesson response object."""
        loader = get_global_asset_loader()
        if not loader:
            return response
        
        try:
            # Check if response has a lesson object
            if "lesson" in response:
                response["lesson"] = loader.enrich_lesson(response["lesson"])
            elif "data" in response and isinstance(response["data"], dict):
                if "lesson" in response["data"]:
                    response["data"]["lesson"] = loader.enrich_lesson(response["data"]["lesson"])
            
            return response
        except Exception as e:
            logger.warning(f"Failed to enrich response: {e}")
            return response


def get_enrichment_service() -> LessonEnrichmentService:
    """Get enrichment service instance."""
    return LessonEnrichmentService()
