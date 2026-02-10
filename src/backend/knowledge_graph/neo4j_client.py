"""
Neo4j Client for Nigerian Government Knowledge Graph
====================================================

Handles all Neo4j database connections, transactions, and query execution.
"""

import os
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
import logging

from neo4j import GraphDatabase, Driver, Session, Result
from neo4j.exceptions import ServiceUnavailable, AuthError

logger = logging.getLogger(__name__)


class Neo4jClient:
    """
    Neo4j database client with connection pooling and query execution.
    
    Supports both Neo4j AuraDB (cloud) and self-hosted instances.
    """
    
    def __init__(
        self,
        uri: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: str = "neo4j",
        max_connection_lifetime: int = 3600,
        max_connection_pool_size: int = 50,
        connection_timeout: int = 30
    ):
        """
        Initialize Neo4j client with connection parameters.
        
        Args:
            uri: Neo4j URI (e.g., neo4j+s://xxx.databases.neo4j.io)
            username: Database username
            password: Database password
            database: Database name (default: "neo4j")
            max_connection_lifetime: Max connection lifetime in seconds
            max_connection_pool_size: Max connections in pool
            connection_timeout: Connection timeout in seconds
        """
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.database = database or os.getenv("NEO4J_DATABASE", "neo4j")
        
        try:
            self.driver: Driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                max_connection_lifetime=max_connection_lifetime,
                max_connection_pool_size=max_connection_pool_size,
                connection_timeout=connection_timeout
            )
            logger.info(f"Connected to Neo4j at {self.uri}")
            self._verify_connectivity()
        except (ServiceUnavailable, AuthError) as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def _verify_connectivity(self) -> bool:
        """Verify database connectivity."""
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run("RETURN 1 AS num")
                record = result.single()
                return record["num"] == 1
        except Exception as e:
            logger.error(f"Connectivity check failed: {e}")
            return False
    
    @contextmanager
    def session(self, **kwargs) -> Session:
        """
        Context manager for Neo4j sessions.
        
        Usage:
            with client.session() as session:
                result = session.run("MATCH (n) RETURN n LIMIT 1")
        """
        session = self.driver.session(database=self.database, **kwargs)
        try:
            yield session
        finally:
            session.close()
    
    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        write: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            write: Whether this is a write transaction
            
        Returns:
            List of records as dictionaries
        """
        parameters = parameters or {}
        
        try:
            with self.session() as session:
                if write:
                    result = session.write_transaction(
                        lambda tx: tx.run(query, parameters)
                    )
                else:
                    result = session.read_transaction(
                        lambda tx: tx.run(query, parameters)
                    )
                
                return [record.data() for record in result]
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.debug(f"Query: {query}")
            logger.debug(f"Parameters: {parameters}")
            raise
    
    def execute_write(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a write transaction."""
        return self.execute_query(query, parameters, write=True)
    
    def execute_read(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a read transaction."""
        return self.execute_query(query, parameters, write=False)
    
    def batch_import(
        self,
        queries: List[str],
        parameters_list: List[Dict[str, Any]],
        batch_size: int = 1000
    ) -> int:
        """
        Execute batch import with multiple queries.
        
        Args:
            queries: List of Cypher queries
            parameters_list: List of parameter dicts (one per query)
            batch_size: Number of operations per transaction
            
        Returns:
            Total number of operations executed
        """
        total = 0
        
        with self.session() as session:
            for i in range(0, len(queries), batch_size):
                batch_queries = queries[i:i + batch_size]
                batch_params = parameters_list[i:i + batch_size]
                
                with session.begin_transaction() as tx:
                    for query, params in zip(batch_queries, batch_params):
                        tx.run(query, params)
                    tx.commit()
                
                total += len(batch_queries)
                logger.info(f"Imported batch {i // batch_size + 1}: {total} operations")
        
        return total
    
    def create_node(
        self,
        label: str,
        properties: Dict[str, Any],
        merge: bool = False
    ) -> Dict[str, Any]:
        """
        Create or merge a node.
        
        Args:
            label: Node label (e.g., "Ministry", "Agency")
            properties: Node properties
            merge: If True, use MERGE instead of CREATE
            
        Returns:
            Created/merged node properties
        """
        operation = "MERGE" if merge else "CREATE"
        
        # Build property string
        props_str = ", ".join(f"{k}: ${k}" for k in properties.keys())
        
        query = f"""
        {operation} (n:{label} {{{props_str}}})
        RETURN n
        """
        
        result = self.execute_write(query, properties)
        return result[0]["n"] if result else {}
    
    def create_relationship(
        self,
        from_label: str,
        from_property: str,
        from_value: Any,
        to_label: str,
        to_property: str,
        to_value: Any,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create a relationship between two nodes.
        
        Args:
            from_label: Source node label
            from_property: Property to match source node
            from_value: Value of property
            to_label: Target node label
            to_property: Property to match target node
            to_value: Value of property
            relationship_type: Type of relationship
            properties: Relationship properties
            
        Returns:
            True if successful
        """
        properties = properties or {}
        
        # Build relationship properties string
        if properties:
            props_str = "{" + ", ".join(f"{k}: ${k}" for k in properties.keys()) + "}"
        else:
            props_str = ""
        
        query = f"""
        MATCH (a:{from_label} {{{from_property}: $from_value}})
        MATCH (b:{to_label} {{{to_property}: $to_value}})
        MERGE (a)-[r:{relationship_type} {props_str}]->(b)
        RETURN r
        """
        
        params = {
            "from_value": from_value,
            "to_value": to_value,
            **properties
        }
        
        result = self.execute_write(query, params)
        return len(result) > 0
    
    def find_nodes(
        self,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Find nodes by label and optional properties.
        
        Args:
            label: Node label
            properties: Properties to filter by
            limit: Maximum results
            
        Returns:
            List of matching nodes
        """
        properties = properties or {}
        
        if properties:
            where_clauses = " AND ".join(f"n.{k} = ${k}" for k in properties.keys())
            query = f"""
            MATCH (n:{label})
            WHERE {where_clauses}
            RETURN n
            LIMIT {limit}
            """
        else:
            query = f"""
            MATCH (n:{label})
            RETURN n
            LIMIT {limit}
            """
        
        result = self.execute_read(query, properties)
        return [r["n"] for r in result]
    
    def get_node_relationships(
        self,
        label: str,
        property_name: str,
        property_value: Any,
        direction: str = "both"
    ) -> List[Dict[str, Any]]:
        """
        Get all relationships for a node.
        
        Args:
            label: Node label
            property_name: Property to identify node
            property_value: Property value
            direction: "outgoing", "incoming", or "both"
            
        Returns:
            List of relationships with connected nodes
        """
        if direction == "outgoing":
            pattern = "(n)-[r]->(m)"
        elif direction == "incoming":
            pattern = "(n)<-[r]-(m)"
        else:
            pattern = "(n)-[r]-(m)"
        
        query = f"""
        MATCH {pattern}
        WHERE n:{label} AND n.{property_name} = $value
        RETURN n, type(r) as relationship_type, properties(r) as rel_props, m
        """
        
        result = self.execute_read(query, {"value": property_value})
        return result
    
    def fulltext_search(
        self,
        index_name: str,
        query_string: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Perform fulltext search on indexed properties.
        
        Args:
            index_name: Name of fulltext index
            query_string: Search query
            limit: Maximum results
            
        Returns:
            List of matching nodes with scores
        """
        query = f"""
        CALL db.index.fulltext.queryNodes($index_name, $query_string)
        YIELD node, score
        RETURN node, score
        ORDER BY score DESC
        LIMIT {limit}
        """
        
        result = self.execute_read(
            query,
            {"index_name": index_name, "query_string": query_string}
        )
        return result
    
    def close(self):
        """Close the Neo4j driver connection."""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()


# Singleton instance for application-wide use
_client_instance: Optional[Neo4jClient] = None


def get_client() -> Neo4jClient:
    """Get or create singleton Neo4j client instance."""
    global _client_instance
    
    if _client_instance is None:
        _client_instance = Neo4jClient()
    
    return _client_instance


def close_client():
    """Close the singleton client instance."""
    global _client_instance
    
    if _client_instance:
        _client_instance.close()
        _client_instance = None
