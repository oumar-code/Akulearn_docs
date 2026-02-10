"""News and social media data loader and aggregator."""

import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)


class NewsSourceRegistry:
    """Registry of Nigerian and African news sources."""
    
    NIGERIAN_SOURCES = [
        {
            "id": str(uuid.uuid4()),
            "name": "The Punch",
            "url": "https://punchng.com",
            "type": "newspaper",
            "political_leaning": "independent",
            "credibility_rating": 0.85,
            "bias_rating": 0.2,
            "founded": "1976-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Vanguard",
            "url": "https://vanguardngr.com",
            "type": "newspaper",
            "political_leaning": "independent",
            "credibility_rating": 0.84,
            "bias_rating": 0.15,
            "founded": "1983-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Guardian",
            "url": "https://guardian.ng",
            "type": "newspaper",
            "political_leaning": "independent",
            "credibility_rating": 0.87,
            "bias_rating": 0.1,
            "founded": "1983-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "ThisDay",
            "url": "https://thisdaylive.com",
            "type": "newspaper",
            "political_leaning": "pro-government",
            "credibility_rating": 0.75,
            "bias_rating": 0.45,
            "founded": "1995-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Daily Trust",
            "url": "https://dailytrust.com",
            "type": "newspaper",
            "political_leaning": "independent",
            "credibility_rating": 0.82,
            "bias_rating": 0.2,
            "founded": "1995-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Premium Times",
            "url": "https://premiumtimesng.com",
            "type": "online",
            "political_leaning": "investigative",
            "credibility_rating": 0.92,
            "bias_rating": 0.05,
            "founded": "2011-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Channels TV",
            "url": "https://channelstv.com",
            "type": "tv",
            "political_leaning": "independent",
            "credibility_rating": 0.83,
            "bias_rating": 0.15,
            "founded": "1994-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Arise News",
            "url": "https://arise.tv",
            "type": "tv",
            "political_leaning": "independent",
            "credibility_rating": 0.81,
            "bias_rating": 0.2,
            "founded": "2013-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "TVC News",
            "url": "https://tvcnews.tv",
            "type": "tv",
            "political_leaning": "pro-government",
            "credibility_rating": 0.73,
            "bias_rating": 0.5,
            "founded": "1993-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The Cable",
            "url": "https://thecable.ng",
            "type": "online",
            "political_leaning": "independent",
            "credibility_rating": 0.88,
            "bias_rating": 0.1,
            "founded": "2014-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Sahara Reporters",
            "url": "https://saharareporters.com",
            "type": "online",
            "political_leaning": "investigative",
            "credibility_rating": 0.79,
            "bias_rating": -0.3,  # Left-leaning
            "founded": "2006-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Peoples Gazette",
            "url": "https://peoplesgazette.com",
            "type": "online",
            "political_leaning": "investigative",
            "credibility_rating": 0.86,
            "bias_rating": 0.0,
            "founded": "2019-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "BusinessDay",
            "url": "https://businessday.ng",
            "type": "newspaper",
            "political_leaning": "business-focused",
            "credibility_rating": 0.80,
            "bias_rating": 0.25,
            "founded": "1999-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nairametrics",
            "url": "https://nairametrics.com",
            "type": "online",
            "political_leaning": "economic-focused",
            "credibility_rating": 0.82,
            "bias_rating": 0.3,
            "founded": "2012-01-01"
        },
    ]
    
    AFRICAN_SOURCES = [
        {
            "id": str(uuid.uuid4()),
            "name": "BBC Africa",
            "url": "https://www.bbc.com/africa",
            "type": "tv",
            "political_leaning": "western",
            "credibility_rating": 0.95,
            "bias_rating": 0.3,
            "founded": "1922-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Reuters",
            "url": "https://www.reuters.com",
            "type": "online",
            "political_leaning": "independent",
            "credibility_rating": 0.96,
            "bias_rating": 0.05,
            "founded": "1851-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Quartz Africa",
            "url": "https://qz.com/africa",
            "type": "online",
            "political_leaning": "western",
            "credibility_rating": 0.88,
            "bias_rating": 0.25,
            "founded": "2012-01-01"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "The East African",
            "url": "https://www.theeastafrican.co.ke",
            "type": "newspaper",
            "political_leaning": "independent",
            "credibility_rating": 0.83,
            "bias_rating": 0.15,
            "founded": "1904-01-01"
        },
    ]
    
    @staticmethod
    def get_nigerian_sources() -> List[Dict[str, Any]]:
        """Get Nigerian news sources."""
        return NewsSourceRegistry.NIGERIAN_SOURCES
    
    @staticmethod
    def get_african_sources() -> List[Dict[str, Any]]:
        """Get African news sources."""
        return NewsSourceRegistry.AFRICAN_SOURCES
    
    @staticmethod
    def get_all_sources() -> List[Dict[str, Any]]:
        """Get all sources."""
        return (
            NewsSourceRegistry.NIGERIAN_SOURCES +
            NewsSourceRegistry.AFRICAN_SOURCES
        )


