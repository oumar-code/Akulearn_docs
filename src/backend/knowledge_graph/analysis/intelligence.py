"""Analysis and intelligence layer for knowledge graph."""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)


class BiasDetector:
    """Detect bias in news coverage."""
    
    # Keywords indicating bias
    POLITICAL_KEYWORDS = {
        "left_leaning": [
            "socialist", "progressive", "equality", "redistribution",
            "regulation", "environmental", "worker", "union"
        ],
        "right_leaning": [
            "conservative", "free_market", "capitalism", "deregulation",
            "business", "enterprise", "efficiency", "patriotic"
        ],
        "positive": [
            "success", "achievement", "progress", "development",
            "improved", "innovation", "growth", "reform"
        ],
        "negative": [
            "failure", "crisis", "corruption", "scam", "fraud",
            "collapse", "decline", "abandoned"
        ]
    }
    
    @staticmethod
    def analyze_bias(article_content: str, source_name: str) -> Dict[str, Any]:
        """
        Analyze bias in article content.
        
        Args:
            article_content: Article text
            source_name: News source name
            
        Returns:
            Bias analysis results
        """
        content_lower = article_content.lower()
        
        # Count keywords
        left_score = sum(1 for kw in BiasDetector.POLITICAL_KEYWORDS["left_leaning"]
                        if kw in content_lower)
        right_score = sum(1 for kw in BiasDetector.POLITICAL_KEYWORDS["right_leaning"]
                         if kw in content_lower)
        positive_score = sum(1 for kw in BiasDetector.POLITICAL_KEYWORDS["positive"]
                            if kw in content_lower)
        negative_score = sum(1 for kw in BiasDetector.POLITICAL_KEYWORDS["negative"]
                            if kw in content_lower)
        
        # Calculate bias score (-1 = left, +1 = right)
        bias_score = 0.0
        if left_score + right_score > 0:
            bias_score = (right_score - left_score) / (left_score + right_score)
        
        # Calculate sentiment
        sentiment = 0.0
        if positive_score + negative_score > 0:
            sentiment = (positive_score - negative_score) / (positive_score + negative_score)
        
        return {
            "bias_score": round(bias_score, 3),
            "sentiment": round(sentiment, 3),
            "left_keywords": left_score,
            "right_keywords": right_score,
            "positive_keywords": positive_score,
            "negative_keywords": negative_score,
        }
    
    @staticmethod
    def compare_coverage(
        article_group: List[Dict[str, Any]],
        topic: str,
    ) -> Dict[str, Any]:
        """
        Compare how different sources cover the same topic.
        
        Args:
            article_group: Articles covering same topic
            topic: Topic being analyzed
            
        Returns:
            Comparative analysis
        """
        if not article_group:
            return {}
        
        bias_scores = [a.get("bias_score", 0) for a in article_group]
        sentiment_scores = [a.get("sentiment", 0) for a in article_group]
        
        return {
            "topic": topic,
            "num_articles": len(article_group),
            "bias_range": (min(bias_scores), max(bias_scores)),
            "avg_bias": round(statistics.mean(bias_scores), 3),
            "bias_stdev": round(statistics.stdev(bias_scores), 3) if len(bias_scores) > 1 else 0,
            "sentiment_range": (min(sentiment_scores), max(sentiment_scores)),
            "avg_sentiment": round(statistics.mean(sentiment_scores), 3),
            "sentiment_stdev": round(statistics.stdev(sentiment_scores), 3)
                              if len(sentiment_scores) > 1 else 0,
            "sources": [a.get("source") for a in article_group],
        }


