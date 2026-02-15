#!/usr/bin/env python3
"""
Cross-Subject Connections & Learning Paths
Expands interdisciplinary links and creates thematic learning pathways
"""

import json
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from neo4j import GraphDatabase, basic_auth
    NEO4J_AVAILABLE = True
except (ImportError, Exception):
    NEO4J_AVAILABLE = False
    GraphDatabase = None


class ConnectionType(Enum):
    """Types of cross-subject connections"""
    MOLECULAR_BIOLOGY = "molecular_biology"
    BIOCHEMICAL_CYCLES = "biochemical_cycles"
    ENVIRONMENTAL_SCIENCE = "environmental_science"
    ECONOMIC_HISTORY = "economic_history"
    URBANIZATION = "urbanization"
    ALGORITHMIC_ECONOMICS = "algorithmic_economics"
    # New connections
    MATHEMATICAL_PHYSICS = "mathematical_physics"
    CHEMICAL_ECOLOGY = "chemical_ecology"
    COMPUTATIONAL_BIOLOGY = "computational_biology"
    GEO_ECONOMICS = "geo_economics"
    HISTORICAL_GEOGRAPHY = "historical_geography"
    LANGUAGE_HISTORY = "language_history"
    ECONOMIC_GEOGRAPHY = "economic_geography"
    SCIENTIFIC_COMMUNICATION = "scientific_communication"
    DATA_SCIENCE = "data_science"
    SYSTEMS_THINKING = "systems_thinking"


class SkillType(Enum):
    """Transferable skills across subjects"""
    CRITICAL_THINKING = "critical_thinking"
    PROBLEM_SOLVING = "problem_solving"
    DATA_ANALYSIS = "data_analysis"
    SCIENTIFIC_METHOD = "scientific_method"
    COMMUNICATION = "communication"
    RESEARCH = "research"
    COMPUTATION = "computation"
    VISUAL_LITERACY = "visual_literacy"
    SYSTEMS_THINKING = "systems_thinking"
    ETHICAL_REASONING = "ethical_reasoning"


@dataclass
class LearningPath:
    """Thematic learning path across subjects"""
    path_id: str
    name: str
    description: str
    theme: str
    duration_weeks: int
    difficulty_level: str
    lesson_sequence: List[str]
    skills_developed: List[SkillType]
    prerequisites: List[str]
    learning_outcomes: List[str]


@dataclass
class SkillConnection:
    """Skill-based connection between lessons"""
    skill: SkillType
    lesson_ids: List[str]
    strength: float  # 0.0 to 1.0