class SocialMediaTrendLoader:
    """Load and track social media trends."""
    
    SAMPLE_TRENDS = [
        {
            "id": str(uuid.uuid4()),
            "topic": "Fuel Subsidy Removal",
            "platform": "twitter",
            "volume": 250000,
            "sentiment": -0.65,
            "started_date": datetime.now() - timedelta(days=30),
            "peak_date": datetime.now() - timedelta(days=10),
            "related_hashtags": ["#FuelSubsidy", "#Nigeria", "#PetrolPrice", "#Inflation"],
            "geographic_focus": ["Nigeria", "Lagos", "Abuja"]
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Naira Devaluation",
            "platform": "twitter",
            "volume": 180000,
            "sentiment": -0.72,
            "started_date": datetime.now() - timedelta(days=60),
            "peak_date": datetime.now() - timedelta(days=5),
            "related_hashtags": ["#NairaCollapse", "#ExchangeRate", "#Economy", "#CBN"],
            "geographic_focus": ["Nigeria", "Financial Centers"]
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Government Corruption",
            "platform": "twitter",
            "volume": 200000,
            "sentiment": -0.58,
            "started_date": datetime.now() - timedelta(days=90),
            "peak_date": datetime.now() - timedelta(days=15),
            "related_hashtags": ["#Corruption", "#EFCC", "#Accountability", "#Nigeria"],
            "geographic_focus": ["Nigeria"]
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Insecurity and Banditry",
            "platform": "twitter",
            "volume": 150000,
            "sentiment": -0.81,
            "started_date": datetime.now() - timedelta(days=120),
            "peak_date": datetime.now() - timedelta(days=20),
            "related_hashtags": ["#EndInsecurity", "#Kidnapping", "#Banditry", "#NorthernNigeria"],
            "geographic_focus": ["Northern Nigeria", "Kaduna", "Katsina", "Sokoto"]
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Food Prices and Hunger",
            "platform": "facebook",
            "volume": 100000,
            "sentiment": -0.74,
            "started_date": datetime.now() - timedelta(days=45),
            "peak_date": datetime.now() - timedelta(days=8),
            "related_hashtags": ["#FoodCrisis", "#FoodPrices", "#HungerStrike"],
            "geographic_focus": ["Nigeria"]
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Gender-Based Violence Awareness",
            "platform": "instagram",
            "volume": 80000,
            "sentiment": -0.55,
            "started_date": datetime.now() - timedelta(days=180),
            "peak_date": datetime.now() - timedelta(days=30),
            "related_hashtags": ["#GBV", "#FightGBV", "#WomensRights", "#EndViolence"],
            "geographic_focus": ["Nigeria", "East Africa"]
        },
        {
            "id": str(uuid.uuid4()),
            "topic": "Education Crisis",
            "platform": "twitter",
            "volume": 120000,
            "sentiment": -0.62,
            "started_date": datetime.now() - timedelta(days=75),
            "peak_date": datetime.now() - timedelta(days=25),
            "related_hashtags": ["#EducationCrisis", "#SchoolClosure", "#StudentsCall"],
            "geographic_focus": ["Nigeria"]
        },
    ]
    
    @staticmethod
    def get_sample_trends() -> List[Dict[str, Any]]:
        """Get sample social media trends."""
        return SocialMediaTrendLoader.SAMPLE_TRENDS


