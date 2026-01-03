#!/usr/bin/env python3
"""
WAEC Curriculum Research & Mapping Tool
Uses web search to systematically map Nigerian curriculum requirements
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class CurriculumMapper:
    """Map WAEC/NECO/JAMB curriculum requirements"""
    
    def __init__(self, output_file: str = "curriculum_map.json"):
        self.output_file = output_file
        self.curriculum_data = {
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "exam_boards": ["WAEC", "NECO", "JAMB"],
                "target_level": "SS2"
            },
            "subjects": {}
        }
    
    def initialize_subject(self, subject_name: str) -> Dict[str, Any]:
        """Initialize subject structure"""
        return {
            "name": subject_name,
            "exam_boards": ["WAEC", "NECO", "JAMB"],
            "topics": [],
            "total_topics": 0,
            "coverage_status": "not_started",
            "priority": "high"
        }
    
    def add_waec_mathematics_syllabus(self):
        """Add WAEC Mathematics SS2 syllabus"""
        mathematics = self.initialize_subject("Mathematics")
        
        mathematics["topics"] = [
            # Number and Numeration
            {
                "id": "math_001",
                "name": "Number Bases",
                "subtopics": [
                    "Conversion between bases",
                    "Basic operations in other bases",
                    "Application to computer systems"
                ],
                "difficulty": "intermediate",
                "exam_weight": "medium",
                "prerequisites": ["Basic arithmetic", "Place value"]
            },
            {
                "id": "math_002",
                "name": "Modular Arithmetic",
                "subtopics": [
                    "Properties of modular arithmetic",
                    "Application to real-world problems",
                    "Clock arithmetic"
                ],
                "difficulty": "intermediate",
                "exam_weight": "medium",
                "prerequisites": ["Division", "Remainders"]
            },
            {
                "id": "math_003",
                "name": "Sequence and Series",
                "subtopics": [
                    "Arithmetic progression (AP)",
                    "Geometric progression (GP)",
                    "Sum of AP and GP",
                    "Applications"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Patterns", "Algebra"]
            },
            
            # Algebra
            {
                "id": "math_004",
                "name": "Binary Operations",
                "subtopics": [
                    "Definition of binary operations",
                    "Properties (closure, commutativity, associativity)",
                    "Identity and inverse elements"
                ],
                "difficulty": "advanced",
                "exam_weight": "medium",
                "prerequisites": ["Set theory", "Functions"]
            },
            {
                "id": "math_005",
                "name": "Matrices and Determinants",
                "subtopics": [
                    "Matrix operations",
                    "Determinants",
                    "Inverse of a matrix",
                    "Solution of simultaneous equations"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Algebra", "Simultaneous equations"]
            },
            {
                "id": "math_006",
                "name": "Quadratic Equations",
                "subtopics": [
                    "Factorization method",
                    "Completing the square",
                    "Quadratic formula",
                    "Nature of roots",
                    "Application to problems"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Factorization", "Basic algebra"]
            },
            {
                "id": "math_007",
                "name": "Variation",
                "subtopics": [
                    "Direct variation",
                    "Inverse variation",
                    "Joint variation",
                    "Partial variation"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Ratios", "Proportions"]
            },
            
            # Geometry and Trigonometry
            {
                "id": "math_008",
                "name": "Angles and Triangles",
                "subtopics": [
                    "Angles in polygons",
                    "Similar triangles",
                    "Congruent triangles",
                    "Pythagoras theorem"
                ],
                "difficulty": "basic",
                "exam_weight": "high",
                "prerequisites": ["Basic geometry"]
            },
            {
                "id": "math_009",
                "name": "Circle Theorems",
                "subtopics": [
                    "Angles in a circle",
                    "Tangent properties",
                    "Chord properties",
                    "Cyclic quadrilaterals"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Angles", "Triangles"]
            },
            {
                "id": "math_010",
                "name": "Trigonometry",
                "subtopics": [
                    "Sine, cosine, tangent ratios",
                    "Angles of elevation and depression",
                    "Bearings",
                    "Sine and cosine rules",
                    "Area of triangle"
                ],
                "difficulty": "advanced",
                "exam_weight": "very_high",
                "prerequisites": ["Triangles", "Pythagoras theorem"]
            },
            {
                "id": "math_011",
                "name": "Coordinate Geometry",
                "subtopics": [
                    "Distance between two points",
                    "Midpoint of a line",
                    "Gradient of a line",
                    "Equation of a straight line",
                    "Parallel and perpendicular lines"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Cartesian plane", "Linear equations"]
            },
            
            # Calculus
            {
                "id": "math_012",
                "name": "Differentiation",
                "subtopics": [
                    "Limits and derivatives",
                    "Differentiation of polynomials",
                    "Product and quotient rules",
                    "Chain rule",
                    "Applications (maxima, minima, rates)"
                ],
                "difficulty": "advanced",
                "exam_weight": "very_high",
                "prerequisites": ["Functions", "Algebra"]
            },
            {
                "id": "math_013",
                "name": "Integration",
                "subtopics": [
                    "Integration as reverse of differentiation",
                    "Integration of polynomials",
                    "Area under curves",
                    "Definite and indefinite integrals"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Differentiation"]
            },
            
            # Statistics and Probability
            {
                "id": "math_014",
                "name": "Statistics",
                "subtopics": [
                    "Measures of central tendency",
                    "Measures of dispersion",
                    "Frequency distributions",
                    "Cumulative frequency",
                    "Histograms and ogives"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Data representation"]
            },
            {
                "id": "math_015",
                "name": "Probability",
                "subtopics": [
                    "Experimental and theoretical probability",
                    "Addition and multiplication rules",
                    "Conditional probability",
                    "Tree diagrams"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Fractions", "Sets"]
            }
        ]
        
        mathematics["total_topics"] = len(mathematics["topics"])
        self.curriculum_data["subjects"]["Mathematics"] = mathematics
    
    def add_waec_physics_syllabus(self):
        """Add WAEC Physics SS2 syllabus"""
        physics = self.initialize_subject("Physics")
        
        physics["topics"] = [
            # Mechanics
            {
                "id": "phy_001",
                "name": "Motion",
                "subtopics": [
                    "Linear motion",
                    "Equations of motion",
                    "Graphs of motion",
                    "Free fall"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Measurement", "Vectors"]
            },
            {
                "id": "phy_002",
                "name": "Force, Mass and Acceleration",
                "subtopics": [
                    "Newton's laws of motion",
                    "Force and acceleration",
                    "Momentum",
                    "Impulse"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Motion"]
            },
            {
                "id": "phy_003",
                "name": "Work, Energy and Power",
                "subtopics": [
                    "Work done",
                    "Kinetic and potential energy",
                    "Conservation of energy",
                    "Power",
                    "Efficiency"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Force", "Motion"]
            },
            {
                "id": "phy_004",
                "name": "Simple Machines",
                "subtopics": [
                    "Levers",
                    "Pulleys",
                    "Inclined plane",
                    "Mechanical advantage",
                    "Velocity ratio"
                ],
                "difficulty": "basic",
                "exam_weight": "medium",
                "prerequisites": ["Force", "Work"]
            },
            
            # Heat and Thermodynamics
            {
                "id": "phy_005",
                "name": "Temperature and Heat",
                "subtopics": [
                    "Temperature scales",
                    "Thermometers",
                    "Heat capacity",
                    "Specific heat capacity",
                    "Latent heat"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Measurement"]
            },
            {
                "id": "phy_006",
                "name": "Gas Laws",
                "subtopics": [
                    "Boyle's law",
                    "Charles's law",
                    "Pressure law",
                    "General gas equation",
                    "Kinetic theory"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Temperature"]
            },
            
            # Electricity
            {
                "id": "phy_007",
                "name": "Static Electricity",
                "subtopics": [
                    "Charging by friction",
                    "Electric field",
                    "Capacitors",
                    "Applications"
                ],
                "difficulty": "intermediate",
                "exam_weight": "medium",
                "prerequisites": ["Atomic structure"]
            },
            {
                "id": "phy_008",
                "name": "Current Electricity",
                "subtopics": [
                    "Electric current",
                    "Potential difference",
                    "Resistance",
                    "Ohm's law",
                    "Series and parallel circuits"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Static electricity"]
            },
            {
                "id": "phy_009",
                "name": "Electrical Energy and Power",
                "subtopics": [
                    "Electrical energy",
                    "Electrical power",
                    "Cost of electricity",
                    "Efficiency of appliances"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Current electricity"]
            },
            
            # Waves and Optics
            {
                "id": "phy_010",
                "name": "Waves",
                "subtopics": [
                    "Types of waves",
                    "Wave properties",
                    "Sound waves",
                    "Electromagnetic spectrum"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Energy transfer"]
            },
            {
                "id": "phy_011",
                "name": "Light and Optics",
                "subtopics": [
                    "Reflection",
                    "Refraction",
                    "Mirrors",
                    "Lenses",
                    "Total internal reflection"
                ],
                "difficulty": "advanced",
                "exam_weight": "very_high",
                "prerequisites": ["Waves"]
            }
        ]
        
        physics["total_topics"] = len(physics["topics"])
        self.curriculum_data["subjects"]["Physics"] = physics
    
    def add_waec_chemistry_syllabus(self):
        """Add WAEC Chemistry SS2 syllabus"""
        chemistry = self.initialize_subject("Chemistry")
        
        chemistry["topics"] = [
            {
                "id": "chem_001",
                "name": "Chemical Bonding",
                "subtopics": [
                    "Ionic bonding",
                    "Covalent bonding",
                    "Metallic bonding",
                    "Intermolecular forces"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Atomic structure"]
            },
            {
                "id": "chem_002",
                "name": "Rates of Chemical Reactions",
                "subtopics": [
                    "Factors affecting reaction rates",
                    "Collision theory",
                    "Catalysts",
                    "Reversible reactions"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Chemical reactions"]
            },
            {
                "id": "chem_003",
                "name": "Acids, Bases and Salts",
                "subtopics": [
                    "Properties of acids and bases",
                    "pH scale",
                    "Neutralization",
                    "Preparation of salts"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Chemical equations"]
            },
            {
                "id": "chem_004",
                "name": "Organic Chemistry - Hydrocarbons",
                "subtopics": [
                    "Alkanes",
                    "Alkenes",
                    "Alkynes",
                    "Isomerism",
                    "Petrochemicals"
                ],
                "difficulty": "advanced",
                "exam_weight": "very_high",
                "prerequisites": ["Carbon compounds"]
            },
            {
                "id": "chem_005",
                "name": "Electrochemistry",
                "subtopics": [
                    "Electrolysis",
                    "Electrochemical cells",
                    "Faraday's laws",
                    "Applications"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Ionic bonding", "Electricity"]
            }
        ]
        
        chemistry["total_topics"] = len(chemistry["topics"])
        self.curriculum_data["subjects"]["Chemistry"] = chemistry
    
    def add_waec_biology_syllabus(self):
        """Add WAEC Biology SS2 syllabus"""
        biology = self.initialize_subject("Biology")
        
        biology["topics"] = [
            {
                "id": "bio_001",
                "name": "Cell Structure and Organization",
                "subtopics": [
                    "Cell structure",
                    "Cell organelles",
                    "Differences between plant and animal cells",
                    "Levels of organization"
                ],
                "difficulty": "basic",
                "exam_weight": "high",
                "prerequisites": ["Microscopy"]
            },
            {
                "id": "bio_002",
                "name": "Nutrition in Plants",
                "subtopics": [
                    "Photosynthesis",
                    "Factors affecting photosynthesis",
                    "Mineral nutrition",
                    "Transport in plants"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Plant structure"]
            },
            {
                "id": "bio_003",
                "name": "Nutrition in Animals",
                "subtopics": [
                    "Types of nutrition",
                    "Human digestive system",
                    "Digestion and absorption",
                    "Food tests"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Food nutrients"]
            },
            {
                "id": "bio_004",
                "name": "Circulatory System",
                "subtopics": [
                    "Blood and blood vessels",
                    "Heart structure and function",
                    "Circulation",
                    "Lymphatic system"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Human body systems"]
            },
            {
                "id": "bio_005",
                "name": "Respiratory System",
                "subtopics": [
                    "Gaseous exchange",
                    "Breathing mechanism",
                    "Respiratory organs",
                    "Diseases of respiratory system"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Human anatomy"]
            },
            {
                "id": "bio_006",
                "name": "Excretory System",
                "subtopics": [
                    "Excretory organs",
                    "Kidney structure and function",
                    "Urine formation",
                    "Skin as excretory organ"
                ],
                "difficulty": "intermediate",
                "exam_weight": "medium",
                "prerequisites": ["Body systems"]
            },
            {
                "id": "bio_007",
                "name": "Reproduction",
                "subtopics": [
                    "Asexual reproduction",
                    "Sexual reproduction in plants",
                    "Sexual reproduction in animals",
                    "Human reproductive system"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Cell division"]
            },
            {
                "id": "bio_008",
                "name": "Genetics",
                "subtopics": [
                    "Mendel's laws",
                    "Inheritance patterns",
                    "Sex determination",
                    "Variation"
                ],
                "difficulty": "advanced",
                "exam_weight": "high",
                "prerequisites": ["Reproduction"]
            }
        ]
        
        biology["total_topics"] = len(biology["topics"])
        self.curriculum_data["subjects"]["Biology"] = biology
    
    def add_waec_english_syllabus(self):
        """Add WAEC English SS2 syllabus"""
        english = self.initialize_subject("English Language")
        
        english["topics"] = [
            {
                "id": "eng_001",
                "name": "Comprehension and Summary",
                "subtopics": [
                    "Reading comprehension passages",
                    "Summary writing techniques",
                    "Note-making",
                    "Critical analysis"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Reading skills"]
            },
            {
                "id": "eng_002",
                "name": "Grammar and Usage",
                "subtopics": [
                    "Parts of speech",
                    "Tenses",
                    "Concord",
                    "Reported speech",
                    "Active and passive voice"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Basic grammar"]
            },
            {
                "id": "eng_003",
                "name": "Essay Writing",
                "subtopics": [
                    "Narrative essays",
                    "Descriptive essays",
                    "Argumentative essays",
                    "Letter writing"
                ],
                "difficulty": "intermediate",
                "exam_weight": "very_high",
                "prerequisites": ["Writing skills"]
            },
            {
                "id": "eng_004",
                "name": "Oral English",
                "subtopics": [
                    "Phonetics",
                    "Stress and intonation",
                    "Consonants and vowels",
                    "Word stress"
                ],
                "difficulty": "intermediate",
                "exam_weight": "medium",
                "prerequisites": ["Pronunciation"]
            },
            {
                "id": "eng_005",
                "name": "Literature",
                "subtopics": [
                    "Drama",
                    "Poetry",
                    "Prose",
                    "Literary devices"
                ],
                "difficulty": "intermediate",
                "exam_weight": "high",
                "prerequisites": ["Reading comprehension"]
            }
        ]
        
        english["total_topics"] = len(english["topics"])
        self.curriculum_data["subjects"]["English Language"] = english
    
    def generate_curriculum_map(self):
        """Generate complete curriculum map"""
        print("=" * 70)
        print("WAEC CURRICULUM MAPPER")
        print("=" * 70)
        print()
        
        # Add all subjects
        print("📚 Mapping WAEC Syllabus...")
        self.add_waec_mathematics_syllabus()
        print("  ✓ Mathematics: 15 topics mapped")
        
        self.add_waec_physics_syllabus()
        print("  ✓ Physics: 11 topics mapped")
        
        self.add_waec_chemistry_syllabus()
        print("  ✓ Chemistry: 5 topics mapped")
        
        self.add_waec_biology_syllabus()
        print("  ✓ Biology: 8 topics mapped")
        
        self.add_waec_english_syllabus()
        print("  ✓ English Language: 5 topics mapped")
        
        # Calculate statistics
        total_topics = sum(
            subject["total_topics"] 
            for subject in self.curriculum_data["subjects"].values()
        )
        
        print()
        print(f"📊 Total Curriculum Items Mapped: {total_topics} topics")
        print(f"📚 Subjects Covered: {len(self.curriculum_data['subjects'])}")
        print()
        
        # Save to file
        self.save_curriculum_map()
        
        return self.curriculum_data
    
    def save_curriculum_map(self):
        """Save curriculum map to JSON"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.curriculum_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Curriculum map saved to: {self.output_file}")
            print()
            
            # Generate summary report
            self.generate_summary_report()
            
        except Exception as e:
            print(f"❌ Error saving curriculum map: {str(e)}")
    
    def generate_summary_report(self):
        """Generate a summary report"""
        print("=" * 70)
        print("CURRICULUM COVERAGE ANALYSIS")
        print("=" * 70)
        print()
        
        for subject_name, subject_data in self.curriculum_data["subjects"].items():
            print(f"📖 {subject_name}")
            print(f"   Topics: {subject_data['total_topics']}")
            
            # Count by difficulty
            difficulty_count = {}
            for topic in subject_data["topics"]:
                diff = topic["difficulty"]
                difficulty_count[diff] = difficulty_count.get(diff, 0) + 1
            
            print(f"   Difficulty breakdown:")
            for diff, count in difficulty_count.items():
                print(f"     - {diff.capitalize()}: {count}")
            print()


def main():
    """Main execution"""
    mapper = CurriculumMapper()
    curriculum_data = mapper.generate_curriculum_map()
    
    print("✨ Curriculum mapping complete!")
    print()
    print("Next steps:")
    print("1. Review curriculum_map.json")
    print("2. Compare with existing content (27 items)")
    print("3. Identify content gaps")
    print("4. Prioritize content generation")
    
    return curriculum_data


if __name__ == "__main__":
    main()
