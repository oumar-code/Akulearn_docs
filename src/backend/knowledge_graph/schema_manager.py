"""
Schema Manager for Nigerian Government Knowledge Graph
======================================================

Manages Neo4j database schema including constraints, indexes, and
initial setup.
"""

import logging
from typing import List, Dict, Any

from .neo4j_client import Neo4jClient

logger = logging.getLogger(__name__)


class SchemaManager:
    """
    Manages Neo4j database schema for the government knowledge graph.
    
    Handles:
    - Creating constraints and indexes
    - Setting up fulltext search
    - Schema validation
    - Schema migration
    """
    
    def __init__(self, client: Neo4jClient):
        """
        Initialize schema manager.
        
        Args:
            client: Neo4j client instance
        """
        self.client = client
    
    def initialize_schema(self, drop_existing: bool = False) -> Dict[str, Any]:
        """
        Initialize complete database schema.
        
        Args:
            drop_existing: If True, drop existing schema first
            
        Returns:
            Dictionary with initialization results
        """
        logger.info("Initializing Neo4j schema...")
        
        results = {
            "constraints_created": 0,
            "indexes_created": 0,
            "fulltext_indexes_created": 0,
            "errors": []
        }
        
        if drop_existing:
            logger.warning("Dropping existing schema...")
            self._drop_all_constraints()
            self._drop_all_indexes()
        
        # Create constraints
        try:
            results["constraints_created"] = self._create_constraints()
        except Exception as e:
            logger.error(f"Error creating constraints: {e}")
            results["errors"].append(f"Constraints: {str(e)}")
        
        # Create indexes
        try:
            results["indexes_created"] = self._create_indexes()
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
            results["errors"].append(f"Indexes: {str(e)}")
        
        # Create fulltext search indexes
        try:
            results["fulltext_indexes_created"] = self._create_fulltext_indexes()
        except Exception as e:
            logger.error(f"Error creating fulltext indexes: {e}")
            results["errors"].append(f"Fulltext: {str(e)}")
        
        logger.info(f"Schema initialization complete: {results}")
        return results
    
    def _create_constraints(self) -> int:
        """Create uniqueness and existence constraints."""
        constraints = [
            # Government Structure
            "CREATE CONSTRAINT ministry_name_unique IF NOT EXISTS "
            "FOR (m:Ministry) REQUIRE m.name IS UNIQUE",
            
            "CREATE CONSTRAINT agency_name_unique IF NOT EXISTS "
            "FOR (a:Agency) REQUIRE a.name IS UNIQUE",
            
            "CREATE CONSTRAINT state_name_unique IF NOT EXISTS "
            "FOR (s:State) REQUIRE s.name IS UNIQUE",
            
            # Financial
            "CREATE CONSTRAINT budget_id IF NOT EXISTS "
            "FOR (b:Budget) REQUIRE (b.year, b.category) IS UNIQUE",
            
            # Projects
            "CREATE CONSTRAINT project_name IF NOT EXISTS "
            "FOR (p:Project) REQUIRE p.name IS NOT NULL",
            
            # News & Media
            "CREATE CONSTRAINT news_url_unique IF NOT EXISTS "
            "FOR (n:NewsArticle) REQUIRE n.url IS UNIQUE",
            
            "CREATE CONSTRAINT news_source_unique IF NOT EXISTS "
            "FOR (ns:NewsSource) REQUIRE ns.name IS UNIQUE",
            
            # Economic Indicators
            "CREATE CONSTRAINT economic_indicator IF NOT EXISTS "
            "FOR (ei:EconomicIndicator) REQUIRE (ei.name, ei.date) IS UNIQUE",
        ]
        
        count = 0
        for constraint in constraints:
            try:
                self.client.execute_write(constraint)
                count += 1
                logger.debug(f"Created constraint: {constraint[:50]}...")
            except Exception as e:
                logger.warning(f"Constraint may already exist: {e}")
        
        return count
    
    def _create_indexes(self) -> int:
        """Create property indexes for query performance."""
        indexes = [
            # Date indexes for time-series queries
            "CREATE INDEX budget_year IF NOT EXISTS FOR (b:Budget) ON (b.year)",
            "CREATE INDEX project_status IF NOT EXISTS FOR (p:Project) ON (p.status)",
            "CREATE INDEX project_state IF NOT EXISTS FOR (p:Project) ON (p.state)",
            "CREATE INDEX news_published_date IF NOT EXISTS FOR (n:NewsArticle) ON (n.published_date)",
            "CREATE INDEX news_source IF NOT EXISTS FOR (n:NewsArticle) ON (n.source)",
            "CREATE INDEX social_platform IF NOT EXISTS FOR (st:SocialTrend) ON (st.platform)",
            "CREATE INDEX social_started_date IF NOT EXISTS FOR (st:SocialTrend) ON (st.started_date)",
            "CREATE INDEX economic_date IF NOT EXISTS FOR (ei:EconomicIndicator) ON (ei.date)",
            "CREATE INDEX economic_category IF NOT EXISTS FOR (ei:EconomicIndicator) ON (ei.category)",
            
            # Government structure
            "CREATE INDEX ministry_sector IF NOT EXISTS FOR (m:Ministry) ON (m.sector)",
            "CREATE INDEX ministry_level IF NOT EXISTS FOR (m:Ministry) ON (m.level)",
            "CREATE INDEX agency_level IF NOT EXISTS FOR (a:Agency) ON (a.level)",
            "CREATE INDEX agency_type IF NOT EXISTS FOR (a:Agency) ON (a.type)",
            "CREATE INDEX agency_acronym IF NOT EXISTS FOR (a:Agency) ON (a.acronym)",
            
            # Geographic
            "CREATE INDEX state_zone IF NOT EXISTS FOR (s:State) ON (s.geopolitical_zone)",
            
            # Performance indexes
            "CREATE INDEX outcome_date IF NOT EXISTS FOR (o:Outcome) ON (o.measurement_date)",
            "CREATE INDEX outcome_verification IF NOT EXISTS FOR (o:Outcome) ON (o.verification_status)",
        ]
        
        count = 0
        for index in indexes:
            try:
                self.client.execute_write(index)
                count += 1
                logger.debug(f"Created index: {index[:50]}...")
            except Exception as e:
                logger.warning(f"Index may already exist: {e}")
        
        return count
    
    def _create_fulltext_indexes(self) -> int:
        """Create fulltext search indexes."""
        fulltext_indexes = [
            # Government entities search
            """
            CREATE FULLTEXT INDEX government_search IF NOT EXISTS
            FOR (n:Ministry|Agency|Project)
            ON EACH [n.name, n.description, n.mandate]
            """,
            
            # News content search
            """
            CREATE FULLTEXT INDEX news_content_search IF NOT EXISTS
            FOR (n:NewsArticle)
            ON EACH [n.title, n.content, n.topics]
            """,
            
            # Social trends search
            """
            CREATE FULLTEXT INDEX social_trends_search IF NOT EXISTS
            FOR (st:SocialTrend)
            ON EACH [st.topic, st.related_hashtags]
            """,
        ]
        
        count = 0
        for index in fulltext_indexes:
            try:
                self.client.execute_write(index)
                count += 1
                logger.debug(f"Created fulltext index")
            except Exception as e:
                logger.warning(f"Fulltext index may already exist: {e}")
        
        return count
    
    def _drop_all_constraints(self):
        """Drop all constraints."""
        query = """
        CALL db.constraints()
        YIELD name
        CALL apoc.cypher.doIt('DROP CONSTRAINT ' + name, {})
        YIELD value
        RETURN count(*)
        """
        try:
            self.client.execute_write(query)
        except Exception as e:
            logger.warning(f"Error dropping constraints: {e}")
    
    def _drop_all_indexes(self):
        """Drop all indexes."""
        query = """
        CALL db.indexes()
        YIELD name
        WHERE name <> 'system'
        CALL apoc.cypher.doIt('DROP INDEX ' + name, {})
        YIELD value
        RETURN count(*)
        """
        try:
            self.client.execute_write(query)
        except Exception as e:
            logger.warning(f"Error dropping indexes: {e}")
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Get current schema information.
        
        Returns:
            Dictionary with schema statistics
        """
        info = {
            "constraints": [],
            "indexes": [],
            "node_labels": [],
            "relationship_types": [],
            "stats": {}
        }
        
        # Get constraints
        query = "SHOW CONSTRAINTS"
        try:
            result = self.client.execute_read(query)
            info["constraints"] = [r.get("name", "unknown") for r in result]
        except Exception as e:
            logger.error(f"Error getting constraints: {e}")
        
        # Get indexes
        query = "SHOW INDEXES"
        try:
            result = self.client.execute_read(query)
            info["indexes"] = [r.get("name", "unknown") for r in result]
        except Exception as e:
            logger.error(f"Error getting indexes: {e}")
        
        # Get node labels
        query = "CALL db.labels()"
        try:
            result = self.client.execute_read(query)
            info["node_labels"] = [r.get("label", "unknown") for r in result]
        except Exception as e:
            logger.error(f"Error getting node labels: {e}")
        
        # Get relationship types
        query = "CALL db.relationshipTypes()"
        try:
            result = self.client.execute_read(query)
            info["relationship_types"] = [
                r.get("relationshipType", "unknown") for r in result
            ]
        except Exception as e:
            logger.error(f"Error getting relationship types: {e}")
        
        # Get statistics
        query = """
        MATCH (n)
        WITH labels(n) as labels
        UNWIND labels as label
        RETURN label, count(*) as count
        ORDER BY count DESC
        """
        try:
            result = self.client.execute_read(query)
            info["stats"]["node_counts"] = {
                r["label"]: r["count"] for r in result
            }
        except Exception as e:
            logger.error(f"Error getting node counts: {e}")
        
        query = """
        MATCH ()-[r]->()
        RETURN type(r) as type, count(*) as count
        ORDER BY count DESC
        """
        try:
            result = self.client.execute_read(query)
            info["stats"]["relationship_counts"] = {
                r["type"]: r["count"] for r in result
            }
        except Exception as e:
            logger.error(f"Error getting relationship counts: {e}")
        
        return info
    
    def validate_schema(self) -> Dict[str, bool]:
        """
        Validate that schema is properly set up.
        
        Returns:
            Dictionary with validation results
        """
        validation = {
            "has_constraints": False,
            "has_indexes": False,
            "has_fulltext_indexes": False,
            "is_valid": False
        }
        
        schema_info = self.get_schema_info()
        
        validation["has_constraints"] = len(schema_info["constraints"]) > 0
        validation["has_indexes"] = len(schema_info["indexes"]) > 0
        
        # Check for fulltext indexes
        fulltext_count = sum(
            1 for idx in schema_info["indexes"]
            if "fulltext" in idx.lower() or "search" in idx.lower()
        )
        validation["has_fulltext_indexes"] = fulltext_count > 0
        
        # Overall validation
        validation["is_valid"] = all([
            validation["has_constraints"],
            validation["has_indexes"],
            validation["has_fulltext_indexes"]
        ])
        
        return validation
    
    def seed_initial_data(self) -> Dict[str, int]:
        """
        Seed database with initial reference data.
        
        Returns:
            Dictionary with seed counts
        """
        logger.info("Seeding initial data...")
        
        counts = {
            "states": 0,
            "geopolitical_zones": 0
        }
        
        # Create Nigerian states
        states_data = [
            {"name": "Abia", "capital": "Umuahia", "zone": "SE"},
            {"name": "Adamawa", "capital": "Yola", "zone": "NE"},
            {"name": "Akwa Ibom", "capital": "Uyo", "zone": "SS"},
            {"name": "Anambra", "capital": "Awka", "zone": "SE"},
            {"name": "Bauchi", "capital": "Bauchi", "zone": "NE"},
            {"name": "Bayelsa", "capital": "Yenagoa", "zone": "SS"},
            {"name": "Benue", "capital": "Makurdi", "zone": "NC"},
            {"name": "Borno", "capital": "Maiduguri", "zone": "NE"},
            {"name": "Cross River", "capital": "Calabar", "zone": "SS"},
            {"name": "Delta", "capital": "Asaba", "zone": "SS"},
            {"name": "Ebonyi", "capital": "Abakaliki", "zone": "SE"},
            {"name": "Edo", "capital": "Benin City", "zone": "SS"},
            {"name": "Ekiti", "capital": "Ado-Ekiti", "zone": "SW"},
            {"name": "Enugu", "capital": "Enugu", "zone": "SE"},
            {"name": "FCT", "capital": "Abuja", "zone": "NC"},
            {"name": "Gombe", "capital": "Gombe", "zone": "NE"},
            {"name": "Imo", "capital": "Owerri", "zone": "SE"},
            {"name": "Jigawa", "capital": "Dutse", "zone": "NW"},
            {"name": "Kaduna", "capital": "Kaduna", "zone": "NW"},
            {"name": "Kano", "capital": "Kano", "zone": "NW"},
            {"name": "Katsina", "capital": "Katsina", "zone": "NW"},
            {"name": "Kebbi", "capital": "Birnin Kebbi", "zone": "NW"},
            {"name": "Kogi", "capital": "Lokoja", "zone": "NC"},
            {"name": "Kwara", "capital": "Ilorin", "zone": "NC"},
            {"name": "Lagos", "capital": "Ikeja", "zone": "SW"},
            {"name": "Nasarawa", "capital": "Lafia", "zone": "NC"},
            {"name": "Niger", "capital": "Minna", "zone": "NC"},
            {"name": "Ogun", "capital": "Abeokuta", "zone": "SW"},
            {"name": "Ondo", "capital": "Akure", "zone": "SW"},
            {"name": "Osun", "capital": "Osogbo", "zone": "SW"},
            {"name": "Oyo", "capital": "Ibadan", "zone": "SW"},
            {"name": "Plateau", "capital": "Jos", "zone": "NC"},
            {"name": "Rivers", "capital": "Port Harcourt", "zone": "SS"},
            {"name": "Sokoto", "capital": "Sokoto", "zone": "NW"},
            {"name": "Taraba", "capital": "Jalingo", "zone": "NE"},
            {"name": "Yobe", "capital": "Damaturu", "zone": "NE"},
            {"name": "Zamfara", "capital": "Gusau", "zone": "NW"},
        ]
        
        for state in states_data:
            try:
                self.client.create_node(
                    "State",
                    {
                        "name": state["name"],
                        "capital": state["capital"],
                        "geopolitical_zone": state["zone"]
                    },
                    merge=True
                )
                counts["states"] += 1
            except Exception as e:
                logger.error(f"Error creating state {state['name']}: {e}")
        
        logger.info(f"Seeded {counts['states']} states")
        
        return counts