class NewsArticleLoader:
    """Load news articles into knowledge graph."""
    
    SAMPLE_ARTICLES = [
        {
            "id": str(uuid.uuid4()),
            "title": "EFCC recovers N15 billion in fuel subsidy fraud",
            "source": "Premium Times",
            "url": "https://example.com/article-001",
            "published_date": datetime.now() - timedelta(days=5),
            "content": "The Economic and Financial Crimes Commission has recovered additional funds in an ongoing investigation into fuel subsidy fraud...",
            "sentiment": 0.45,
            "bias_score": 0.05,
            "credibility_score": 0.92,
            "topics": ["corruption", "fuel", "EFCC"],
            "entities_mentioned": ["EFCC", "Fuel Subsidy"],
            "fact_check_status": "verified"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Naira hits all-time low amid economic crisis",
            "source": "Nairametrics",
            "url": "https://example.com/article-002",
            "published_date": datetime.now() - timedelta(days=3),
            "content": "Nigerian currency continues to depreciate as economic challenges mount...",
            "sentiment": -0.72,
            "bias_score": 0.2,
            "credibility_score": 0.82,
            "topics": ["economy", "currency", "inflation"],
            "entities_mentioned": ["CBN", "Naira"],
            "fact_check_status": "verified"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "ICPC concludes investigation into N2.8bn highway fraud",
            "source": "The Cable",
            "url": "https://example.com/article-003",
            "published_date": datetime.now() - timedelta(days=7),
            "content": "The Independent Corrupt Practices Commission has concluded its investigation into alleged fraud in a major road project...",
            "sentiment": 0.38,
            "bias_score": 0.08,
            "credibility_score": 0.88,
            "topics": ["corruption", "infrastructure", "ICPC"],
            "entities_mentioned": ["ICPC", "Highway Project"],
            "fact_check_status": "verified"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Over 30 million Nigerians at risk of hunger - UN",
            "source": "BBC Africa",
            "url": "https://example.com/article-004",
            "published_date": datetime.now() - timedelta(days=2),
            "content": "UN agencies warn that food insecurity is worsening in Nigeria due to economic hardship...",
            "sentiment": -0.68,
            "bias_score": 0.3,
            "credibility_score": 0.95,
            "topics": ["hunger", "food_security", "poverty"],
            "entities_mentioned": ["UN", "Nigeria"],
            "fact_check_status": "verified"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Report: Almajiri children face exploitation in northern states",
            "source": "Sahara Reporters",
            "url": "https://example.com/article-005",
            "published_date": datetime.now() - timedelta(days=4),
            "content": "Investigation reveals systematic exploitation of Almajiri children across multiple northern states...",
            "sentiment": -0.55,
            "bias_score": -0.2,
            "credibility_score": 0.79,
            "topics": ["almajiri", "child_welfare", "education"],
            "entities_mentioned": ["Northern States"],
            "fact_check_status": "needs_verification"
        },
    ]
    
    @staticmethod
    def get_sample_articles() -> List[Dict[str, Any]]:
        """Get sample news articles."""
        return NewsArticleLoader.SAMPLE_ARTICLES


class NewsAggregator:
    """Aggregate news from multiple sources."""
    
    @staticmethod
    async def fetch_from_news_api(
        query: str,
        sources: Optional[List[str]] = None,
        language: str = "en",
        days_back: int = 7,
    ) -> List[Dict[str, Any]]:
        """
        Fetch news from NewsAPI (requires API key).
        
        This is a stub for production implementation.
        Requires newsapi.org API key.
        """
        logger.info(f"Would fetch news for query: {query}")
        return []
    
    @staticmethod
    async def fetch_from_twitter(
        query: str,
        days_back: int = 7,
    ) -> List[Dict[str, Any]]:
        """
        Fetch tweets using Twitter API v2 (requires bearer token).
        
        This is a stub for production implementation.
        """
        logger.info(f"Would fetch tweets for query: {query}")
        return []
    
    @staticmethod
    async def web_scrape_news_source(
        source_url: str,
        max_articles: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Scrape news from website using BeautifulSoup.
        
        This is a stub for production implementation.
        """
        logger.info(f"Would scrape news from: {source_url}")
        return []
    
    @staticmethod
    async def aggregate_news(
        queries: List[str],
        days_back: int = 7,
    ) -> List[Dict[str, Any]]:
        """Aggregate news from multiple sources asynchronously."""
        results = []
        tasks = [
            NewsAggregator.fetch_from_news_api(q, days_back=days_back)
            for q in queries
        ]
        try:
            results = await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error aggregating news: {e}")
        return [item for sublist in results for item in sublist]
