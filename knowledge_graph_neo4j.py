#!/usr/bin/env python3
"""
Neo4j Knowledge Graph Implementation for Akulearn
Production-ready graph database integration for educational content
"""

import json
import os
import csv
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# Neo4j driver
try:
    from neo4j import GraphDatabase, basic_auth
    NEO4J_AVAILABLE = True
    print("✅ Neo4j driver available")
except ImportError as e:
    print(f"⚠️ Neo4j driver not available: {e}")
    print("💡 Install with: pip install neo4j")
    NEO4J_AVAILABLE = False
    GraphDatabase = None
    basic_auth = None

class NodeType(Enum):
    """Types of nodes in the Neo4j knowledge graph"""
    SUBJECT = "Subject"
    TOPIC = "Topic"
    SUBTOPIC = "Subtopic"
    CONCEPT = "Concept"
    SKILL = "Skill"
    LEARNING_OBJECTIVE = "LearningObjective"
    ASSESSMENT = "Assessment"
    RESOURCE = "Resource"
    PREREQUISITE = "Prerequisite"
    STUDENT = "Student"
    TEACHER = "Teacher"
    LEARNING_PATH = "LearningPath"

class RelationshipType(Enum):
    """Types of relationships in the Neo4j knowledge graph"""
    BELONGS_TO = "BELONGS_TO"
    PREREQUISITE_FOR = "PREREQUISITE_FOR"
    RELATED_TO = "RELATED_TO"
    BUILDS_ON = "BUILDS_ON"
    ASSESSES = "ASSESSES"
    TEACHES = "TEACHES"
    REQUIRES = "REQUIRES"
    COMPLETES = "COMPLETES"
    DIFFICULTY_LEVEL = "DIFFICULTY_LEVEL"
    EXAM_BOARD = "EXAM_BOARD"
    CONTAINS = "CONTAINS"
    RECOMMENDS = "RECOMMENDS"

@dataclass
class Neo4jConfig:
    """Neo4j database configuration"""
    uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user: str = os.getenv("NEO4J_USER", "neo4j")
    password: str = os.getenv("NEO4J_PASSWORD", "password")
    database: str = os.getenv("NEO4J_DATABASE", "neo4j")

