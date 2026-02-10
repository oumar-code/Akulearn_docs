"""Data validation module."""

import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, date

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate knowledge graph data."""
    
    @staticmethod
    def validate_entity(entity: Dict[str, Any], entity_type: str) -> Tuple[bool, List[str]]:
        """
        Validate an entity against expected schema.
        
        Args:
            entity: Entity data to validate
            entity_type: Type of entity (Ministry, Agency, etc.)
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        required_fields = {
            "Ministry": ["id", "name", "sector"],
            "Agency": ["id", "name", "acronym"],
            "CorruptionCase": ["id", "case_id", "title", "value_involved"],
            "NGO": ["id", "name", "mission"],
            "Conflict": ["id", "name", "type", "status"],
            "NewsArticle": ["id", "title", "source", "url"],
        }
        
        if entity_type in required_fields:
            for field in required_fields[entity_type]:
                if field not in entity or entity[field] is None:
                    errors.append(f"Missing required field: {field}")
        
        # Validate common field types
        if "id" in entity and not isinstance(entity["id"], str):
            errors.append("ID must be string")
        
        if "name" in entity and not isinstance(entity["name"], str):
            errors.append("Name must be string")
        
        # Validate numeric fields
        numeric_fields = ["budget_annual", "value_involved", "amount", "sentiment", "bias_score"]
        for field in numeric_fields:
            if field in entity and entity[field] is not None:
                if not isinstance(entity[field], (int, float)):
                    errors.append(f"{field} must be numeric")
        
        # Validate score fields (0-1)
        score_fields = ["credibility_score", "bias_score", "sentiment", "credibility_rating"]
        for field in score_fields:
            if field in entity and entity[field] is not None:
                if not (-1 <= entity[field] <= 1):
                    errors.append(f"{field} must be between -1 and 1")
        
        # Validate date fields
        date_fields = ["date_reported", "start_date", "founded_date", "established"]
        for field in date_fields:
            if field in entity and entity[field] is not None:
                if not isinstance(entity[field], (str, date, datetime)):
                    errors.append(f"{field} must be a date")
        
        # Entity-specific validation
        if entity_type == "Ministry" and "level" in entity:
            if entity["level"] not in ["federal", "state"]:
                errors.append("Ministry level must be 'federal' or 'state'")
        
        if entity_type == "CorruptionCase" and "status" in entity:
            valid_statuses = ["ongoing", "concluded", "dismissed", "suspended"]
            if entity["status"] not in valid_statuses:
                errors.append(f"Case status must be one of: {valid_statuses}")
        
        if entity_type == "Conflict" and "type" in entity:
            valid_types = ["armed", "insurgency", "terrorism", "war", "civil_unrest"]
            if entity["type"] not in valid_types:
                errors.append(f"Conflict type must be one of: {valid_types}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_relationship(
        rel: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        """
        Validate a relationship definition.
        
        Args:
            rel: Relationship data
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        required_fields = ["start_id", "end_id", "type"]
        for field in required_fields:
            if field not in rel or rel[field] is None:
                errors.append(f"Missing required field: {field}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def deduplicate_entities(
        entities: List[Dict[str, Any]],
        key_fields: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate entities based on key fields.
        
        Args:
            entities: List of entities
            key_fields: Fields that define uniqueness
            
        Returns:
            List of deduplicated entities
        """
        seen = set()
        deduplicated = []
        
        for entity in entities:
            # Create key from specified fields
            key = tuple(entity.get(field, None) for field in key_fields)
            if key not in seen:
                seen.add(key)
                deduplicated.append(entity)
        
        logger.info(f"Deduplicated {len(entities) - len(deduplicated)} duplicate entities")
        return deduplicated
    
    @staticmethod
    def validate_batch(
        entities: List[Dict[str, Any]],
        entity_type: str,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Validate a batch of entities.
        
        Args:
            entities: List of entities to validate
            entity_type: Type of entities
            
        Returns:
            Tuple of (valid_entities, invalid_entities_with_errors)
        """
        valid = []
        invalid = []
        
        for entity in entities:
            is_valid, errors = DataValidator.validate_entity(entity, entity_type)
            if is_valid:
                valid.append(entity)
            else:
                invalid.append({
                    "entity": entity,
                    "errors": errors
                })
        
        logger.info(f"Validated {len(valid)} valid and {len(invalid)} invalid {entity_type} entities")
        return valid, invalid
    
    @staticmethod
    def check_data_quality(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check overall data quality of entity batch.
        
        Args:
            entities: List of entities
            
        Returns:
            Quality metrics
        """
        if not entities:
            return {"total": 0, "completeness": 0.0}
        
        total_fields_possible = 0
        total_fields_filled = 0
        
        for entity in entities:
            total_fields_possible += len(entity)
            for value in entity.values():
                if value is not None and value != "":
                    total_fields_filled += 1
        
        completeness = (total_fields_filled / total_fields_possible * 100
                       if total_fields_possible > 0 else 0)
        
        return {
            "total_entities": len(entities),
            "total_fields": total_fields_filled,
            "completeness_percentage": round(completeness, 2),
            "avg_fields_per_entity": round(
                total_fields_filled / len(entities), 2
            ) if entities else 0
        }