class CrossSubjectExpander:
    """
    Expands cross-subject connections and creates learning paths
    """

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password"):
        self.uri = neo4j_uri
        self.user = neo4j_user
        self.password = neo4j_password
        self.driver = None
        
        # Extended cross-subject connections
        self.extended_connections = [
            # Original 6 + 9 new = 15 total
            ("Chemistry:lesson_01_atomic_structure_and_chemical_bonding", 
             "Biology:lesson_01_cell_structure_and_functions", 
             ConnectionType.MOLECULAR_BIOLOGY, 0.9),
            
            ("Chemistry:lesson_03_chemical_equations_and_reactions", 
             "Biology:lesson_03_ecology_and_nutrition", 
             ConnectionType.BIOCHEMICAL_CYCLES, 0.85),
            
            ("Geography:lesson_02_weather,_climate,_and_natural_resources", 
             "Biology:lesson_03_ecology_and_nutrition", 
             ConnectionType.ENVIRONMENTAL_SCIENCE, 0.9),
            
            ("Economics:lesson_03_nigerian_economy_and_development", 
             "History:lesson_03_post-independence_nigeria", 
             ConnectionType.ECONOMIC_HISTORY, 0.95),
            
            ("Geography:lesson_03_human_geography_and_settlements", 
             "History:lesson_02_colonial_period_and_independence", 
             ConnectionType.URBANIZATION, 0.8),
            
            ("Computer Science:lesson_02_algorithms_and_programming_basics", 
             "Economics:lesson_02_supply,_demand,_and_markets", 
             ConnectionType.ALGORITHMIC_ECONOMICS, 0.7),
            
            # New connections
            ("Chemistry:lesson_02_states_of_matter_and_properties", 
             "Geography:lesson_02_weather,_climate,_and_natural_resources", 
             ConnectionType.CHEMICAL_ECOLOGY, 0.75),
            
            ("Computer Science:lesson_01_computer_hardware_and_software", 
             "Biology:lesson_02_genetics_and_heredity", 
             ConnectionType.COMPUTATIONAL_BIOLOGY, 0.7),
            
            ("Economics:lesson_01_basic_economics_concepts", 
             "Geography:lesson_03_human_geography_and_settlements", 
             ConnectionType.GEO_ECONOMICS, 0.85),
            
            ("History:lesson_01_pre-colonial_nigeria", 
             "Geography:lesson_03_human_geography_and_settlements", 
             ConnectionType.HISTORICAL_GEOGRAPHY, 0.8),
            
            ("English Language:lesson_03_writing_skills_and_composition", 
             "History:lesson_02_colonial_period_and_independence", 
             ConnectionType.LANGUAGE_HISTORY, 0.7),
            
            ("Economics:lesson_02_supply,_demand,_and_markets", 
             "Geography:lesson_02_weather,_climate,_and_natural_resources", 
             ConnectionType.ECONOMIC_GEOGRAPHY, 0.75),
            
            ("English Language:lesson_02_comprehension_and_vocabulary", 
             "Biology:lesson_01_cell_structure_and_functions", 
             ConnectionType.SCIENTIFIC_COMMUNICATION, 0.65),
            
            ("Computer Science:lesson_03_data_and_cybersecurity_fundamentals", 
             "Economics:lesson_01_basic_economics_concepts", 
             ConnectionType.DATA_SCIENCE, 0.8),
            
            ("English Language:lesson_01_grammar_and_sentence_structure", 
             "Computer Science:lesson_02_algorithms_and_programming_basics", 
             ConnectionType.SYSTEMS_THINKING, 0.6),
        ]
        
        # Thematic learning paths
        self.learning_paths = [
            LearningPath(
                path_id="path_environmental_science",
                name="Environmental Science & Sustainability",
                description="Explore the interconnections between chemistry, biology, and geography in environmental systems",
                theme="environment",
                duration_weeks=6,
                difficulty_level="intermediate",
                lesson_sequence=[
                    "lesson_02_states_of_matter_and_properties",  # Chemistry
                    "lesson_03_ecology_and_nutrition",  # Biology
                    "lesson_02_weather,_climate,_and_natural_resources",  # Geography
                    "lesson_03_human_geography_and_settlements"  # Geography
                ],
                skills_developed=[
                    SkillType.SYSTEMS_THINKING,
                    SkillType.SCIENTIFIC_METHOD,
                    SkillType.DATA_ANALYSIS,
                    SkillType.CRITICAL_THINKING
                ],
                prerequisites=[],
                learning_outcomes=[
                    "Understand chemical processes in natural systems",
                    "Analyze ecological interactions and nutrient cycles",
                    "Evaluate climate change impacts",
                    "Propose sustainable development solutions"
                ]
            ),
            
            LearningPath(
                path_id="path_nigerian_development",
                name="Nigerian Development: History, Economy & Geography",
                description="Examine Nigeria's development through historical, economic, and geographical perspectives",
                theme="nigerian_studies",
                duration_weeks=5,
                difficulty_level="intermediate",
                lesson_sequence=[
                    "lesson_01_pre-colonial_nigeria",  # History
                    "lesson_02_colonial_period_and_independence",  # History
                    "lesson_03_post-independence_nigeria",  # History
                    "lesson_03_human_geography_and_settlements",  # Geography
                    "lesson_03_nigerian_economy_and_development"  # Economics
                ],
                skills_developed=[
                    SkillType.CRITICAL_THINKING,
                    SkillType.RESEARCH,
                    SkillType.COMMUNICATION,
                    SkillType.ETHICAL_REASONING
                ],
                prerequisites=[],
                learning_outcomes=[
                    "Trace Nigeria's historical development",
                    "Analyze urbanization patterns",
                    "Evaluate economic policies and challenges",
                    "Propose development strategies"
                ]
            ),
            
            LearningPath(
                path_id="path_scientific_foundations",
                name="Scientific Foundations: Chemistry & Biology",
                description="Build core scientific knowledge through chemistry and biology",
                theme="science",
                duration_weeks=6,
                difficulty_level="intermediate",
                lesson_sequence=[
                    "lesson_01_atomic_structure_and_chemical_bonding",  # Chemistry
                    "lesson_01_cell_structure_and_functions",  # Biology
                    "lesson_02_genetics_and_heredity",  # Biology
                    "lesson_03_chemical_equations_and_reactions",  # Chemistry
                    "lesson_03_ecology_and_nutrition"  # Biology
                ],
                skills_developed=[
                    SkillType.SCIENTIFIC_METHOD,
                    SkillType.PROBLEM_SOLVING,
                    SkillType.DATA_ANALYSIS,
                    SkillType.SYSTEMS_THINKING
                ],
                prerequisites=[],
                learning_outcomes=[
                    "Understand atomic and molecular structure",
                    "Analyze cellular processes",
                    "Apply genetic principles",
                    "Investigate ecological systems"
                ]
            ),
            
            LearningPath(
                path_id="path_computational_thinking",
                name="Computational Thinking Across Disciplines",
                description="Apply computational thinking to economics, biology, and data analysis",
                theme="computation",
                duration_weeks=4,
                difficulty_level="intermediate_to_advanced",
                lesson_sequence=[
                    "lesson_01_computer_hardware_and_software",  # CS
                    "lesson_02_algorithms_and_programming_basics",  # CS
                    "lesson_03_data_and_cybersecurity_fundamentals",  # CS
                    "lesson_02_supply,_demand,_and_markets"  # Economics
                ],
                skills_developed=[
                    SkillType.COMPUTATION,
                    SkillType.PROBLEM_SOLVING,
                    SkillType.DATA_ANALYSIS,
                    SkillType.SYSTEMS_THINKING
                ],
                prerequisites=[],
                learning_outcomes=[
                    "Master algorithmic thinking",
                    "Apply programming to real-world problems",
                    "Analyze data patterns",
                    "Model economic systems computationally"
                ]
            ),
            
            LearningPath(
                path_id="path_communication_literacy",
                name="Communication & Scientific Literacy",
                description="Develop communication skills through language and scientific writing",
                theme="communication",
                duration_weeks=4,
                difficulty_level="intermediate",
                lesson_sequence=[
                    "lesson_01_grammar_and_sentence_structure",  # English
                    "lesson_02_comprehension_and_vocabulary",  # English
                    "lesson_03_writing_skills_and_composition",  # English
                    "lesson_01_cell_structure_and_functions"  # Biology (scientific writing)
                ],
                skills_developed=[
                    SkillType.COMMUNICATION,
                    SkillType.CRITICAL_THINKING,
                    SkillType.RESEARCH,
                    SkillType.VISUAL_LITERACY
                ],
                prerequisites=[],
                learning_outcomes=[
                    "Master academic writing conventions",
                    "Communicate scientific concepts clearly",
                    "Analyze complex texts",
                    "Present arguments effectively"
                ]
            ),
            
            LearningPath(
                path_id="path_systems_analysis",
                name="Systems Analysis: Geography, Economics & History",
                description="Analyze complex systems through geographic, economic, and historical lenses",
                theme="systems",
                duration_weeks=5,
                difficulty_level="advanced",
                lesson_sequence=[
                    "lesson_01_map_skills_and_cartography",  # Geography
                    "lesson_01_basic_economics_concepts",  # Economics
                    "lesson_02_supply,_demand,_and_markets",  # Economics
                    "lesson_02_weather,_climate,_and_natural_resources",  # Geography
                    "lesson_02_colonial_period_and_independence"  # History
                ],
                skills_developed=[
                    SkillType.SYSTEMS_THINKING,
                    SkillType.DATA_ANALYSIS,
                    SkillType.CRITICAL_THINKING,
                    SkillType.VISUAL_LITERACY
                ],
                prerequisites=[],
                learning_outcomes=[
                    "Analyze spatial patterns",
                    "Model economic systems",
                    "Evaluate historical causation",
                    "Synthesize multidisciplinary perspectives"
                ]
            )
        ]
        
        self._connect()

    def _connect(self):
        """Connect to Neo4j"""
        try:
            from neo4j import GraphDatabase, basic_auth
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 7687))
            sock.close()
            
            if result != 0:
                return
            
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=basic_auth(self.user, self.password)
            )
            print("✅ Connected to Neo4j for cross-subject expansion")
        except Exception:
            pass

    def create_extended_connections(self):
        """Create extended cross-subject connections"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print("\n🌐 Creating extended cross-subject connections...")
        
        with self.driver.session() as session:
            created = 0
            for lesson1, lesson2, conn_type, strength in self.extended_connections:
                subject1, lesson1_id = lesson1.split(':')
                subject2, lesson2_id = lesson2.split(':')
                
                session.run("""
                    MATCH (l1:Lesson {id: $lesson1_id})
                    MATCH (l2:Lesson {id: $lesson2_id})
                    MERGE (l1)-[c:CONNECTS_TO {
                        type: $connection_type,
                        strength: $strength,
                        bidirectional: true,
                        created_at: datetime()
                    }]->(l2)
                """, {
                    "lesson1_id": lesson1_id,
                    "lesson2_id": lesson2_id,
                    "connection_type": conn_type.value,
                    "strength": strength
                })
                
                created += 1
                print(f"  ✅ {subject1} ↔ {subject2}: {conn_type.value} (strength: {strength})")
        
        print(f"\n✅ Created {created} cross-subject connections")

    def create_learning_paths(self):
        """Create thematic learning paths"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print("\n🛤️  Creating thematic learning paths...")
        
        with self.driver.session() as session:
            for path in self.learning_paths:
                # Create learning path node
                session.run("""
                    MERGE (lp:LearningPath {id: $path_id})
                    SET lp.name = $name,
                        lp.description = $description,
                        lp.theme = $theme,
                        lp.duration_weeks = $duration_weeks,
                        lp.difficulty_level = $difficulty_level,
                        lp.skills_developed = $skills_developed,
                        lp.prerequisites = $prerequisites,
                        lp.learning_outcomes = $learning_outcomes,
                        lp.created_at = datetime()
                """, {
                    "path_id": path.path_id,
                    "name": path.name,
                    "description": path.description,
                    "theme": path.theme,
                    "duration_weeks": path.duration_weeks,
                    "difficulty_level": path.difficulty_level,
                    "skills_developed": [s.value for s in path.skills_developed],
                    "prerequisites": path.prerequisites,
                    "learning_outcomes": path.learning_outcomes
                })
                
                # Link lessons in sequence
                for order, lesson_id in enumerate(path.lesson_sequence, 1):
                    session.run("""
                        MATCH (lp:LearningPath {id: $path_id})
                        MATCH (l:Lesson)
                        WHERE l.id CONTAINS $lesson_id
                        MERGE (lp)-[:INCLUDES_LESSON {
                            order: $order,
                            total_lessons: $total
                        }]->(l)
                    """, {
                        "path_id": path.path_id,
                        "lesson_id": lesson_id,
                        "order": order,
                        "total": len(path.lesson_sequence)
                    })
                
                print(f"  ✅ {path.name} ({len(path.lesson_sequence)} lessons)")
        
        print(f"\n✅ Created {len(self.learning_paths)} learning paths")

    def create_skill_connections(self):
        """Create skill-based connections between lessons"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return
        
        print("\n🎯 Creating skill-based connections...")
        
        # Define skill mappings
        skill_mappings = {
            SkillType.SCIENTIFIC_METHOD: [
                "lesson_01_atomic_structure_and_chemical_bonding",
                "lesson_01_cell_structure_and_functions",
                "lesson_02_genetics_and_heredity"
            ],
            SkillType.PROBLEM_SOLVING: [
                "lesson_02_algorithms_and_programming_basics",
                "lesson_01_basic_economics_concepts",
                "lesson_03_chemical_equations_and_reactions"
            ],
            SkillType.DATA_ANALYSIS: [
                "lesson_03_data_and_cybersecurity_fundamentals",
                "lesson_02_supply,_demand,_and_markets",
                "lesson_01_map_skills_and_cartography"
            ],
            SkillType.SYSTEMS_THINKING: [
                "lesson_03_ecology_and_nutrition",
                "lesson_02_weather,_climate,_and_natural_resources",
                "lesson_03_nigerian_economy_and_development"
            ],
            SkillType.COMMUNICATION: [
                "lesson_01_grammar_and_sentence_structure",
                "lesson_02_comprehension_and_vocabulary",
                "lesson_03_writing_skills_and_composition"
            ],
            SkillType.CRITICAL_THINKING: [
                "lesson_01_pre-colonial_nigeria",
                "lesson_02_colonial_period_and_independence",
                "lesson_03_post-independence_nigeria"
            ]
        }
        
        with self.driver.session() as session:
            for skill, lesson_ids in skill_mappings.items():
                # Create skill node
                session.run("""
                    MERGE (s:Skill {name: $skill_name})
                    SET s.type = $skill_type,
                        s.description = $description,
                        s.created_at = datetime()
                """, {
                    "skill_name": skill.value,
                    "skill_type": skill.name,
                    "description": f"Transferable skill: {skill.value.replace('_', ' ').title()}"
                })
                
                # Link lessons to skill
                for lesson_id in lesson_ids:
                    session.run("""
                        MATCH (s:Skill {name: $skill_name})
                        MATCH (l:Lesson)
                        WHERE l.id CONTAINS $lesson_id
                        MERGE (l)-[:DEVELOPS_SKILL]->(s)
                    """, {
                        "skill_name": skill.value,
                        "lesson_id": lesson_id
                    })
                
                print(f"  ✅ {skill.value}: {len(lesson_ids)} lessons")
        
        print(f"\n✅ Created skill connections for {len(skill_mappings)} skills")

    def get_learning_path_recommendations(self, student_id: str) -> List[Dict[str, Any]]:
        """Recommend learning paths based on student interests and progress"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                // Find subjects the student has engaged with
                MATCH (s:Student {id: $student_id})-[:STUDYING]->(l:Lesson)
                WITH s, collect(DISTINCT l.subject) as studied_subjects
                
                // Find learning paths that match those subjects
                MATCH (lp:LearningPath)-[:INCLUDES_LESSON]->(path_lesson:Lesson)
                WHERE path_lesson.subject IN studied_subjects
                
                WITH lp, count(DISTINCT path_lesson) as matching_lessons
                RETURN lp.id as path_id,
                       lp.name as name,
                       lp.description as description,
                       lp.theme as theme,
                       lp.duration_weeks as duration,
                       lp.skills_developed as skills,
                       matching_lessons
                ORDER BY matching_lessons DESC
                LIMIT 5
            """, {"student_id": student_id})
            
            recommendations = []
            for record in result:
                recommendations.append({
                    "path_id": record['path_id'],
                    "name": record['name'],
                    "description": record['description'],
                    "theme": record['theme'],
                    "duration_weeks": record['duration'],
                    "skills_developed": record['skills'],
                    "relevance_score": record['matching_lessons']
                })
            
            return recommendations

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()


def main():
    """Execute cross-subject expansion"""
    print("=" * 60)
    print("Cross-Subject Connections & Learning Paths")
    print("=" * 60)
    
    expander = CrossSubjectExpander()
    
    if not expander.driver:
        print("\n⚠️ Neo4j not available. Start with:")
        print("docker-compose -f docker-compose-neo4j.yaml up -d")
        return
    
    # Create extended connections
    expander.create_extended_connections()
    
    # Create learning paths
    expander.create_learning_paths()
    
    # Create skill connections
    expander.create_skill_connections()
    
    print("\n" + "=" * 60)
    print("✅ Cross-Subject Expansion Complete")
    print(f"   • 15 cross-subject connections")
    print(f"   • 6 thematic learning paths")
    print(f"   • 6 skill-based networks")
    print("=" * 60)
    
    expander.close()


if __name__ == "__main__":
    main()
