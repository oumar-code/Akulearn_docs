#!/usr/bin/env python3
"""YouTube MCP client for educational video search.

Searches YouTube for educational content related to Nigerian secondary school lessons.
Falls back to stub results if MCP/API is unavailable.
"""

import os
import re
from typing import List, Dict, Optional

# Try importing real YouTube API client
YOUTUBE_API_AVAILABLE = False
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    YOUTUBE_API_AVAILABLE = True
except (ImportError, KeyboardInterrupt, Exception):
    pass


class YouTubeMCPClient:
    """YouTube search client with real API integration and stub fallback."""

    def __init__(self, api_key: Optional[str] = None, use_stub: bool = False) -> None:
        """Initialize YouTube client.
        
        Args:
            api_key: YouTube Data API v3 key (defaults to YOUTUBE_API_KEY env var)
            use_stub: Force stub mode even if API is available
        """
        self.use_stub = use_stub or not YOUTUBE_API_AVAILABLE
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        
        if not self.use_stub and self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                self.use_stub = False
                print("[YouTube MCP] Using real YouTube Data API v3")
            except Exception as e:
                print(f"[YouTube MCP] API init failed: {e}, falling back to stub")
                self.use_stub = True
        else:
            if not self.api_key:
                print("[YouTube MCP] No API key found, using stub mode")
            self.use_stub = True

    def _parse_duration(self, iso_duration: str) -> str:
        """Convert ISO 8601 duration to MM:SS format."""
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
        if not match:
            return "0:00"
        
        hours, minutes, seconds = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
        
        total_minutes = hours * 60 + minutes
        return f"{total_minutes}:{seconds:02d}"

    def _search_youtube_api(self, query: str, limit: int) -> List[Dict[str, str]]:
        """Search YouTube using real API."""
        try:
            # Enhance query for educational content
            edu_query = f"{query} educational lesson tutorial"
            
            search_response = self.youtube.search().list(
                q=edu_query,
                part='id,snippet',
                maxResults=limit,
                type='video',
                videoDuration='medium',  # 4-20 minutes
                relevanceLanguage='en',
                safeSearch='strict',
                order='relevance'
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return []
            
            # Get video details for duration
            videos_response = self.youtube.videos().list(
                part='contentDetails,snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            results = []
            for item in videos_response.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                duration_iso = item['contentDetails']['duration']
                
                results.append({
                    "video_id": video_id,
                    "title": snippet['title'][:80],
                    "channel": snippet['channelTitle'],
                    "duration": self._parse_duration(duration_iso),
                    "url": f"https://youtu.be/{video_id}",
                    "thumbnail": snippet['thumbnails']['default']['url'],
                    "reason": "Educational content match",
                    "status": "verified",
                })
            
            return results
            
        except HttpError as e:
            print(f"[YouTube MCP] API error: {e}")
            return []
        except Exception as e:
            print(f"[YouTube MCP] Search error: {e}")
            return []

    def _search_stub(self, query: str, limit: int) -> List[Dict[str, str]]:
        """Return mock search results for testing."""
        base = query[:30].replace(" ", "_").replace("|", "") or "lesson"
        results = []
        for idx in range(limit):
            video_id = f"vid_{base}_{idx+1}"
            results.append({
                "video_id": video_id,
                "title": f"Educational Video: {query[:50]} (Example {idx+1})",
                "channel": "YouTube-MCP-Stub",
                "duration": "8:45",
                "url": f"https://youtu.be/{video_id}",
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/default.jpg",
                "reason": "Curated educational content (stub)",
                "status": "suggested_stub",
            })
        return results

    def search_videos(self, query: str, limit: int = 3) -> List[Dict[str, str]]:
        """Search YouTube for educational videos.

        Args:
            query: Search string (subject/topic/title combined).
            limit: Max results (default 3).

        Returns:
            List of video metadata dicts with video_id, title, channel, duration, url, etc.
        """
        if self.use_stub:
            return self._search_stub(query, limit)
        else:
            results = self._search_youtube_api(query, limit)
            # Fallback to stub if API returns nothing
            if not results:
                print(f"[YouTube MCP] No API results for '{query[:40]}...', using stub")
                return self._search_stub(query, limit)
            return results


__all__ = ["YouTubeMCPClient"]
