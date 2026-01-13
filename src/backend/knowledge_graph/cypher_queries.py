"""
Pre-built Cypher Query Templates
=================================

Commonly used queries for Nigerian Government Knowledge Graph analysis.
"""

from typing import Dict, Any, List, Optional
from datetime import date, datetime


class CypherQueries:
    """Collection of pre-built Cypher queries for common use cases."""
    
    # ========================================================================
    # RESOURCE FLOW ANALYSIS
    # ========================================================================
    
    @staticmethod
    def budget_to_impact_flow(
        ministry_name: str,
        year: int
    ) -> tuple[str, Dict[str, Any]]:
        """
        Track budget from ministry allocation to measurable impact.
        
        Args:
            ministry_name: Name of ministry
            year: Budget year
            
        Returns:
            (query, parameters) tuple
        """
        query = """
        MATCH path = (m:Ministry {name: $ministry_name})-[:ALLOCATED]->(b:Budget {year: $year})
                     -[:FUNDS]->(p:Project)-[:ACHIEVES]->(o:Outcome)
        RETURN m, b, p, o, o.beneficiaries_count as beneficiaries,
               b.amount as budget, p.cost_actual as spent
        ORDER BY o.beneficiaries_count DESC
        """
        params = {"ministry_name": ministry_name, "year": year}
        return query, params
    
    @staticmethod
    def agency_budget_utilization(
        agency_name: str,
        start_year: int,
        end_year: int
    ) -> tuple[str, Dict[str, Any]]:
        """Get budget utilization rates for an agency over time."""
        query = """
        MATCH (a:Agency {name: $agency_name})-[:RECEIVES]->(b:Budget)
        WHERE b.year >= $start_year AND b.year <= $end_year
        RETURN b.year as year, b.amount as allocated,
               b.utilization_rate as utilization,
               CASE 
                 WHEN b.utilization_rate >= 80 THEN 'Good'
                 WHEN b.utilization_rate >= 60 THEN 'Fair'
                 ELSE 'Poor'
               END as rating
        ORDER BY b.year
        """
        params = {
            "agency_name": agency_name,
            "start_year": start_year,
            "end_year": end_year
        }
        return query, params
    
    # ========================================================================
    # PROJECT ANALYSIS
    # ========================================================================
    
    @staticmethod
    def abandoned_projects(
        state: Optional[str] = None,
        min_cost: float = 1000000
    ) -> tuple[str, Dict[str, Any]]:
        """Find abandoned projects with their allocated budgets."""
        query = """
        MATCH (p:Project {status: 'abandoned'})<-[:IMPLEMENTS]-(a:Agency)
        MATCH (p)<-[:FUNDS]-(b:Budget)
        """
        if state:
            query += "WHERE p.state = $state AND b.amount >= $min_cost\n"
        else:
            query += "WHERE b.amount >= $min_cost\n"
        
        query += """
        RETURN p.name as project, a.name as agency, b.amount as budget,
               p.location as location, p.state as state,
               p.start_date as started, p.progress_percentage as progress
        ORDER BY b.amount DESC
        """
        params = {"min_cost": min_cost}
        if state:
            params["state"] = state
        return query, params
    
    @staticmethod
    def project_success_by_state() -> tuple[str, Dict[str, Any]]:
        """Compare project success rates across states."""
        query = """
        MATCH (s:State)<-[:LOCATED_IN]-(p:Project)
        WITH s, p,
             CASE p.status
               WHEN 'completed' THEN 1
               ELSE 0
             END as is_completed,
             CASE p.status
               WHEN 'abandoned' THEN 1
               ELSE 0
             END as is_abandoned
        RETURN s.name as state, s.geopolitical_zone as zone,
               count(p) as total_projects,
               sum(is_completed) as completed,
               sum(is_abandoned) as abandoned,
               avg(p.progress_percentage) as avg_progress,
               round(100.0 * sum(is_completed) / count(p), 2) as success_rate
        ORDER BY success_rate DESC
        """
        return query, {}
    
    @staticmethod
    def stalled_projects_investigation(
        days_stalled: int = 180
    ) -> tuple[str, Dict[str, Any]]:
        """Find projects stalled for extended periods."""
        query = """
        MATCH (p:Project {status: 'stalled'})<-[:IMPLEMENTS]-(a:Agency)
        MATCH (p)<-[:FUNDS]-(b:Budget)
        WHERE duration.between(p.start_date, date()).days > $days_stalled
        RETURN p.name as project, a.name as agency,
               p.start_date as started,
               duration.between(p.start_date, date()).days as days_elapsed,
               b.amount as budget, p.cost_actual as spent,
               p.progress_percentage as progress
        ORDER BY days_elapsed DESC
        """
        return query, {"days_stalled": days_stalled}
    
    # ========================================================================
    # GOVERNMENT STRUCTURE
    # ========================================================================
    
    @staticmethod
    def agency_dependencies(
        agency_name: str,
        max_depth: int = 3
    ) -> tuple[str, Dict[str, Any]]:
        """Map dependencies for an agency."""
        query = f"""
        MATCH path = (a1:Agency {{name: $agency_name}})-[:DEPENDS_ON*1..{max_depth}]->(a2:Agency)
        RETURN path, a2.name as depends_on, length(path) as depth
        ORDER BY depth, depends_on
        """
        return query, {"agency_name": agency_name}
    
    @staticmethod
    def ministry_structure(ministry_name: str) -> tuple[str, Dict[str, Any]]:
        """Get complete structure under a ministry."""
        query = """
        MATCH (m:Ministry {name: $ministry_name})
        OPTIONAL MATCH (m)-[:OVERSEES]->(a:Agency)
        OPTIONAL MATCH (a)-[:IMPLEMENTS]->(p:Project)
        OPTIONAL MATCH (a)-[:RECEIVES]->(b:Budget)
        RETURN m, collect(DISTINCT a) as agencies,
               collect(DISTINCT p) as projects,
               sum(b.amount) as total_budget
        """
        return query, {"ministry_name": ministry_name}
    
    # ========================================================================
    # NEWS & MEDIA ANALYSIS
    # ========================================================================
    
    @staticmethod
    def news_sentiment_vs_performance(
        agency_name: str,
        start_date: date
    ) -> tuple[str, Dict[str, Any]]:
        """Compare media sentiment to actual performance."""
        query = """
        MATCH (a:Agency {name: $agency_name})<-[:MENTIONS]-(n:NewsArticle)
        MATCH (a)-[:IMPLEMENTS]->(p:Project)-[:ACHIEVES]->(o:Outcome)
        WHERE n.published_date >= datetime($start_date)
        RETURN a.name as agency,
               avg(n.sentiment) as media_sentiment,
               avg(n.bias_score) as avg_bias,
               avg(o.value) as actual_performance,
               count(DISTINCT p) as completed_projects,
               count(DISTINCT n) as articles_count
        """
        return query, {"agency_name": agency_name, "start_date": start_date.isoformat()}
    
    @staticmethod
    def bias_detection_by_source(
        entity_name: str,
        entity_type: str = "Agency"
    ) -> tuple[str, Dict[str, Any]]:
        """Analyze how different sources cover same entity."""
        query = f"""
        MATCH (ns:NewsSource)<-[:PUBLISHED_BY]-(n:NewsArticle)-[:MENTIONS]->(e:{entity_type} {{name: $entity_name}})
        RETURN ns.name as source,
               ns.political_leaning as leaning,
               ns.credibility_rating as credibility,
               avg(n.bias_score) as avg_bias,
               avg(n.sentiment) as avg_sentiment,
               count(n) as article_count
        ORDER BY avg_bias DESC
        """
        return query, {"entity_name": entity_name}
    
    @staticmethod
    def trending_topics_and_response(
        min_volume: int = 1000,
        days_back: int = 30
    ) -> tuple[str, Dict[str, Any]]:
        """Identify trending topics and related government actions."""
        query = """
        MATCH (st:SocialTrend)-[:REFERENCES]->(a:Agency)
        MATCH (a)-[:IMPLEMENTS]->(p:Project)
        WHERE st.volume >= $min_volume
          AND duration.between(st.started_date, datetime()).days <= $days_back
        RETURN st.topic as trend,
               st.platform as platform,
               st.volume as mentions,
               st.sentiment as public_sentiment,
               a.name as agency,
               collect(p.name)[0..5] as related_projects,
               p.status as project_status
        ORDER BY st.volume DESC
        """
        return query, {"min_volume": min_volume, "days_back": days_back}
    
    @staticmethod
    def news_manipulation_detection(
        topic: str,
        days_back: int = 7
    ) -> tuple[str, Dict[str, Any]]:
        """Detect conflicting narratives on same topic."""
        query = """
        MATCH (n1:NewsArticle)-[:RELATES_TO]->(:NewsArticle {title: $topic})
        WHERE duration.between(n1.published_date, datetime()).days <= $days_back
        WITH n1, n1.sentiment as sentiment
        MATCH (n2:NewsArticle)-[:RELATES_TO]->(:NewsArticle {title: $topic})
        WHERE n2.sentiment * sentiment < 0  // Opposite sentiments
          AND duration.between(n2.published_date, datetime()).days <= $days_back
        RETURN n1.source as source1, n1.sentiment as sentiment1, n1.url as url1,
               n2.source as source2, n2.sentiment as sentiment2, n2.url as url2,
               abs(n1.sentiment - n2.sentiment) as sentiment_gap
        ORDER BY sentiment_gap DESC
        """
        return query, {"topic": topic, "days_back": days_back}
    
    # ========================================================================
    # ECONOMIC IMPACT
    # ========================================================================
    
    @staticmethod
    def fuel_price_impact_on_projects(
        start_date: date
    ) -> tuple[str, Dict[str, Any]]:
        """Track fuel price impact on projects (2025 context)."""
        query = """
        MATCH (ei:EconomicIndicator {name: 'Petrol Price'})-[:IMPACTS]->(p:Project)
        WHERE ei.date >= date($start_date)
        RETURN p.name as project,
               p.status as status,
               p.cost_budgeted as original_budget,
               p.cost_actual as actual_cost,
               ei.value as petrol_price,
               ei.date as price_date,
               CASE
                 WHEN p.cost_actual > p.cost_budgeted * 1.5 THEN 'Severe Impact'
                 WHEN p.cost_actual > p.cost_budgeted * 1.2 THEN 'Moderate Impact'
                 ELSE 'Minimal Impact'
               END as impact_level
        ORDER BY ei.date DESC, p.cost_actual DESC
        """
        return query, {"start_date": start_date.isoformat()}
    
    @staticmethod
    def subsidy_removal_sentiment_analysis() -> tuple[str, Dict[str, Any]]:
        """Analyze public sentiment on subsidy removal."""
        query = """
        MATCH (n:NewsArticle)-[:MENTIONS]->(:Agency {acronym: 'NNPC'})
        WHERE n.published_date >= datetime('2024-01-01T00:00:00')
          AND (toLower(n.content) CONTAINS 'subsidy' OR toLower(n.content) CONTAINS 'petrol')
        WITH n.source as source,
             avg(n.sentiment) as avg_sentiment,
             avg(n.bias_score) as avg_bias,
             count(n) as articles
        RETURN source, avg_sentiment, avg_bias, articles
        ORDER BY articles DESC
        """
        return query, {}
    
    # ========================================================================
    # TRANSPARENCY & ACCOUNTABILITY
    # ========================================================================
    
    @staticmethod
    def budget_vs_outcome_efficiency(
        sector: str,
        year: int
    ) -> tuple[str, Dict[str, Any]]:
        """Measure cost-effectiveness of government spending."""
        query = """
        MATCH (m:Ministry {sector: $sector})-[:ALLOCATED]->(b:Budget {year: $year})
        MATCH (b)-[:FUNDS]->(p:Project)-[:ACHIEVES]->(o:Outcome)
        WHERE o.beneficiaries_count IS NOT NULL
        RETURN m.name as ministry,
               b.amount as budget,
               sum(o.beneficiaries_count) as total_beneficiaries,
               b.amount / sum(o.beneficiaries_count) as cost_per_beneficiary,
               count(DISTINCT p) as projects_count
        ORDER BY cost_per_beneficiary ASC
        """
        return query, {"sector": sector, "year": year}
    
    @staticmethod
    def unverified_outcomes(min_value: float = 100000) -> tuple[str, Dict[str, Any]]:
        """Find high-value outcomes lacking verification."""
        query = """
        MATCH (o:Outcome {verification_status: 'reported'})<-[:ACHIEVES]-(p:Project)
        MATCH (p)<-[:FUNDS]-(b:Budget)
        WHERE b.amount >= $min_value
        RETURN o.name as outcome,
               o.value as reported_value,
               o.beneficiaries_count as beneficiaries,
               p.name as project,
               b.amount as budget,
               o.measurement_date as measured
        ORDER BY b.amount DESC
        """
        return query, {"min_value": min_value}
    
    # ========================================================================
    # CURRENT ISSUES (2025 NIGERIA CONTEXT)
    # ========================================================================
    
    @staticmethod
    def taxation_regime_impact() -> tuple[str, Dict[str, Any]]:
        """Track taxation-related news and government response."""
        query = """
        MATCH (n:NewsArticle)
        WHERE (toLower(n.content) CONTAINS 'tax' OR toLower(n.title) CONTAINS 'tax')
          AND n.published_date >= datetime('2025-01-01T00:00:00')
        OPTIONAL MATCH (n)-[:MENTIONS]->(gov)
        WHERE gov:Ministry OR gov:Agency
        RETURN n.title as headline,
               n.source as source,
               n.published_date as date,
               n.sentiment as sentiment,
               collect(gov.name)[0..3] as government_entities
        ORDER BY n.published_date DESC
        LIMIT 20
        """
        return query, {}
    
    @staticmethod
    def insecurity_budget_effectiveness(
        start_year: int = 2020
    ) -> tuple[str, Dict[str, Any]]:
        """Analyze security spending vs outcomes."""
        query = """
        MATCH (a:Agency)-[:RECEIVES]->(b:Budget)
        WHERE a.type = 'security' AND b.year >= $start_year
        OPTIONAL MATCH (a)-[:IMPLEMENTS]->(p:Project)-[:ACHIEVES]->(o:Outcome)
        RETURN a.name as agency,
               sum(b.amount) as total_budget,
               count(DISTINCT p) as projects,
               avg(CASE WHEN p.status = 'completed' THEN 1.0 ELSE 0.0 END) as success_rate,
               collect(DISTINCT o.name)[0..5] as key_outcomes
        ORDER BY total_budget DESC
        """
        return query, {"start_year": start_year}
    
    # ========================================================================
    # FULL TEXT SEARCH
    # ========================================================================
    
    @staticmethod
    def search_government_entities(
        search_term: str,
        limit: int = 20
    ) -> tuple[str, Dict[str, Any]]:
        """Search across all government entities."""
        query = """
        CALL db.index.fulltext.queryNodes('government_search', $search_term)
        YIELD node, score
        RETURN node, score, labels(node) as entity_type
        ORDER BY score DESC
        LIMIT $limit
        """
        return query, {"search_term": search_term, "limit": limit}
    
    @staticmethod
    def search_news_content(
        search_term: str,
        start_date: Optional[date] = None,
        limit: int = 20
    ) -> tuple[str, Dict[str, Any]]:
        """Search news articles by content."""
        query = """
        CALL db.index.fulltext.queryNodes('news_content_search', $search_term)
        YIELD node, score
        """
        if start_date:
            query += "WHERE node.published_date >= datetime($start_date)\n"
        query += """
        RETURN node.title as title,
               node.source as source,
               node.published_date as date,
               node.url as url,
               score
        ORDER BY score DESC
        LIMIT $limit
        """
        params = {"search_term": search_term, "limit": limit}
        if start_date:
            params["start_date"] = start_date.isoformat()
        return query, params