class SentimentAnalyzer:
    """Analyze sentiment in text."""
    
    @staticmethod
    def calculate_sentiment(text: str) -> float:
        """
        Calculate sentiment score for text.
        Simple implementation using keyword matching.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score (-1 to 1)
        """
        positive_words = [
            "good", "great", "excellent", "better", "improvement",
            "success", "achievement", "progress", "growth"
        ]
        negative_words = [
            "bad", "worse", "terrible", "failure", "decline",
            "corrupt", "fraud", "crime", "crisis"
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / (positive_count + negative_count)
        return round(sentiment, 3)


class TrendAnalyzer:
    """Analyze social media trends and predict futures."""
    
    @staticmethod
    def analyze_trend(
        trend_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze trend trajectory.
        
        Args:
            trend_data: Time series trend data
            
        Returns:
            Trend analysis
        """
        if not trend_data:
            return {}
        
        volumes = [t.get("volume", 0) for t in trend_data]
        sentiments = [t.get("sentiment", 0) for t in trend_data]
        
        return {
            "current_volume": volumes[-1] if volumes else 0,
            "peak_volume": max(volumes) if volumes else 0,
            "avg_volume": round(statistics.mean(volumes), 0) if volumes else 0,
            "current_sentiment": sentiments[-1] if sentiments else 0,
            "avg_sentiment": round(statistics.mean(sentiments), 3) if sentiments else 0,
            "trend_direction": "increasing" if (
                len(volumes) > 1 and volumes[-1] > volumes[-2]
            ) else "decreasing",
        }
    
    @staticmethod
    def predict_trend_trajectory(
        recent_volumes: List[int],
        days_ahead: int = 7,
    ) -> List[int]:
        """
        Simple linear trend prediction.
        
        Args:
            recent_volumes: Recent volume data points
            days_ahead: How many days to predict
            
        Returns:
            Predicted volumes
        """
        if len(recent_volumes) < 2:
            return recent_volumes
        
        # Simple linear regression slope
        n = len(recent_volumes)
        x = list(range(n))
        y = recent_volumes
        
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        slope = sum(
            (x[i] - x_mean) * (y[i] - y_mean) for i in range(n)
        ) / sum((x[i] - x_mean) ** 2 for i in range(n))
        
        intercept = y_mean - slope * x_mean
        
        predictions = []
        for i in range(days_ahead):
            predicted = int(slope * (n + i) + intercept)
            predictions.append(max(0, predicted))  # No negative volumes
        
        return predictions


class CorruptionAnalyzer:
    """Analyze corruption data and patterns."""
    
    @staticmethod
    def calculate_corruption_burden(
        cases: List[Dict[str, Any]],
        agency_name: str,
    ) -> Dict[str, Any]:
        """
        Calculate corruption burden on an agency.
        
        Args:
            cases: Corruption cases
            agency_name: Agency to analyze
            
        Returns:
            Burden analysis
        """
        agency_cases = [c for c in cases if agency_name in c.get("agencies", [])]
        
        if not agency_cases:
            return {"agency": agency_name, "burden": 0}
        
        total_amount = sum(c.get("value_involved", 0) for c in agency_cases)
        concluded_cases = sum(1 for c in agency_cases if c.get("status") == "concluded")
        conviction_rate = (
            concluded_cases / len(agency_cases) if agency_cases else 0
        )
        
        return {
            "agency": agency_name,
            "total_cases": len(agency_cases),
            "total_amount_involved": total_amount,
            "concluded_cases": concluded_cases,
            "conviction_rate": round(conviction_rate, 3),
            "avg_case_value": round(total_amount / len(agency_cases), 0)
                             if agency_cases else 0,
        }
    
    @staticmethod
    def identify_high_risk_agencies(
        cases: List[Dict[str, Any]],
        threshold: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Identify agencies with high corruption case counts.
        
        Args:
            cases: All corruption cases
            threshold: Minimum cases to consider high-risk
            
        Returns:
            List of high-risk agencies
        """
        agency_case_count = {}
        agency_amount = {}
        
        for case in cases:
            for agency in case.get("agencies", []):
                agency_case_count[agency] = agency_case_count.get(agency, 0) + 1
                agency_amount[agency] = (
                    agency_amount.get(agency, 0) + case.get("value_involved", 0)
                )
        
        high_risk = [
            {
                "agency": agency,
                "case_count": count,
                "total_amount": agency_amount[agency]
            }
            for agency, count in agency_case_count.items()
            if count >= threshold
        ]
        
        return sorted(high_risk, key=lambda x: x["total_amount"], reverse=True)


class DebtAnalyzer:
    """Analyze debt patterns and sustainability."""
    
    @staticmethod
    def calculate_debt_burden(
        country_name: str,
        debts: List[Dict[str, Any]],
        gdp: float,
    ) -> Dict[str, Any]:
        """
        Calculate country's debt burden.
        
        Args:
            country_name: Country to analyze
            debts: List of debt records
            gdp: Country's GDP
            
        Returns:
            Debt burden metrics
        """
        country_debts = [d for d in debts if d.get("country") == country_name]
        
        total_debt = sum(d.get("amount", 0) for d in country_debts)
        active_debts = sum(1 for d in country_debts if d.get("status") == "active")
        avg_interest = (
            statistics.mean([d.get("interest_rate", 0) for d in country_debts])
            if country_debts else 0
        )
        
        return {
            "country": country_name,
            "total_debt": total_debt,
            "num_debts": len(country_debts),
            "active_debts": active_debts,
            "debt_to_gdp_ratio": round((total_debt / gdp * 100), 2) if gdp else 0,
            "avg_interest_rate": round(avg_interest, 2),
            "top_creditor": max(
                set(d.get("creditor") for d in country_debts),
                key=[d.get("creditor") for d in country_debts].count
            ) if country_debts else None,
        }
    
    @staticmethod
    def identify_debt_crisis_risk(
        countries: List[Dict[str, Any]],
        threshold_ratio: float = 60.0,
    ) -> List[Dict[str, Any]]:
        """
        Identify countries at risk of debt crisis.
        
        Debt-to-GDP ratio > 60% is generally considered high risk.
        """
        at_risk = [
            c for c in countries
            if c.get("debt_to_gdp_ratio", 0) > threshold_ratio
        ]
        return sorted(at_risk, key=lambda x: x["debt_to_gdp_ratio"], reverse=True)
