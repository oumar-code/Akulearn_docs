#!/usr/bin/env python3
"""
Wave 3 Knowledge Graph Integration
Ingests all 21 SS1 lessons into Neo4j with comprehensive relationships
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime

try:
    from neo4j import GraphDatabase, basic_auth
    NEO4J_AVAILABLE = True
except ImportError:
    print("⚠️ Neo4j driver not available. Install with: pip install neo4j")
    NEO4J_AVAILABLE = False
    GraphDatabase = None
    basic_auth = None


@dataclass
class LessonComponent:
    """Represents a lesson component for the knowledge graph"""
    lesson_id: str
    component_type: str
    content: Any
    metadata: Dict[str, Any]


class Wave3KnowledgeGraphIntegration:
    """
    Integrates Wave 3 SS1 lessons into Neo4j knowledge graph
    Creates 147 nodes (21 lessons × 7 components)
    """

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password"):
        self.uri = neo4j_uri
        self.user = neo4j_user
        self.password = neo4j_password
        self.driver = None
        
        # Wave 3 subjects and their structure
        self.subjects = [
            "Chemistry", "Biology", "English Language", "Economics",
            "Geography", "History", "Computer Science"
        ]
        
        # Component types for each lesson
        self.component_types = [
            "LearningObjectives",
            "ContentSections",
            "WorkedExamples",
            "PracticeProblems",
            "Glossary",
            "Resources",
            "Assessment"
        ]
        
        # Prerequisite chains
        self.prerequisite_chains = {
            "Chemistry": [
                ("lesson_01_atomic_structure_and_chemical_bonding", "lesson_02_states_of_matter_and_properties"),
                ("lesson_02_states_of_matter_and_properties", "lesson_03_chemical_equations_and_reactions")
            ],
            "Biology": [
                ("lesson_01_cell_structure_and_functions", "lesson_02_genetics_and_heredity"),
                ("lesson_02_genetics_and_heredity", "lesson_03_ecology_and_nutrition")
            ],
            "English Language": [
                ("lesson_01_grammar_and_sentence_structure", "lesson_02_comprehension_and_vocabulary"),
                ("lesson_02_comprehension_and_vocabulary", "lesson_03_writing_skills_and_composition")
            ],
            "Economics": [
                ("lesson_01_basic_economics_concepts", "lesson_02_supply,_demand,_and_markets"),
                ("lesson_02_supply,_demand,_and_markets", "lesson_03_nigerian_economy_and_development")
            ],
            "Geography": [
                ("lesson_01_map_skills_and_cartography", "lesson_02_weather,_climate,_and_natural_resources"),
                ("lesson_02_weather,_climate,_and_natural_resources", "lesson_03_human_geography_and_settlements")
            ],
            "History": [
                ("lesson_01_pre-colonial_nigeria", "lesson_02_colonial_period_and_independence"),
                ("lesson_02_colonial_period_and_independence", "lesson_03_post-independence_nigeria")
            ],
            "Computer Science": [
                ("lesson_01_computer_hardware_and_software", "lesson_02_algorithms_and_programming_basics"),
                ("lesson_02_algorithms_and_programming_basics", "lesson_03_data_and_cybersecurity_fundamentals")
            ]
        }
        
        # Cross-subject connections
        self.cross_subject_connections = [
            ("Chemistry:lesson_01_atomic_structure_and_chemical_bonding", 
             "Biology:lesson_01_cell_structure_and_functions", "molecular_biology"),
            ("Chemistry:lesson_03_chemical_equations_and_reactions", 
             "Biology:lesson_03_ecology_and_nutrition", "biochemical_cycles"),
            ("Geography:lesson_02_weather,_climate,_and_natural_resources", 
             "Biology:lesson_03_ecology_and_nutrition", "environmental_science"),
            ("Economics:lesson_03_nigerian_economy_and_development", 
             "History:lesson_03_post-independence_nigeria", "economic_history"),
            ("Geography:lesson_03_human_geography_and_settlements", 
             "History:lesson_02_colonial_period_and_independence", "urbanization"),
            ("Computer Science:lesson_02_algorithms_and_programming_basics", 
             "Economics:lesson_02_supply,_demand,_and_markets", "algorithmic_economics")
        ]
        
        if NEO4J_AVAILABLE:
            self._connect()

    def _connect(self):
        """Connect to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=basic_auth(self.user, self.password)
            )
            with self.driver.session() as session:
                result = session.run("RETURN 'Connected' as status")
                record = result.single()
                print(f"✅ Neo4j Connection: {record['status']}")
        except Exception as e:
            print(f"❌ Neo4j Connection Failed: {e}")
            print("💡 Start Neo4j with: docker-compose -f docker-compose-neo4j.yaml up -d")
            self.driver = None

    def clear_existing_wave3_data(self):
        """Clear existing Wave 3 data from the graph"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        with self.driver.session() as session:
            # Delete Wave 3 lesson nodes and their relationships
            session.run("""
                MATCH (l:Lesson)
                WHERE l.grade = 'SS1' AND l.wave = 3
                DETACH DELETE l
            """)
            
            # Delete orphaned component nodes
            session.run("""
                MATCH (c)
                WHERE c:LearningObjectives OR c:ContentSection OR c:WorkedExample 
                   OR c:PracticeProblem OR c:GlossaryTerm OR c:Resource OR c:Assessment
                WHERE NOT (c)-[]-()
                DELETE c
            """)
            
            print("✅ Cleared existing Wave 3 data")

    def load_lesson_json(self, subject: str, lesson_file: str) -> Optional[Dict]:
        """Load lesson JSON file"""
        lesson_path = Path(f"content/ai_generated/textbooks/{subject}/SS1/{lesson_file}")
        
        if not lesson_path.exists():
            print(f"⚠️ Lesson not found: {lesson_path}")
            return None
        
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {lesson_path}: {e}")
            return None

    def create_lesson_node(self, session, subject: str, lesson_data: Dict, lesson_file: str):
        """Create main lesson node with metadata"""
        
        lesson_id = lesson_file.replace('.json', '')
        metadata = lesson_data.get('metadata', {})
        
        result = session.run("""
            MERGE (l:Lesson {id: $lesson_id})
            SET l.subject = $subject,
                l.grade = $grade,
                l.wave = $wave,
                l.title = $title,
                l.description = $description,
                l.duration_minutes = $duration_minutes,
                l.difficulty_level = $difficulty_level,
                l.nerdc_codes = $nerdc_codes,
                l.waec_topics = $waec_topics,
                l.keywords = $keywords,
                l.created_at = datetime(),
                l.last_updated = datetime()
            RETURN l.id as lesson_id
        """, {
            "lesson_id": lesson_id,
            "subject": subject,
            "grade": "SS1",
            "wave": 3,
            "title": metadata.get('title', ''),
            "description": metadata.get('description', ''),
            "duration_minutes": metadata.get('duration_minutes', 90),
            "difficulty_level": metadata.get('difficulty_level', 'intermediate'),
            "nerdc_codes": metadata.get('nerdc_references', []),
            "waec_topics": metadata.get('waec_tags', []),
            "keywords": metadata.get('keywords', [])
        })
        
        record = result.single()
        print(f"  ✅ Created lesson node: {record['lesson_id']}")
        return lesson_id

    def create_learning_objectives_nodes(self, session, lesson_id: str, objectives: List[str]):
        """Create learning objectives nodes"""
        for idx, objective in enumerate(objectives, 1):
            session.run("""
                MERGE (lo:LearningObjective {
                    id: $obj_id
                })
                SET lo.text = $text,
                    lo.order = $order,
                    lo.created_at = datetime()
                WITH lo
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:HAS_OBJECTIVE]->(lo)
            """, {
                "obj_id": f"{lesson_id}_obj_{idx}",
                "text": objective,
                "order": idx,
                "lesson_id": lesson_id
            })
        
        print(f"    ✅ Created {len(objectives)} learning objectives")

    def create_content_section_nodes(self, session, lesson_id: str, sections: List[Dict]):
        """Create content section nodes"""
        for idx, section in enumerate(sections, 1):
            session.run("""
                MERGE (cs:ContentSection {
                    id: $section_id
                })
                SET cs.title = $title,
                    cs.content = $content,
                    cs.duration_minutes = $duration,
                    cs.order = $order,
                    cs.created_at = datetime()
                WITH cs
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:HAS_SECTION]->(cs)
            """, {
                "section_id": f"{lesson_id}_section_{idx}",
                "title": section.get('title', ''),
                "content": section.get('content', ''),
                "duration": section.get('duration_minutes', 15),
                "order": idx,
                "lesson_id": lesson_id
            })
        
        print(f"    ✅ Created {len(sections)} content sections")

    def create_worked_example_nodes(self, session, lesson_id: str, examples: List[Dict]):
        """Create worked example nodes"""
        for idx, example in enumerate(examples, 1):
            session.run("""
                MERGE (we:WorkedExample {
                    id: $example_id
                })
                SET we.title = $title,
                    we.problem = $problem,
                    we.solution = $solution,
                    we.explanation = $explanation,
                    we.difficulty = $difficulty,
                    we.order = $order,
                    we.created_at = datetime()
                WITH we
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:HAS_EXAMPLE]->(we)
            """, {
                "example_id": f"{lesson_id}_example_{idx}",
                "title": example.get('title', ''),
                "problem": example.get('problem', ''),
                "solution": example.get('solution', ''),
                "explanation": example.get('explanation', ''),
                "difficulty": example.get('difficulty', 'medium'),
                "order": idx,
                "lesson_id": lesson_id
            })
        
        print(f"    ✅ Created {len(examples)} worked examples")

    def create_practice_problem_nodes(self, session, lesson_id: str, problems: List[Dict]):
        """Create practice problem nodes"""
        for idx, problem in enumerate(problems, 1):
            session.run("""
                MERGE (pp:PracticeProblem {
                    id: $problem_id
                })
                SET pp.question = $question,
                    pp.answer = $answer,
                    pp.difficulty = $difficulty,
                    pp.points = $points,
                    pp.hints = $hints,
                    pp.order = $order,
                    pp.created_at = datetime()
                WITH pp
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:HAS_PROBLEM]->(pp)
            """, {
                "problem_id": f"{lesson_id}_problem_{idx}",
                "question": problem.get('question', ''),
                "answer": problem.get('answer', ''),
                "difficulty": problem.get('difficulty', 'medium'),
                "points": problem.get('points', 1),
                "hints": problem.get('hints', []),
                "order": idx,
                "lesson_id": lesson_id
            })
        
        print(f"    ✅ Created {len(problems)} practice problems")

    def create_glossary_nodes(self, session, lesson_id: str, glossary: List[Dict]):
        """Create glossary term nodes"""
        for term in glossary:
            term_id = f"{lesson_id}_term_{term.get('term', '').lower().replace(' ', '_')}"
            session.run("""
                MERGE (gt:GlossaryTerm {
                    id: $term_id
                })
                SET gt.term = $term,
                    gt.definition = $definition,
                    gt.example = $example,
                    gt.subject = $subject,
                    gt.created_at = datetime()
                WITH gt
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:DEFINES_TERM]->(gt)
            """, {
                "term_id": term_id,
                "term": term.get('term', ''),
                "definition": term.get('definition', ''),
                "example": term.get('example', ''),
                "subject": term.get('subject', ''),
                "lesson_id": lesson_id
            })
        
        print(f"    ✅ Created {len(glossary)} glossary terms")

    def create_resource_nodes(self, session, lesson_id: str, resources: List[Dict]):
        """Create resource nodes"""
        for resource in resources:
            resource_id = f"{lesson_id}_resource_{resource.get('title', '').lower().replace(' ', '_')[:30]}"
            session.run("""
                MERGE (r:Resource {
                    id: $resource_id
                })
                SET r.title = $title,
                    r.type = $type,
                    r.url = $url,
                    r.description = $description,
                    r.created_at = datetime()
                WITH r
                MATCH (l:Lesson {id: $lesson_id})
                MERGE (l)-[:REFERENCES_RESOURCE]->(r)
            """, {
                "resource_id": resource_id,
                "title": resource.get('title', ''),
                "type": resource.get('type', 'external'),
                "url": resource.get('url', ''),
                "description": resource.get('description', ''),
                "lesson_id": lesson_id
            })
        
        print(f"    ✅ Created {len(resources)} resources")

    def create_assessment_node(self, session, lesson_id: str, assessment: Dict):
        """Create assessment node"""
        assessment_id = f"{lesson_id}_assessment"
        session.run("""
            MERGE (a:Assessment {
                id: $assessment_id
            })
            SET a.type = $type,
                a.duration_minutes = $duration,
                a.total_points = $total_points,
                a.passing_score = $passing_score,
                a.questions = $questions,
                a.created_at = datetime()
            WITH a
            MATCH (l:Lesson {id: $lesson_id})
            MERGE (l)-[:HAS_ASSESSMENT]->(a)
        """, {
            "assessment_id": assessment_id,
            "type": assessment.get('type', 'formative'),
            "duration": assessment.get('duration_minutes', 20),
            "total_points": assessment.get('total_points', 10),
            "passing_score": assessment.get('passing_score', 6),
            "questions": assessment.get('questions', []),
            "lesson_id": lesson_id
        })
        
        print(f"    ✅ Created assessment")

    def ingest_lesson(self, subject: str, lesson_file: str):
        """Ingest a complete lesson into the knowledge graph"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print(f"\n📚 Ingesting: {subject} - {lesson_file}")
        
        lesson_data = self.load_lesson_json(subject, lesson_file)
        if not lesson_data:
            return
        
        with self.driver.session() as session:
            # Create main lesson node
            lesson_id = self.create_lesson_node(session, subject, lesson_data, lesson_file)
            
            # Create component nodes
            if 'learning_objectives' in lesson_data:
                self.create_learning_objectives_nodes(
                    session, lesson_id, lesson_data['learning_objectives']
                )
            
            if 'content_sections' in lesson_data:
                self.create_content_section_nodes(
                    session, lesson_id, lesson_data['content_sections']
                )
            
            if 'worked_examples' in lesson_data:
                self.create_worked_example_nodes(
                    session, lesson_id, lesson_data['worked_examples']
                )
            
            if 'practice_problems' in lesson_data:
                self.create_practice_problem_nodes(
                    session, lesson_id, lesson_data['practice_problems']
                )
            
            if 'glossary' in lesson_data:
                self.create_glossary_nodes(
                    session, lesson_id, lesson_data['glossary']
                )
            
            if 'resources' in lesson_data:
                self.create_resource_nodes(
                    session, lesson_id, lesson_data['resources']
                )
            
            if 'assessment' in lesson_data:
                self.create_assessment_node(
                    session, lesson_id, lesson_data['assessment']
                )

    def create_prerequisite_relationships(self):
        """Create prerequisite relationships between lessons"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print("\n🔗 Creating prerequisite relationships...")
        
        with self.driver.session() as session:
            total = 0
            for subject, chains in self.prerequisite_chains.items():
                for prereq, advanced in chains:
                    session.run("""
                        MATCH (prereq:Lesson {id: $prereq_id})
                        MATCH (advanced:Lesson {id: $advanced_id})
                        MERGE (advanced)-[:REQUIRES_PREREQUISITE {
                            strength: 1.0,
                            created_at: datetime()
                        }]->(prereq)
                    """, {
                        "prereq_id": prereq,
                        "advanced_id": advanced
                    })
                    total += 1
                    print(f"  ✅ {subject}: {prereq} → {advanced}")
        
        print(f"✅ Created {total} prerequisite relationships")

    def create_cross_subject_connections(self):
        """Create cross-subject connections"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print("\n🌐 Creating cross-subject connections...")
        
        with self.driver.session() as session:
            for lesson1, lesson2, connection_type in self.cross_subject_connections:
                subject1, lesson1_id = lesson1.split(':')
                subject2, lesson2_id = lesson2.split(':')
                
                session.run("""
                    MATCH (l1:Lesson {id: $lesson1_id})
                    MATCH (l2:Lesson {id: $lesson2_id})
                    MERGE (l1)-[:CONNECTS_TO {
                        type: $connection_type,
                        bidirectional: true,
                        created_at: datetime()
                    }]->(l2)
                """, {
                    "lesson1_id": lesson1_id,
                    "lesson2_id": lesson2_id,
                    "connection_type": connection_type
                })
                
                print(f"  ✅ {subject1} ↔ {subject2}: {connection_type}")
        
        print(f"✅ Created {len(self.cross_subject_connections)} cross-subject connections")

    def create_curriculum_alignment_nodes(self):
        """Create NERDC and WAEC alignment nodes"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print("\n📋 Creating curriculum alignment nodes...")
        
        with self.driver.session() as session:
            # Get all unique NERDC codes and WAEC topics
            result = session.run("""
                MATCH (l:Lesson)
                WHERE l.wave = 3
                RETURN l.nerdc_codes as nerdc_codes, l.waec_topics as waec_topics
            """)
            
            nerdc_codes = set()
            waec_topics = set()
            
            for record in result:
                nerdc_codes.update(record['nerdc_codes'] or [])
                waec_topics.update(record['waec_topics'] or [])
            
            # Create NERDC nodes
            for code in nerdc_codes:
                session.run("""
                    MERGE (n:NERDCCode {code: $code})
                    SET n.created_at = datetime()
                """, {"code": code})
            
            # Create WAEC nodes
            for topic in waec_topics:
                session.run("""
                    MERGE (w:WAECTopic {topic: $topic})
                    SET w.created_at = datetime()
                """, {"topic": topic})
            
            # Link lessons to NERDC codes
            session.run("""
                MATCH (l:Lesson)
                WHERE l.wave = 3 AND l.nerdc_codes IS NOT NULL
                UNWIND l.nerdc_codes as code
                MATCH (n:NERDCCode {code: code})
                MERGE (l)-[:ALIGNS_WITH_NERDC]->(n)
            """)
            
            # Link lessons to WAEC topics
            session.run("""
                MATCH (l:Lesson)
                WHERE l.wave = 3 AND l.waec_topics IS NOT NULL
                UNWIND l.waec_topics as topic
                MATCH (w:WAECTopic {topic: topic})
                MERGE (l)-[:ALIGNS_WITH_WAEC]->(w)
            """)
            
            print(f"  ✅ Created {len(nerdc_codes)} NERDC nodes")
            print(f"  ✅ Created {len(waec_topics)} WAEC nodes")
            print(f"  ✅ Linked lessons to curriculum standards")

    def ingest_all_wave3_lessons(self):
        """Ingest all 21 Wave 3 lessons"""
        print("=" * 60)
        print("Wave 3 Knowledge Graph Integration")
        print("Ingesting 21 SS1 lessons into Neo4j")
        print("=" * 60)
        
        # Clear existing data
        self.clear_existing_wave3_data()
        
        # Lesson files for each subject
        lesson_files = {
            "Chemistry": [
                "lesson_01_atomic_structure_and_chemical_bonding.json",
                "lesson_02_states_of_matter_and_properties.json",
                "lesson_03_chemical_equations_and_reactions.json"
            ],
            "Biology": [
                "lesson_01_cell_structure_and_functions.json",
                "lesson_02_genetics_and_heredity.json",
                "lesson_03_ecology_and_nutrition.json"
            ],
            "English Language": [
                "lesson_01_grammar_and_sentence_structure.json",
                "lesson_02_comprehension_and_vocabulary.json",
                "lesson_03_writing_skills_and_composition.json"
            ],
            "Economics": [
                "lesson_01_basic_economics_concepts.json",
                "lesson_02_supply,_demand,_and_markets.json",
                "lesson_03_nigerian_economy_and_development.json"
            ],
            "Geography": [
                "lesson_01_map_skills_and_cartography.json",
                "lesson_02_weather,_climate,_and_natural_resources.json",
                "lesson_03_human_geography_and_settlements.json"
            ],
            "History": [
                "lesson_01_pre-colonial_nigeria.json",
                "lesson_02_colonial_period_and_independence.json",
                "lesson_03_post-independence_nigeria.json"
            ],
            "Computer Science": [
                "lesson_01_computer_hardware_and_software.json",
                "lesson_02_algorithms_and_programming_basics.json",
                "lesson_03_data_and_cybersecurity_fundamentals.json"
            ]
        }
        
        # Ingest all lessons
        total_lessons = 0
        for subject, files in lesson_files.items():
            for lesson_file in files:
                self.ingest_lesson(subject, lesson_file)
                total_lessons += 1
        
        # Create relationships
        self.create_prerequisite_relationships()
        self.create_cross_subject_connections()
        self.create_curriculum_alignment_nodes()
        
        # Generate statistics
        self.print_statistics()
        
        print("\n" + "=" * 60)
        print(f"✅ Integration Complete: {total_lessons} lessons ingested")
        print("=" * 60)

    def print_statistics(self):
        """Print knowledge graph statistics"""
        if not self.driver:
            return
        
        print("\n📊 Knowledge Graph Statistics:")
        
        with self.driver.session() as session:
            # Count nodes by type
            result = session.run("""
                MATCH (n)
                WHERE n:Lesson OR n:LearningObjective OR n:ContentSection 
                   OR n:WorkedExample OR n:PracticeProblem OR n:GlossaryTerm 
                   OR n:Resource OR n:Assessment
                RETURN labels(n)[0] as type, count(n) as count
                ORDER BY count DESC
            """)
            
            print("\n  Node Counts:")
            total_nodes = 0
            for record in result:
                count = record['count']
                total_nodes += count
                print(f"    {record['type']}: {count}")
            
            print(f"\n  Total Nodes: {total_nodes}")
            
            # Count relationships
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            print("\n  Relationship Counts:")
            total_rels = 0
            for record in result:
                count = record['count']
                total_rels += count
                print(f"    {record['rel_type']}: {count}")
            
            print(f"\n  Total Relationships: {total_rels}")

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            print("✅ Neo4j connection closed")


def main():
    """Main execution"""
    print("Starting Wave 3 Knowledge Graph Integration...")
    
    # Initialize integration
    integrator = Wave3KnowledgeGraphIntegration()
    
    if not integrator.driver:
        print("\n⚠️ Neo4j not available. Start with:")
        print("docker-compose -f docker-compose-neo4j.yaml up -d")
        return
    
    try:
        # Ingest all lessons
        integrator.ingest_all_wave3_lessons()
        
    finally:
        integrator.close()


if __name__ == "__main__":
    main()