class AkulearnKnowledgeGraph:
    """
    Neo4j-based knowledge graph for Akulearn educational platform
    """

    def __init__(self, config: Neo4jConfig = None):
        self.config = config or Neo4jConfig()
        self.driver = None
        self.subject_hierarchy = self._build_subject_hierarchy()

        if NEO4J_AVAILABLE:
            try:
                self.driver = GraphDatabase.driver(
                    self.config.uri,
                    auth=basic_auth(self.config.user, self.config.password)
                )
                # Test connection
                with self.driver.session() as session:
                    result = session.run("RETURN 'Connection successful' as message")
                    record = result.single()
                    print(f"✅ Neo4j Connection: {record['message']}")
            except Exception as e:
                print(f"❌ Neo4j Connection Failed: {e}")
                print("💡 Make sure Neo4j is running and credentials are correct")
                self.driver = None

    def _build_subject_hierarchy(self) -> Dict[str, Dict]:
        """Build the hierarchical structure of subjects and topics"""
        return {
            "Mathematics": {
                "topics": {
                    "Algebra": ["Equations", "Inequalities", "Functions", "Sequences"],
                    "Geometry": ["Coordinate Geometry", "Trigonometry", "Vectors"],
                    "Calculus": ["Differentiation", "Integration", "Limits"],
                    "Statistics": ["Probability", "Data Analysis", "Distributions"]
                }
            },
            "Physics": {
                "topics": {
                    "Mechanics": ["Kinematics", "Dynamics", "Energy", "Momentum"],
                    "Electricity": ["Circuits", "Magnetism", "Electromagnetic Induction"],
                    "Waves": ["Sound", "Light", "Wave Properties"],
                    "Modern Physics": ["Quantum Physics", "Nuclear Physics"]
                }
            },
            "Chemistry": {
                "topics": {
                    "Physical Chemistry": ["Chemical Kinetics", "Equilibrium", "Thermodynamics"],
                    "Organic Chemistry": ["Hydrocarbons", "Functional Groups", "Reactions"],
                    "Inorganic Chemistry": ["Periodic Table", "Chemical Bonding", "Acids & Bases"]
                }
            },
            "Biology": {
                "topics": {
                    "Cell Biology": ["Cell Structure", "Cell Functions", "Cell Division"],
                    "Genetics": ["DNA", "RNA", "Inheritance", "Mutations"],
                    "Ecology": ["Ecosystems", "Food Chains", "Biodiversity"]
                }
            },
            "English": {
                "topics": {
                    "Literature": ["Poetry", "Drama", "Prose", "Literary Devices"],
                    "Language": ["Grammar", "Comprehension", "Writing Skills"],
                    "Communication": ["Speaking", "Listening", "Reading"]
                }
            }
        }

    def create_constraints_and_indexes(self):
        """Create Neo4j constraints and indexes for optimal performance"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return

        constraints = [
            "CREATE CONSTRAINT subject_name_unique IF NOT EXISTS FOR (s:Subject) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT topic_name_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
            "CREATE CONSTRAINT resource_id_unique IF NOT EXISTS FOR (r:Resource) REQUIRE r.id IS UNIQUE",
            "CREATE CONSTRAINT student_id_unique IF NOT EXISTS FOR (st:Student) REQUIRE st.id IS UNIQUE",
            "CREATE INDEX subject_name_idx IF NOT EXISTS FOR (s:Subject) ON (s.name)",
            "CREATE INDEX topic_name_idx IF NOT EXISTS FOR (t:Topic) ON (t.name)",
            "CREATE INDEX resource_subject_idx IF NOT EXISTS FOR (r:Resource) ON (r.subject)",
            "CREATE INDEX resource_difficulty_idx IF NOT EXISTS FOR (r:Resource) ON (r.difficulty)"
        ]

        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"✅ Created: {constraint.split('FOR')[0].strip()}")
                except Exception as e:
                    print(f"⚠️ Constraint/Index may already exist: {e}")

    def create_subject_hierarchy(self):
        """Create the complete subject hierarchy in Neo4j"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return

        with self.driver.session() as session:
            for subject_name, subject_data in self.subject_hierarchy.items():
                # Create subject node
                session.run("""
                    MERGE (s:Subject {name: $subject_name})
                    SET s.description = $description,
                        s.exam_board = $exam_board,
                        s.difficulty_levels = $difficulty_levels,
                        s.estimated_completion_time = $completion_time,
                        s.created_at = datetime()
                """, {
                    "subject_name": subject_name,
                    "description": f"Complete {subject_name} curriculum for WAEC preparation",
                    "exam_board": "WAEC",
                    "difficulty_levels": ["basic", "intermediate", "advanced"],
                    "completion_time": "6 months"
                })

                # Create topic nodes and relationships
                for topic_name, subtopics in subject_data["topics"].items():
                    session.run("""
                        MERGE (t:Topic {name: $topic_name})
                        SET t.subject = $subject_name,
                            t.difficulty = $difficulty,
                            t.created_at = datetime()
                        WITH t
                        MATCH (s:Subject {name: $subject_name})
                        MERGE (t)-[:BELONGS_TO]->(s)
                    """, {
                        "topic_name": topic_name,
                        "subject_name": subject_name,
                        "difficulty": "intermediate"
                    })

                    # Create subtopic nodes
                    for subtopic in subtopics:
                        session.run("""
                            MERGE (st:Subtopic {name: $subtopic_name})
                            SET st.topic = $topic_name,
                                st.subject = $subject_name,
                                st.difficulty = $difficulty,
                                st.created_at = datetime()
                            WITH st
                            MATCH (t:Topic {name: $topic_name})
                            MERGE (st)-[:BELONGS_TO]->(t)
                        """, {
                            "subtopic_name": subtopic,
                            "topic_name": topic_name,
                            "subject_name": subject_name,
                            "difficulty": "intermediate"
                        })

        print(f"✅ Created subject hierarchy for {len(self.subject_hierarchy)} subjects")

    def integrate_csv_content(self):
        """Integrate existing CSV content into the knowledge graph"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return

        templates_dir = "content_templates"
        if not os.path.exists(templates_dir):
            print(f"⚠️ Templates directory not found: {templates_dir}")
            return

        total_resources = 0

        with self.driver.session() as session:
            for csv_file in os.listdir(templates_dir):
                if csv_file.endswith('.csv'):
                    csv_path = os.path.join(templates_dir, csv_file)
                    subject = csv_file.split('_')[2]  # Extract subject from filename

                    try:
                        with open(csv_path, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                # Create resource node
                                resource_id = f"{subject}_{row.get('title', '').lower().replace(' ', '_')}"

                                session.run("""
                                    MERGE (r:Resource {id: $resource_id})
                                    SET r.title = $title,
                                        r.subject = $subject,
                                        r.topic = $topic,
                                        r.subtopic = $subtopic,
                                        r.content_type = $content_type,
                                        r.difficulty = $difficulty,
                                        r.exam_board = $exam_board,
                                        r.content = $content,
                                        r.summary = $summary,
                                        r.learning_objectives = $learning_objectives,
                                        r.key_concepts = $key_concepts,
                                        r.practice_problems = $practice_problems,
                                        r.estimated_read_time = $read_time,
                                        r.tags = $tags,
                                        r.cultural_notes = $cultural_notes,
                                        r.created_at = datetime()
                                    WITH r
                                    MATCH (s:Subject {name: $subject})
                                    MERGE (r)-[:BELONGS_TO]->(s)
                                """, {
                                    "resource_id": resource_id,
                                    "title": row.get('title', ''),
                                    "subject": subject,
                                    "topic": row.get('topic', ''),
                                    "subtopic": row.get('subtopic', ''),
                                    "content_type": row.get('content_type', 'study_guide'),
                                    "difficulty": row.get('difficulty', 'intermediate'),
                                    "exam_board": row.get('exam_board', 'WAEC'),
                                    "content": row.get('content', ''),
                                    "summary": row.get('summary', ''),
                                    "learning_objectives": row.get('learning_objectives', ''),
                                    "key_concepts": row.get('key_concepts', ''),
                                    "practice_problems": row.get('practice_problems', ''),
                                    "read_time": row.get('estimated_read_time', '20'),
                                    "tags": row.get('tags', ''),
                                    "cultural_notes": row.get('cultural_notes', '')
                                })

                                # Connect to topic if it exists
                                topic_name = row.get('topic', '')
                                if topic_name:
                                    session.run("""
                                        MATCH (r:Resource {id: $resource_id})
                                        MATCH (t:Topic {name: $topic_name})
                                        MERGE (r)-[:BELONGS_TO]->(t)
                                    """, {
                                        "resource_id": resource_id,
                                        "topic_name": topic_name
                                    })

                                total_resources += 1

                        print(f"✅ Integrated {csv_file}")

                    except Exception as e:
                        print(f"❌ Error processing {csv_file}: {e}")

        print(f"✅ Integrated {total_resources} resources from CSV files")

    def create_prerequisite_relationships(self):
        """Create prerequisite relationships between topics"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return

        prerequisites = {
            "Calculus": ["Algebra", "Limits"],
            "Chemical Kinetics": ["Physical Chemistry", "Chemical Equilibrium"],
            "Organic Chemistry": ["Basic Chemistry", "Carbon Chemistry"],
            "Genetics": ["Cell Biology", "Molecular Biology"],
            "Electricity": ["Basic Physics", "Mathematics"],
            "Mechanics": ["Mathematics", "Basic Physics"]
        }

        with self.driver.session() as session:
            for advanced_topic, required_topics in prerequisites.items():
                for required_topic in required_topics:
                    session.run("""
                        MATCH (advanced:Topic {name: $advanced_topic})
                        MATCH (required:Topic {name: $required_topic})
                        MERGE (advanced)-[:PREREQUISITE_FOR {weight: 1.0}]->(required)
                    """, {
                        "advanced_topic": advanced_topic,
                        "required_topic": required_topic
                    })

        print("✅ Created prerequisite relationships")

    def create_learning_paths(self):
        """Create predefined learning paths"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return

        learning_paths = {
            "waec_science_track": {
                "name": "WAEC Science Track",
                "subjects": ["Mathematics", "Physics", "Chemistry", "Biology"],
                "duration_months": 6,
                "difficulty": "intermediate",
                "description": "Complete WAEC Science subjects preparation"
            },
            "engineering_foundation": {
                "name": "Engineering Foundation",
                "subjects": ["Mathematics", "Physics", "Chemistry"],
                "prerequisites": ["Basic Algebra", "Basic Physics"],
                "duration_months": 8,
                "difficulty": "advanced",
                "description": "Preparation for engineering undergraduate studies"
            },
            "medical_sciences": {
                "name": "Medical Sciences",
                "subjects": ["Biology", "Chemistry", "Physics", "Mathematics"],
                "prerequisites": ["Basic Biology", "Basic Chemistry"],
                "duration_months": 8,
                "difficulty": "advanced",
                "description": "Preparation for medical sciences"
            }
        }

        with self.driver.session() as session:
            for path_id, path_data in learning_paths.items():
                session.run("""
                    MERGE (lp:LearningPath {id: $path_id})
                    SET lp.name = $name,
                        lp.subjects = $subjects,
                        lp.prerequisites = $prerequisites,
                        lp.duration_months = $duration,
                        lp.difficulty = $difficulty,
                        lp.description = $description,
                        lp.created_at = datetime()
                """, {
                    "path_id": path_id,
                    "name": path_data["name"],
                    "subjects": path_data["subjects"],
                    "prerequisites": path_data.get("prerequisites", []),
                    "duration": path_data["duration_months"],
                    "difficulty": path_data["difficulty"],
                    "description": path_data["description"]
                })

                # Connect learning path to subjects
                for subject in path_data["subjects"]:
                    session.run("""
                        MATCH (lp:LearningPath {id: $path_id})
                        MATCH (s:Subject {name: $subject_name})
                        MERGE (lp)-[:RECOMMENDS]->(s)
                    """, {
                        "path_id": path_id,
                        "subject_name": subject
                    })

        print(f"✅ Created {len(learning_paths)} learning paths")

    def find_prerequisites(self, topic_name: str) -> List[Dict[str, Any]]:
        """Find all prerequisites for a given topic"""
        if not self.driver:
            return []

        with self.driver.session() as session:
            result = session.run("""
                MATCH (t:Topic {name: $topic_name})<-[:PREREQUISITE_FOR]-(prereq:Topic)
                RETURN prereq.name as prerequisite, prereq.subject as subject
                ORDER BY prereq.name
            """, {"topic_name": topic_name})

            return [{"name": record["prerequisite"], "subject": record["subject"]}
                   for record in result]

    def find_related_topics(self, subject_names: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Find related topics across subjects"""
        if not self.driver:
            return []

        with self.driver.session() as session:
            # Find topics from other subjects that are related
            result = session.run("""
                MATCH (t:Topic)
                WHERE NOT t.subject IN $subject_names
                RETURN t.name as topic, t.subject as subject, t.difficulty as difficulty
                ORDER BY t.name
                LIMIT $limit
            """, {
                "subject_names": subject_names,
                "limit": limit
            })

            return [{"topic": record["topic"],
                    "subject": record["subject"],
                    "difficulty": record["difficulty"]}
                   for record in result]

    def get_learning_path(self, path_id: str) -> Optional[Dict[str, Any]]:
        """Get details of a learning path"""
        if not self.driver:
            return None

        with self.driver.session() as session:
            result = session.run("""
                MATCH (lp:LearningPath {id: $path_id})
                RETURN lp.name as name, lp.subjects as subjects,
                       lp.prerequisites as prerequisites,
                       lp.duration_months as duration,
                       lp.difficulty as difficulty,
                       lp.description as description
            """, {"path_id": path_id})

            record = result.single()
            if record:
                return dict(record)
            return None

    def recommend_content(self, student_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend content based on student profile"""
        if not self.driver:
            return []

        current_level = student_profile.get("current_level", "beginner")
        target_subjects = student_profile.get("target_subjects", [])
        completed_topics = student_profile.get("completed_topics", [])

        with self.driver.session() as session:
            # Find resources matching criteria
            result = session.run("""
                MATCH (r:Resource)
                WHERE r.subject IN $target_subjects
                AND r.difficulty = $current_level
                AND NOT r.topic IN $completed_topics
                RETURN r.title as title, r.subject as subject, r.topic as topic,
                       r.difficulty as difficulty, r.estimated_read_time as read_time,
                       r.summary as summary
                ORDER BY r.subject, r.topic
                LIMIT 10
            """, {
                "target_subjects": target_subjects,
                "current_level": current_level,
                "completed_topics": completed_topics
            })

            return [dict(record) for record in result]

    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the knowledge graph"""
        if not self.driver:
            return {"error": "Neo4j not connected"}

        with self.driver.session() as session:
            # Node counts by type
            node_stats = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(*) as count
                ORDER BY count DESC
            """)

            # Relationship counts by type
            rel_stats = session.run("""
                MATCH ()-[r]-()
                RETURN type(r) as relationship_type, count(*) as count
                ORDER BY count DESC
            """)

            # Subject breakdown
            subject_stats = session.run("""
                MATCH (s:Subject)
                OPTIONAL MATCH (s)<-[:BELONGS_TO]-(r:Resource)
                RETURN s.name as subject, count(r) as resources
                ORDER BY resources DESC
            """)

            return {
                "node_counts": {record["label"]: record["count"] for record in node_stats},
                "relationship_counts": {record["relationship_type"]: record["count"] for record in rel_stats},
                "subject_resources": {record["subject"]: record["resources"] for record in subject_stats},
                "total_nodes": sum(record["count"] for record in node_stats),
                "total_relationships": sum(record["count"] for record in rel_stats)
            }

    def close(self):
        """Close the Neo4j driver connection"""
        if self.driver:
            self.driver.close()
            print("✅ Neo4j connection closed")

# ============================================================================
# INTEGRATION WITH EXISTING PLATFORM
# ============================================================================

class AkulearnGraphIntegration:
    """
    Integration layer between Neo4j knowledge graph and existing Akulearn platform
    """

    def __init__(self, graph: AkulearnKnowledgeGraph):
        self.graph = graph
        self.content_service_path = os.path.join(
            os.path.dirname(__file__),
            'connected_stack', 'backend', 'content_service.py'
        )

    def integrate_with_content_service(self):
        """Integrate knowledge graph with existing content service"""
        if not os.path.exists(self.content_service_path):
            print(f"⚠️ Content service not found at {self.content_service_path}")
            return

        # Read existing content service
        with open(self.content_service_path, 'r') as f:
            content = f.read()

        # Add knowledge graph integration methods
        integration_code = '''

    # ============================================================================
    # KNOWLEDGE GRAPH INTEGRATION
    # ============================================================================

    def get_knowledge_graph_recommendations(self, student_id: str, subject: str = None) -> Dict[str, Any]:
        """
        Get personalized recommendations from knowledge graph

        Args:
            student_id: Unique student identifier
            subject: Optional subject filter

        Returns:
            Dictionary with recommendations
        """
        try:
            from knowledge_graph_neo4j import AkulearnKnowledgeGraph

            kg = AkulearnKnowledgeGraph()
            student_profile = self.get_student_profile(student_id)

            if not student_profile:
                return {"error": "Student profile not found"}

            # Get recommendations
            recommendations = kg.recommend_content({
                "current_level": student_profile.get("level", "intermediate"),
                "target_subjects": [subject] if subject else student_profile.get("subjects", []),
                "completed_topics": student_profile.get("completed_topics", [])
            })

            # Get prerequisites
            prerequisites = []
            if subject:
                prereqs = kg.find_prerequisites(subject)
                prerequisites = [p["name"] for p in prereqs]

            # Get related topics
            related_topics = kg.find_related_topics(
                [subject] if subject else student_profile.get("subjects", [])
            )

            kg.close()

            return {
                "recommendations": recommendations,
                "prerequisites": prerequisites,
                "related_topics": related_topics,
                "learning_paths": self.get_suggested_learning_paths(student_id)
            }

        except Exception as e:
            return {"error": f"Knowledge graph integration failed: {str(e)}"}

    def get_learning_path_progress(self, student_id: str, path_id: str) -> Dict[str, Any]:
        """
        Get progress on a specific learning path

        Args:
            student_id: Student identifier
            path_id: Learning path identifier

        Returns:
            Progress information
        """
        try:
            from knowledge_graph_neo4j import AkulearnKnowledgeGraph

            kg = AkulearnKnowledgeGraph()
            path_info = kg.get_learning_path(path_id)

            if not path_info:
                return {"error": "Learning path not found"}

            # Calculate progress based on completed topics
            student_profile = self.get_student_profile(student_id)
            completed_topics = set(student_profile.get("completed_topics", []))

            path_subjects = path_info["subjects"]
            total_topics = 0
            completed_count = 0

            # Count topics in path subjects
            for subject in path_subjects:
                subject_topics = kg.subject_hierarchy.get(subject, {}).get("topics", {})
                for topic, subtopics in subject_topics.items():
                    total_topics += len(subtopics)
                    for subtopic in subtopics:
                        if subtopic in completed_topics:
                            completed_count += 1

            progress_percentage = (completed_count / total_topics * 100) if total_topics > 0 else 0

            kg.close()

            return {
                "path_name": path_info["name"],
                "progress_percentage": progress_percentage,
                "completed_topics": completed_count,
                "total_topics": total_topics,
                "remaining_subjects": [s for s in path_subjects if s not in completed_topics],
                "estimated_completion": f"{(total_topics - completed_count) * 2} hours"
            }

        except Exception as e:
            return {"error": f"Progress calculation failed: {str(e)}"}

    def get_suggested_learning_paths(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Suggest appropriate learning paths for a student

        Args:
            student_id: Student identifier

        Returns:
            List of suggested learning paths
        """
        student_profile = self.get_student_profile(student_id)
        if not student_profile:
            return []

        student_level = student_profile.get("level", "intermediate")
        target_goals = student_profile.get("goals", [])

        # Simple rule-based suggestions
        suggestions = []

        if "waec" in target_goals or "examination" in target_goals:
            if student_level in ["intermediate", "advanced"]:
                suggestions.append({
                    "path_id": "waec_science_track",
                    "name": "WAEC Science Track",
                    "reason": "Comprehensive preparation for WAEC science subjects"
                })

        if "engineering" in target_goals:
            suggestions.append({
                "path_id": "engineering_foundation",
                "name": "Engineering Foundation",
                "reason": "Essential preparation for engineering studies"
            })

        if "medical" in target_goals or "health" in target_goals:
            suggestions.append({
                "path_id": "medical_sciences",
                "name": "Medical Sciences",
                "reason": "Foundation for medical and health sciences"
            })

        return suggestions

    def get_student_profile(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student profile (placeholder - integrate with actual student service)

        Args:
            student_id: Student identifier

        Returns:
            Student profile dictionary
        """
        # Placeholder implementation
        # In real implementation, this would fetch from student database
        return {
            "id": student_id,
            "level": "intermediate",
            "subjects": ["Mathematics", "Physics", "Chemistry"],
            "completed_topics": ["Basic Algebra", "Mechanics"],
            "goals": ["waec", "engineering"],
            "preferences": ["visual_learning", "practice_problems"]
        }

'''

        # Insert integration code before the last class/method
        if "class " in content:
            # Find the last class definition
            classes = content.split("class ")
            if len(classes) > 1:
                # Insert before the last class
                last_class_index = content.rfind("class ")
                new_content = content[:last_class_index] + integration_code + "\n" + content[last_class_index:]

                with open(self.content_service_path, 'w') as f:
                    f.write(new_content)

                print("✅ Integrated knowledge graph with content service")
            else:
                print("⚠️ Could not find class definitions in content service")
        else:
            print("⚠️ Content service structure not recognized")

# ============================================================================
# IMPLEMENTATION PHASES
# ============================================================================

def phase_1_foundation():
    """Phase 1: Foundation - Basic Neo4j setup and subject hierarchy"""
    print("🚀 Phase 1: Foundation - Neo4j Knowledge Graph Setup")
    print("=" * 60)

    if not NEO4J_AVAILABLE:
        print("❌ Neo4j driver not installed. Install with: pip install neo4j")
        return

    kg = AkulearnKnowledgeGraph()

    if not kg.driver:
        print("❌ Cannot proceed without Neo4j connection")
        print("💡 Make sure Neo4j is running on bolt://localhost:7687")
        return

    try:
        # Create constraints and indexes
        print("📋 Creating constraints and indexes...")
        kg.create_constraints_and_indexes()

        # Create subject hierarchy
        print("🏗️ Building subject hierarchy...")
        kg.create_subject_hierarchy()

        # Create prerequisite relationships
        print("🔗 Creating prerequisite relationships...")
        kg.create_prerequisite_relationships()

        # Get statistics
        stats = kg.get_graph_statistics()
        print(f"\n📊 Phase 1 Results:")
        print(f"   Total Nodes: {stats.get('total_nodes', 0)}")
        print(f"   Total Relationships: {stats.get('total_relationships', 0)}")
        print(f"   Node Types: {stats.get('node_counts', {})}")

        print("✅ Phase 1 completed successfully!")

    except Exception as e:
        print(f"❌ Phase 1 failed: {e}")
    finally:
        kg.close()

def phase_2_content_integration():
    """Phase 2: Content Integration - CSV import and learning paths"""
    print("🚀 Phase 2: Content Integration - CSV Import & Learning Paths")
    print("=" * 60)

    if not NEO4J_AVAILABLE:
        print("❌ Neo4j driver not installed")
        return

    kg = AkulearnKnowledgeGraph()

    if not kg.driver:
        print("❌ Cannot proceed without Neo4j connection")
        return

    try:
        # Integrate CSV content
        print("📄 Integrating CSV content...")
        kg.integrate_csv_content()

        # Create learning paths
        print("🛤️ Creating learning paths...")
        kg.create_learning_paths()

        # Test query system
        print("🧪 Testing query system...")
        prereqs = kg.find_prerequisites("Calculus")
        print(f"   Prerequisites for Calculus: {[p['name'] for p in prereqs]}")

        related = kg.find_related_topics(["Mathematics"])
        print(f"   Related topics for Mathematics: {[r['topic'] for r in related[:3]]}")

        # Get final statistics
        stats = kg.get_graph_statistics()
        print(f"\n📊 Phase 2 Results:")
        print(f"   Total Resources: {stats.get('node_counts', {}).get('Resource', 0)}")
        print(f"   Learning Paths: {stats.get('node_counts', {}).get('LearningPath', 0)}")
        print(f"   Subject Resources: {stats.get('subject_resources', {})}")

        print("✅ Phase 2 completed successfully!")

    except Exception as e:
        print(f"❌ Phase 2 failed: {e}")
    finally:
        kg.close()

def phase_3_platform_integration():
    """Phase 3: Platform Integration - Connect with existing services"""
    print("🚀 Phase 3: Platform Integration - Content Service Connection")
    print("=" * 60)

    if not NEO4J_AVAILABLE:
        print("❌ Neo4j driver not installed")
        return

    try:
        # Initialize knowledge graph
        kg = AkulearnKnowledgeGraph()

        # Create integration layer
        integrator = AkulearnGraphIntegration(kg)

        # Integrate with content service
        print("🔗 Integrating with content service...")
        integrator.integrate_with_content_service()

        # Test integration
        print("🧪 Testing integration...")
        test_recommendations = kg.recommend_content({
            "current_level": "intermediate",
            "target_subjects": ["Mathematics", "Physics"],
            "completed_topics": ["Basic Algebra"]
        })

        print(f"   Sample recommendations: {len(test_recommendations)} items")

        if test_recommendations:
            sample = test_recommendations[0]
            print(f"   Example: {sample.get('title', 'N/A')} ({sample.get('subject', 'N/A')})")

        kg.close()
        print("✅ Phase 3 completed successfully!")

    except Exception as e:
        print(f"❌ Phase 3 failed: {e}")

def main():
    """Main function for Neo4j knowledge graph implementation"""
    print("🧠 Akulearn Neo4j Knowledge Graph Implementation")
    print("=" * 60)

    if not NEO4J_AVAILABLE:
        print("❌ Neo4j driver not available")
        print("Install with: pip install neo4j")
        print("\nAlso ensure Neo4j is running:")
        print("1. Download from: https://neo4j.com/download/")
        print("2. Start Neo4j Desktop or Server")
        print("3. Default connection: bolt://localhost:7687")
        print("4. Default credentials: neo4j/password")
        return

    # Run implementation phases
    try:
        phase_1_foundation()
        print("\n" + "="*60 + "\n")

        phase_2_content_integration()
        print("\n" + "="*60 + "\n")

        phase_3_platform_integration()

        print("\n🎉 All phases completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Start Neo4j server if not running")
        print("2. Run: python knowledge_graph_neo4j.py")
        print("3. Test API endpoints in content_service.py")
        print("4. Monitor performance and optimize queries")

    except KeyboardInterrupt:
        print("\n⚠️ Implementation interrupted by user")
    except Exception as e:
        print(f"\n❌ Implementation failed: {e}")

if __name__ == "__main__":
    main()