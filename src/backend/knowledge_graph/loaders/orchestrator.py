"""
Data Ingestion Orchestrator for Nigerian Government Knowledge Graph
====================================================================

Coordinates loading of government data, corruption cases, debt, NGOs,
conflicts, social issues, and news/media monitoring into Neo4j.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from ..neo4j_client import Neo4jClient
from .government_and_corruption import (
    GovernmentDataLoader,
    CorruptionDataLoader,
    DebtDataLoader,
    NGODataLoader,
    ConflictDataLoader,
    SocialIssueDataLoader,
)
from .news_loader import (
    NewsSourceRegistry,
    NewsArticleLoader,
    SocialMediaTrendLoader,
)
from ..validators import DataValidator
from ..analysis import BiasDetector, SentimentAnalyzer

logger = logging.getLogger(__name__)


class DataIngestionOrchestrator:
    """Orchestrate data ingestion into knowledge graph."""
    
    def __init__(self, neo4j_client: Neo4jClient):
        """
        Initialize orchestrator.
        
        Args:
            neo4j_client: Connected Neo4j client
        """
        self.client = neo4j_client
        self.validation_report = {
            "total_entities": 0,
            "valid_entities": 0,
            "invalid_entities": 0,
            "total_relationships": 0,
            "created_relationships": 0,
        }
    
    async def ingest_all_government_data(self) -> Dict[str, Any]:
        """
        Ingest all government-related data in sequence.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting government data ingestion...")
        
        results = {}
        
        try:
            # Load ministries
            logger.info("Loading federal ministries...")
            ministries = GovernmentDataLoader.get_ministries()
            results["ministries"] = await self._ingest_entities(
                ministries, "Ministry"
            )
            
            # Load agencies
            logger.info("Loading government agencies...")
            agencies = GovernmentDataLoader.get_agencies()
            results["agencies"] = await self._ingest_entities(
                agencies, "Agency"
            )
            
            # Create ministry-agency relationships
            logger.info("Creating ministry-agency relationships...")
            results["relationships"] = await self._create_ministry_agency_relationships()
            
            logger.info("Government data ingestion complete")
            return results
            
        except Exception as e:
            logger.error(f"Government data ingestion failed: {e}")
            raise
    
    async def ingest_corruption_data(self) -> Dict[str, Any]:
        """
        Ingest corruption case data.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting corruption data ingestion...")
        
        try:
            cases = CorruptionDataLoader.get_sample_cases()
            result = await self._ingest_entities(cases, "CorruptionCase")
            logger.info(f"Ingested {result['created']} corruption cases")
            return result
            
        except Exception as e:
            logger.error(f"Corruption data ingestion failed: {e}")
            raise
    
    async def ingest_debt_data(self) -> Dict[str, Any]:
        """
        Ingest African debt data.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting debt data ingestion...")
        
        try:
            debts = DebtDataLoader.get_african_debts()
            result = await self._ingest_entities(debts, "Debt")
            logger.info(f"Ingested {result['created']} debt records")
            return result
            
        except Exception as e:
            logger.error(f"Debt data ingestion failed: {e}")
            raise
    
    async def ingest_ngo_data(self) -> Dict[str, Any]:
        """
        Ingest NGO data.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting NGO data ingestion...")
        
        try:
            ngos = NGODataLoader.get_key_ngos()
            result = await self._ingest_entities(ngos, "NGO")
            logger.info(f"Ingested {result['created']} NGOs")
            return result
            
        except Exception as e:
            logger.error(f"NGO data ingestion failed: {e}")
            raise
    
    async def ingest_conflict_data(self) -> Dict[str, Any]:
        """
        Ingest global conflict data.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting conflict data ingestion...")
        
        try:
            conflicts = ConflictDataLoader.get_conflicts()
            result = await self._ingest_entities(conflicts, "Conflict")
            logger.info(f"Ingested {result['created']} conflict records")
            return result
            
        except Exception as e:
            logger.error(f"Conflict data ingestion failed: {e}")
            raise
    
    async def ingest_social_issues(self) -> Dict[str, Any]:
        """
        Ingest social issue data.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting social issue data ingestion...")
        
        try:
            issues = SocialIssueDataLoader.get_social_issues()
            result = await self._ingest_entities(issues, "SocialIssue")
            logger.info(f"Ingested {result['created']} social issues")
            return result
            
        except Exception as e:
            logger.error(f"Social issue data ingestion failed: {e}")
            raise
    
    async def ingest_news_sources(self) -> Dict[str, Any]:
        """
        Ingest news sources.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting news source ingestion...")
        
        try:
            all_sources = NewsSourceRegistry.get_all_sources()
            result = await self._ingest_entities(all_sources, "NewsSource")
            logger.info(f"Ingested {result['created']} news sources")
            return result
            
        except Exception as e:
            logger.error(f"News source ingestion failed: {e}")
            raise
    
    async def ingest_news_articles(self) -> Dict[str, Any]:
        """
        Ingest sample news articles.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting news article ingestion...")
        
        try:
            articles = NewsArticleLoader.get_sample_articles()
            
            # Enrich articles with analysis
            for article in articles:
                # Bias analysis
                bias_data = BiasDetector.analyze_bias(
                    article.get("content", ""),
                    article.get("source", "")
                )
                article["bias_score"] = bias_data["bias_score"]
                article["sentiment"] = bias_data["sentiment"]
            
            result = await self._ingest_entities(articles, "NewsArticle")
            logger.info(f"Ingested {result['created']} news articles")
            return result
            
        except Exception as e:
            logger.error(f"News article ingestion failed: {e}")
            raise
    
    async def ingest_social_trends(self) -> Dict[str, Any]:
        """
        Ingest social media trends.
        
        Returns:
            Ingestion report
        """
        logger.info("Starting social trend ingestion...")
        
        try:
            trends = SocialMediaTrendLoader.get_sample_trends()
            result = await self._ingest_entities(trends, "SocialTrend")
            logger.info(f"Ingested {result['created']} social trends")
            return result
            
        except Exception as e:
            logger.error(f"Social trend ingestion failed: {e}")
            raise
    
    async def ingest_full_knowledge_graph(self) -> Dict[str, Any]:
        """
        Ingest complete knowledge graph in sequence.
        
        Returns:
            Comprehensive ingestion report
        """
        logger.info("=" * 60)
        logger.info("STARTING FULL KNOWLEDGE GRAPH INGESTION")
        logger.info("=" * 60)
        
        all_results = {}
        start_time = datetime.now()
        
        try:
            # 1. Government Data
            all_results["government"] = await self.ingest_all_government_data()
            
            # 2. Corruption
            all_results["corruption"] = await self.ingest_corruption_data()
            
            # 3. Debt
            all_results["debt"] = await self.ingest_debt_data()
            
            # 4. NGOs
            all_results["ngos"] = await self.ingest_ngo_data()
            
            # 5. Conflicts
            all_results["conflicts"] = await self.ingest_conflict_data()
            
            # 6. Social Issues
            all_results["social_issues"] = await self.ingest_social_issues()
            
            # 7. News Infrastructure
            all_results["news_sources"] = await self.ingest_news_sources()
            all_results["news_articles"] = await self.ingest_news_articles()
            all_results["social_trends"] = await self.ingest_social_trends()
            
            # 8. Create indexes
            logger.info("Creating database indexes...")
            self.client.create_indexes()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            summary = {
                "status": "success",
                "duration_seconds": duration,
                "timestamp": end_time.isoformat(),
                "results": all_results,
            }
            
            logger.info("=" * 60)
            logger.info(f"INGESTION COMPLETE in {duration:.2f} seconds")
            logger.info("=" * 60)
            
            return summary
            
        except Exception as e:
            logger.error(f"Full ingestion failed: {e}")
            raise
    
    async def _ingest_entities(
        self,
        entities: List[Dict[str, Any]],
        entity_type: str,
    ) -> Dict[str, int]:
        """
        Ingest a batch of entities with validation.
        
        Args:
            entities: Entities to ingest
            entity_type: Type of entities
            
        Returns:
            Ingestion results
        """
        # Validate entities
        valid_entities, invalid_entities = DataValidator.validate_batch(
            entities, entity_type
        )
        
        if invalid_entities:
            logger.warning(
                f"Found {len(invalid_entities)} invalid {entity_type} entities"
            )
            for invalid in invalid_entities[:3]:  # Log first 3
                logger.warning(f"  - {invalid['entity'].get('id', 'N/A')}: "
                              f"{invalid['errors']}")
        
        # Create nodes
        created_count = self.client.batch_create_nodes(entity_type, valid_entities)
        
        # Update stats
        self.validation_report["total_entities"] += len(entities)
        self.validation_report["valid_entities"] += len(valid_entities)
        self.validation_report["invalid_entities"] += len(invalid_entities)
        
        return {
            "total": len(entities),
            "valid": len(valid_entities),
            "invalid": len(invalid_entities),
            "created": created_count,
        }
    
    async def _create_ministry_agency_relationships(self) -> int:
        """
        Create OVERSEES relationships between ministries and agencies.
        
        Returns:
            Number of relationships created
        """
        # This is a simplified example
        # In production, would match on actual ministry-agency pairs
        query = """
        MATCH (m:Ministry)
        MATCH (a:Agency)
        WHERE a.type IN ['Regulatory', 'Implementation']
        CREATE (m)-[:OVERSEES]->(a)
        RETURN count(*) as created
        """
        
        try:
            result = self.client.execute_query(query)
            created = result[0]["created"] if result else 0
            logger.info(f"Created {created} OVERSEES relationships")
            self.validation_report["created_relationships"] = created
            return created
        except Exception as e:
            logger.warning(f"Could not create relationships: {e}")
            return 0
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Get ingestion validation report."""
        return self.validation_report


async def main():
    """Example usage."""
    # Initialize Neo4j client
    client = Neo4jClient(
        uri="neo4j+s://your-instance.databases.neo4j.io",
        username="neo4j",
        password="your-password"
    )
    
    try:
        # Create orchestrator
        orchestrator = DataIngestionOrchestrator(client)
        
        # Run full ingestion
        result = await orchestrator.ingest_full_knowledge_graph()
        
        print("Ingestion Report:")
        import json
        print(json.dumps(result, indent=2, default=str))
        
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
