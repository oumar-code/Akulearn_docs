"""
Wave 3 Redis Cache Integration
Distributed caching for recommendations, analytics, and session storage
"""

import redis
import json
import pickle
from typing import Any, Optional, Dict, List, Callable
from datetime import timedelta
from functools import wraps
import hashlib


class RedisCache:
    """
    Redis cache manager for Wave 3 platform
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True
    ):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses
        )
        
        # Key prefixes for different data types
        self.prefixes = {
            'recommendation': 'rec:',
            'analytics': 'analytics:',
            'session': 'session:',
            'user_profile': 'user:',
            'leaderboard': 'leaderboard:',
            'quiz_cache': 'quiz:',
            'mastery': 'mastery:'
        }
    
    def _make_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with prefix"""
        return f"{prefix}{identifier}"
    
    # === Basic Operations ===
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        serialize: bool = True
    ) -> bool:
        """
        Set a value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            serialize: Whether to JSON serialize the value
        """
        try:
            if serialize:
                value = json.dumps(value)
            
            if ttl:
                return self.client.setex(key, ttl, value)
            else:
                return self.client.set(key, value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def get(
        self,
        key: str,
        deserialize: bool = True,
        default: Any = None
    ) -> Any:
        """Get a value from cache"""
        try:
            value = self.client.get(key)
            if value is None:
                return default
            
            if deserialize:
                return json.loads(value)
            return value
        except Exception as e:
            print(f"Redis get error: {e}")
            return default
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        try:
            return self.client.delete(key) > 0
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return self.client.exists(key) > 0
    
    def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for existing key"""
        return self.client.expire(key, ttl)
    
    # === Recommendation Caching ===
    
    def cache_recommendations(
        self,
        student_id: str,
        recommendations: List[Dict],
        ttl: int = 3600
    ):
        """Cache personalized recommendations"""
        key = self._make_key(self.prefixes['recommendation'], student_id)
        self.set(key, recommendations, ttl=ttl)
    
    def get_recommendations(self, student_id: str) -> Optional[List[Dict]]:
        """Get cached recommendations"""
        key = self._make_key(self.prefixes['recommendation'], student_id)
        return self.get(key, default=None)
    
    def invalidate_recommendations(self, student_id: str):
        """Invalidate cached recommendations"""
        key = self._make_key(self.prefixes['recommendation'], student_id)
        self.delete(key)
    
    # === Session Management ===
    
    def create_session(
        self,
        session_id: str,
        data: Dict,
        ttl: int = 86400
    ):
        """Create user session"""
        key = self._make_key(self.prefixes['session'], session_id)
        self.set(key, data, ttl=ttl)
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        key = self._make_key(self.prefixes['session'], session_id)
        return self.get(key, default=None)
    
    def update_session(self, session_id: str, data: Dict):
        """Update session data"""
        key = self._make_key(self.prefixes['session'], session_id)
        existing = self.get_session(session_id) or {}
        existing.update(data)
        
        # Preserve TTL
        ttl = self.client.ttl(key)
        if ttl > 0:
            self.set(key, existing, ttl=ttl)
        else:
            self.set(key, existing, ttl=86400)
    
    def delete_session(self, session_id: str):
        """Delete session"""
        key = self._make_key(self.prefixes['session'], session_id)
        self.delete(key)
    
    # === User Profile Caching ===
    
    def cache_user_profile(
        self,
        student_id: str,
        profile: Dict,
        ttl: int = 3600
    ):
        """Cache user profile data"""
        key = self._make_key(self.prefixes['user_profile'], student_id)
        self.set(key, profile, ttl=ttl)
    
    def get_user_profile(self, student_id: str) -> Optional[Dict]:
        """Get cached user profile"""
        key = self._make_key(self.prefixes['user_profile'], student_id)
        return self.get(key, default=None)
    
    # === Leaderboard Management ===
    
    def update_leaderboard(
        self,
        leaderboard_name: str,
        student_id: str,
        score: float
    ):
        """
        Update leaderboard using sorted sets
        Higher scores = better ranking
        """
        key = self._make_key(self.prefixes['leaderboard'], leaderboard_name)
        self.client.zadd(key, {student_id: score})
    
    def get_leaderboard(
        self,
        leaderboard_name: str,
        top_n: int = 10,
        reverse: bool = True
    ) -> List[Dict]:
        """
        Get top N from leaderboard
        
        Args:
            leaderboard_name: Name of leaderboard
            top_n: Number of top entries to return
            reverse: True for descending (high to low), False for ascending
        """
        key = self._make_key(self.prefixes['leaderboard'], leaderboard_name)
        
        if reverse:
            entries = self.client.zrevrange(key, 0, top_n - 1, withscores=True)
        else:
            entries = self.client.zrange(key, 0, top_n - 1, withscores=True)
        
        return [
            {'student_id': student_id, 'score': score}
            for student_id, score in entries
        ]
    
    def get_user_rank(
        self,
        leaderboard_name: str,
        student_id: str
    ) -> Optional[int]:
        """Get user's rank in leaderboard (1-indexed)"""
        key = self._make_key(self.prefixes['leaderboard'], leaderboard_name)
        rank = self.client.zrevrank(key, student_id)
        return rank + 1 if rank is not None else None
    
    def get_user_score(
        self,
        leaderboard_name: str,
        student_id: str
    ) -> Optional[float]:
        """Get user's score in leaderboard"""
        key = self._make_key(self.prefixes['leaderboard'], leaderboard_name)
        return self.client.zscore(key, student_id)
    
    # === Analytics Caching ===
    
    def increment_counter(self, counter_name: str, amount: int = 1) -> int:
        """Increment a counter"""
        key = self._make_key(self.prefixes['analytics'], counter_name)
        return self.client.incrby(key, amount)
    
    def get_counter(self, counter_name: str) -> int:
        """Get counter value"""
        key = self._make_key(self.prefixes['analytics'], counter_name)
        value = self.client.get(key)
        return int(value) if value else 0
    
    def cache_analytics(
        self,
        analytics_key: str,
        data: Dict,
        ttl: int = 3600
    ):
        """Cache analytics data"""
        key = self._make_key(self.prefixes['analytics'], analytics_key)
        self.set(key, data, ttl=ttl)
    
    def get_analytics(self, analytics_key: str) -> Optional[Dict]:
        """Get cached analytics"""
        key = self._make_key(self.prefixes['analytics'], analytics_key)
        return self.get(key, default=None)
    
    # === Mastery Data Caching ===
    
    def cache_mastery_data(
        self,
        student_id: str,
        mastery_data: Dict,
        ttl: int = 1800
    ):
        """Cache student mastery data"""
        key = self._make_key(self.prefixes['mastery'], student_id)
        self.set(key, mastery_data, ttl=ttl)
    
    def get_mastery_data(self, student_id: str) -> Optional[Dict]:
        """Get cached mastery data"""
        key = self._make_key(self.prefixes['mastery'], student_id)
        return self.get(key, default=None)
    
    # === Pub/Sub for Real-time Updates ===
    
    def publish(self, channel: str, message: Dict):
        """Publish message to channel"""
        self.client.publish(channel, json.dumps(message))
    
    def subscribe(self, *channels: str):
        """Subscribe to channels"""
        pubsub = self.client.pubsub()
        pubsub.subscribe(*channels)
        return pubsub
    
    # === Cache Patterns ===
    
    def get_or_set(
        self,
        key: str,
        fetch_func: Callable,
        ttl: int = 3600
    ) -> Any:
        """
        Get from cache or fetch and cache if not found
        
        Args:
            key: Cache key
            fetch_func: Function to call if cache miss
            ttl: Time to live for cached value
        """
        # Try cache first
        cached = self.get(key, default=None)
        if cached is not None:
            return cached
        
        # Cache miss - fetch data
        data = fetch_func()
        
        # Cache for next time
        self.set(key, data, ttl=ttl)
        
        return data
    
    def cache_aside(
        self,
        key: str,
        ttl: int = 3600
    ):
        """
        Cache-aside decorator pattern
        
        Usage:
            @cache.cache_aside(key="user:{student_id}", ttl=3600)
            def get_user_data(student_id: str):
                return fetch_from_db(student_id)
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key with function arguments
                cache_key = key.format(**kwargs)
                
                # Try cache
                cached = self.get(cache_key, default=None)
                if cached is not None:
                    return cached
                
                # Cache miss - call function
                result = func(*args, **kwargs)
                
                # Cache result
                self.set(cache_key, result, ttl=ttl)
                
                return result
            
            return wrapper
        return decorator
    
    # === Bulk Operations ===
    
    def mget(self, keys: List[str]) -> List[Any]:
        """Get multiple keys at once"""
        values = self.client.mget(keys)
        return [
            json.loads(v) if v else None
            for v in values
        ]
    
    def mset(self, mapping: Dict[str, Any]):
        """Set multiple keys at once"""
        serialized = {
            k: json.dumps(v)
            for k, v in mapping.items()
        }
        return self.client.mset(serialized)
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0
    
    # === Health Check ===
    
    def ping(self) -> bool:
        """Check if Redis is accessible"""
        try:
            return self.client.ping()
        except Exception as e:
            print(f"Redis ping failed: {e}")
            return False
    
    def get_info(self) -> Dict:
        """Get Redis server info"""
        return self.client.info()


# Global cache instance
cache = RedisCache()


# Decorator for caching function results
def cached(
    key_pattern: str,
    ttl: int = 3600,
    cache_instance: Optional[RedisCache] = None
):
    """
    Decorator to cache function results
    
    Usage:
        @cached(key_pattern="recommendations:{student_id}", ttl=3600)
        async def get_recommendations(student_id: str):
            return compute_recommendations(student_id)
    """
    if cache_instance is None:
        cache_instance = cache
    
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = key_pattern.format(**kwargs)
            
            # Try cache
            cached_result = cache_instance.get(cache_key, default=None)
            if cached_result is not None:
                return cached_result
            
            # Cache miss - call function
            result = await func(*args, **kwargs)
            
            # Cache result
            cache_instance.set(cache_key, result, ttl=ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = key_pattern.format(**kwargs)
            
            cached_result = cache_instance.get(cache_key, default=None)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache_instance.set(cache_key, result, ttl=ttl)
            
            return result
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Example usage
if __name__ == "__main__":
    # Initialize cache
    cache = RedisCache()
    
    # Test connection
    if cache.ping():
        print("✓ Connected to Redis")
    else:
        print("✗ Failed to connect to Redis")
        exit(1)
    
    # Test basic operations
    cache.set("test_key", {"message": "Hello, Redis!"}, ttl=60)
    result = cache.get("test_key")
    print(f"Basic get/set: {result}")
    
    # Test recommendations caching
    cache.cache_recommendations(
        "student_123",
        [
            {"lesson_id": "math_101", "score": 0.95},
            {"lesson_id": "physics_201", "score": 0.87}
        ],
        ttl=3600
    )
    recs = cache.get_recommendations("student_123")
    print(f"Cached recommendations: {recs}")
    
    # Test leaderboard
    cache.update_leaderboard("weekly_xp", "student_1", 1500)
    cache.update_leaderboard("weekly_xp", "student_2", 2000)
    cache.update_leaderboard("weekly_xp", "student_3", 1800)
    
    top_students = cache.get_leaderboard("weekly_xp", top_n=3)
    print(f"Top 3 students: {top_students}")
    
    rank = cache.get_user_rank("weekly_xp", "student_2")
    print(f"Student 2 rank: {rank}")
    
    # Test counter
    cache.increment_counter("lesson_views", 5)
    views = cache.get_counter("lesson_views")
    print(f"Lesson views: {views}")
    
    # Test session management
    cache.create_session(
        "session_abc123",
        {
            "user_id": "student_456",
            "login_time": "2024-01-15T10:30:00",
            "preferences": {"theme": "dark"}
        },
        ttl=86400
    )
    session = cache.get_session("session_abc123")
    print(f"Session data: {session}")
    
    print("\n✓ All tests passed!")
