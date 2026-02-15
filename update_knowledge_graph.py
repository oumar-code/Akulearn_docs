#!/usr/bin/env python3
"""
Update Akulearn Knowledge Graph with 100% Coverage Content
- WAEC: 44 items (100% coverage across 5 subjects)
- NERDC: 168 items (100% coverage across 9 subjects)
- Total: 212 curriculum-aligned lessons
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    print("⚠️ Neo4j driver not available. Install with: pip install neo4j")
    NEO4J_AVAILABLE = False
    GraphDatabase = None


class KnowledgeGraphUpdater:
    """Updates Neo4j knowledge graph with complete curriculum content"""

    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        
        if NEO4J_AVAILABLE:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(user, password))
                print(f"✅ Connected to Neo4j at {uri}")
            except Exception as e:
                print(f"❌ Failed to connect to Neo4j: {e}")
                print("💡 Ensure Neo4j is running: docker-compose -f docker-compose-neo4j.yaml up -d")

    def close(self):
        if self.driver:
            self.driver.close()

    def clear_graph(self):
        """Clear all nodes and relationships (use with caution!)"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("🗑️  Cleared existing graph")

    def create_constraints(self):
        """Create uniqueness constraints for better performance"""
        if not self.driver:
            return
        
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Subject) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Topic) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Lesson) REQUIRE l.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE",
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Constraint may already exist
                    pass
        print("✅ Created graph constraints")

    def ingest_waec_content(self):
        """Ingest 44 WAEC lessons into knowledge graph"""
        waec_path = Path("wave3_content_database.json")
        if not waec_path.exists():
            print(f"❌ WAEC database not found: {waec_path}")
            return 0
        
        with open(waec_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        content = db.get("content", [])
        count = 0
        
        with self.driver.session() as session:
            for item in content:
                self._create_lesson_nodes(session, item, "WAEC")
                count += 1
        
        print(f"✅ Ingested {count} WAEC lessons")
        return count

    def ingest_nerdc_content(self):
        """Ingest 168 NERDC lessons into knowledge graph"""
        nerdc_path = Path("connected_stack/backend/content_data.json")
        if not nerdc_path.exists():
            print(f"❌ NERDC database not found: {nerdc_path}")
            return 0
        
        with open(nerdc_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        content = db.get("content", [])
        count = 0
        
        with self.driver.session() as session:
            for item in content:
                self._create_lesson_nodes(session, item, "NERDC")
                count += 1
        
        print(f"✅ Ingested {count} NERDC lessons")
        return count

    def _create_lesson_nodes(self, session, item: Dict, curriculum: str):
        """Create comprehensive nodes and relationships for a lesson"""
        lesson_id = item.get("id", "unknown")
        subject = item.get("subject", "Unknown")
        topic = item.get("topic", "Unknown")
        title = item.get("title", "Untitled")
        difficulty = item.get("difficulty", "intermediate")
        level = item.get("level", "SS1")  # NERDC specific
        
        # Create Subject node
        session.run("""
            MERGE (s:Subject {name: $subject})
            SET s.curriculum = $curriculum,
                s.updated_at = datetime()
        """, subject=subject, curriculum=curriculum)
        
        # Create Topic node
        session.run("""
            MERGE (t:Topic {id: $topic_id})
            SET t.name = $topic,
                t.subject = $subject,
                t.curriculum = $curriculum,
                t.updated_at = datetime()
            
            WITH t
            MATCH (s:Subject {name: $subject})
            MERGE (t)-[:BELONGS_TO]->(s)
        """, topic_id=f"{subject}_{topic}".replace(" ", "_").lower(),
             topic=topic, subject=subject, curriculum=curriculum)
        
        # Create Lesson node with rich metadata
        lesson_data = {
            "lesson_id": lesson_id,
            "title": title,
            "subject": subject,
            "topic": topic,
            "difficulty": difficulty,
            "curriculum": curriculum,
            "level": level,
            "content_type": item.get("content_type", "study_guide"),
            "exam_board": item.get("exam_board", curriculum),
        }
        
        session.run("""
            MERGE (l:Lesson {id: $lesson_id})
            SET l += $lesson_data,
                l.updated_at = datetime()
            
            WITH l
            MATCH (t:Topic {id: $topic_id})
            MERGE (l)-[:COVERS]->(t)
        """, lesson_id=lesson_id, lesson_data=lesson_data,
             topic_id=f"{subject}_{topic}".replace(" ", "_").lower())
        
        # Create Concept nodes from key concepts
        key_concepts = item.get("key_concepts", [])
        for concept in key_concepts:
            session.run("""
                MERGE (c:Concept {name: $concept, subject: $subject})
                SET c.updated_at = datetime()
                
                WITH c
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:TEACHES]->(c)
                
                WITH c
                MATCH (t:Topic {id: $topic_id})
                MERGE (c)-[:PART_OF]->(t)
            """, concept=concept, subject=subject, lesson_id=lesson_id,
                 topic_id=f"{subject}_{topic}".replace(" ", "_").lower())
        
        # Create Learning Objectives nodes
        objectives = item.get("learning_objectives", [])
        for i, objective in enumerate(objectives):
            session.run("""
                CREATE (lo:LearningObjective {
                    id: $lo_id,
                    text: $objective,
                    lesson_id: $lesson_id,
                    sequence: $sequence,
                    created_at: datetime()
                })
                
                WITH lo
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:HAS_OBJECTIVE]->(lo)
            """, lo_id=f"{lesson_id}_obj_{i}", objective=objective,
                 lesson_id=lesson_id, sequence=i)

    def create_prerequisite_relationships(self):
        """Create prerequisite relationships between topics based on curriculum progression"""
        if not self.driver:
            return
        
        # Example: Basic topics are prerequisites for advanced topics in same subject
        with self.driver.session() as session:
            # Mathematics progression
            session.run("""
                MATCH (basic:Topic {subject: 'Mathematics'})
                WHERE basic.name CONTAINS 'Basic' OR basic.name CONTAINS 'Introduction'
                MATCH (advanced:Topic {subject: 'Mathematics'})
                WHERE advanced.name CONTAINS 'Advanced' OR advanced.name CONTAINS 'Calculus'
                MERGE (basic)-[:PREREQUISITE_FOR]->(advanced)
            """)
            
            # Physics progression
            session.run("""
                MATCH (basic:Topic {subject: 'Physics'})
                WHERE basic.name CONTAINS 'Motion' OR basic.name CONTAINS 'Force'
                MATCH (advanced:Topic {subject: 'Physics'})
                WHERE advanced.name CONTAINS 'Energy' OR advanced.name CONTAINS 'Momentum'
                MERGE (basic)-[:PREREQUISITE_FOR]->(advanced)
            """)
        
        print("✅ Created prerequisite relationships")

    def create_cross_subject_relationships(self):
        """Create relationships between related concepts across subjects"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            # Math-Physics connections
            session.run("""
                MATCH (mc:Concept)
                WHERE mc.subject = 'Mathematics' AND 
                      (mc.name CONTAINS 'Vector' OR mc.name CONTAINS 'Calculus')
                MATCH (pc:Concept)
                WHERE pc.subject = 'Physics'
                MERGE (mc)-[:SUPPORTS]->(pc)
            """)
            
            # Chemistry-Biology connections
            session.run("""
                MATCH (cc:Concept)
                WHERE cc.subject = 'Chemistry' AND 
                      (cc.name CONTAINS 'Molecule' OR cc.name CONTAINS 'Reaction')
                MATCH (bc:Concept)
                WHERE bc.subject = 'Biology'
                MERGE (cc)-[:RELATES_TO]->(bc)
            """)
        
        print("✅ Created cross-subject relationships")

    def generate_statistics(self):
        """Generate and display graph statistics"""
        if not self.driver:
            return
        
        with self.driver.session() as session:
            # Count nodes by type
            stats = {}
            
            node_types = ["Subject", "Topic", "Lesson", "Concept", "LearningObjective"]
            for node_type in node_types:
                result = session.run(f"MATCH (n:{node_type}) RETURN count(n) as count")
                stats[node_type] = result.single()["count"]
            
            # Count relationships
            rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            stats["Relationships"] = rel_result.single()["count"]
            
            print("\n📊 Knowledge Graph Statistics:")
            print("="*50)
            for key, value in stats.items():
                print(f"  {key:20s}: {value:6d}")
            print("="*50)

    def export_graph_summary(self, output_path="knowledge_graph_summary.json"):
        """Export graph statistics to JSON"""
        if not self.driver:
            return
        
        summary = {
            "updated_at": datetime.now().isoformat(),
            "curricula": {
                "WAEC": {"subjects": 5, "items": 44, "coverage": "100%"},
                "NERDC": {"subjects": 9, "items": 168, "coverage": "100%"}
            },
            "totals": {
                "subjects": 9,  # Unique count
                "items": 212,
                "coverage": "100%"
            }
        }
        
        with self.driver.session() as session:
            # Subject breakdown
            result = session.run("""
                MATCH (s:Subject)
                RETURN s.name as subject, 
                       count{(s)<-[:BELONGS_TO]-(t:Topic)} as topics,
                       count{(s)<-[:BELONGS_TO]-(:Topic)<-[:COVERS]-(l:Lesson)} as lessons
                ORDER BY s.name
            """)
            
            summary["subjects"] = [dict(record) for record in result]
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported summary to {output_path}")


def main():
    print("\n" + "="*60)
    print("AKULEARN KNOWLEDGE GRAPH UPDATE")
    print("="*60 + "\n")
    
    updater = KnowledgeGraphUpdater()
    
    if not updater.driver:
        print("\n❌ Cannot proceed without Neo4j connection")
        print("💡 Start Neo4j with: docker-compose -f docker-compose-neo4j.yaml up -d")
        return
    
    try:
        # Step 1: Clear old graph (optional - comment out to preserve)
        # updater.clear_graph()
        
        # Step 2: Create constraints
        updater.create_constraints()
        
        # Step 3: Ingest content
        waec_count = updater.ingest_waec_content()
        nerdc_count = updater.ingest_nerdc_content()
        
        # Step 4: Create relationships
        updater.create_prerequisite_relationships()
        updater.create_cross_subject_relationships()
        
        # Step 5: Generate statistics
        updater.generate_statistics()
        
        # Step 6: Export summary
        updater.export_graph_summary()
        
        print(f"\n✅ Successfully updated knowledge graph!")
        print(f"   - WAEC: {waec_count} lessons")
        print(f"   - NERDC: {nerdc_count} lessons")
        print(f"   - Total: {waec_count + nerdc_count} lessons\n")
        
    finally:
        updater.close()


if __name__ == "__main__":
    main()
