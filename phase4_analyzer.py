#!/usr/bin/env python3
"""
Phase 4 Analyzer - Practice Question Opportunity Detection
Analyzes curriculum content to identify opportunities for practice questions
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

class Phase4Analyzer:
    """Analyze lessons and generate practice question specifications"""
    
    def __init__(self, curriculum_file="curriculum_map.json"):
        self.curriculum_file = curriculum_file
        self.curriculum = {}
        self.question_specs = []
        self.load_curriculum()
    
    def load_curriculum(self):
        """Load curriculum map"""
        print("Loading curriculum map...")
        try:
            with open(self.curriculum_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract subjects from nested structure
            if "subjects" in data:
                self.curriculum = {}
                for subject_name, subject_data in data["subjects"].items():
                    topics = []
                    if "topics" in subject_data and isinstance(subject_data["topics"], list):
                        topics = [t.get("name", t) if isinstance(t, dict) else t 
                                 for t in subject_data["topics"]]
                    
                    self.curriculum[subject_name] = {
                        "topics": topics[:10],  # Limit to first 10 topics per subject
                        "grade": "SS1"
                    }
                
                print(f"OK Loaded {len(self.curriculum)} subjects\n")
            else:
                print("Warning: Unexpected curriculum format. Using sample data.\n")
                self.create_sample_curriculum()
        except FileNotFoundError:
            print(f"Warning: {self.curriculum_file} not found. Using sample data.\n")
            self.create_sample_curriculum()
    
    def create_sample_curriculum(self):
        """Create sample curriculum for testing"""
        self.curriculum = {
            "Mathematics": {
                "topics": ["Algebra", "Geometry", "Calculus", "Statistics"],
                "grade": "SS1"
            },
            "Physics": {
                "topics": ["Mechanics", "Electricity", "Waves", "Thermodynamics"],
                "grade": "SS1"
            },
            "Chemistry": {
                "topics": ["Atomic Structure", "Chemical Bonding", "Acids & Bases"],
                "grade": "SS1"
            },
            "Biology": {
                "topics": ["Cell Biology", "Genetics", "Evolution", "Ecology"],
                "grade": "SS1"
            },
            "English": {
                "topics": ["Grammar", "Literature", "Composition", "Comprehension"],
                "grade": "SS1"
            }
        }
    
    def identify_question_types(self, subject: str, topic: str) -> List[str]:
        """Determine which question types are suitable for a topic"""
        question_types = []
        
        # STEM subjects: all question types work
        if subject in ["Mathematics", "Physics", "Chemistry", "Biology"]:
            question_types = ["multiple_choice", "true_false", "fill_blank", "short_answer"]
            
            # Math gets matching for equations
            if subject == "Mathematics":
                question_types.append("matching")
        
        # Languages: focus on comprehension and grammar
        elif subject in ["English", "Literature"]:
            question_types = ["multiple_choice", "fill_blank", "short_answer"]
        
        # Social sciences: definitions and concepts
        elif subject in ["Economics", "Geography", "Government"]:
            question_types = ["multiple_choice", "true_false", "matching", "short_answer"]
        
        # Default
        else:
            question_types = ["multiple_choice", "true_false"]
        
        return question_types
    
    def generate_question_specs(self):
        """Generate specifications for practice questions"""
        print("=" * 70)
        print("GENERATING QUESTION SPECIFICATIONS")
        print("=" * 70)
        print()
        
        spec_count = 0
        subject_counts = defaultdict(int)
        type_counts = defaultdict(int)
        
        for subject, details in self.curriculum.items():
            topics = details.get('topics', [])
            grade = details.get('grade', 'SS1')
            
            print(f"📚 {subject} ({len(topics)} topics)")
            
            for topic in topics:
                # Determine question types for this topic
                question_types = self.identify_question_types(subject, topic)
                
                # Generate 2-3 questions per topic per type
                questions_per_type = 2 if len(topics) > 5 else 3
                
                for q_type in question_types:
                    for i in range(questions_per_type):
                        spec = {
                            "id": f"{subject.lower().replace(' ', '_')}_{topic.lower().replace(' ', '_')}_{q_type}_{i+1}",
                            "subject": subject,
                            "topic": topic,
                            "grade": grade,
                            "question_type": q_type,
                            "difficulty": self.assign_difficulty(subject, topic, i),
                            "tags": [subject.lower(), topic.lower(), q_type],
                            "estimated_time": self.estimate_time(q_type),
                            "points": self.assign_points(q_type)
                        }
                        
                        self.question_specs.append(spec)
                        spec_count += 1
                        subject_counts[subject] += 1
                        type_counts[q_type] += 1
            
            print(f"   ✓ Generated {subject_counts[subject]} question specs")
        
        print()
        print("=" * 70)
        print(f"TOTAL SPECIFICATIONS: {spec_count}")
        print("=" * 70)
        print()
        
        if spec_count == 0:
            print("Warning: No specifications generated. Check curriculum data.")
            return
        
        # Summary by type
        print("Question Types Distribution:")
        for q_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / spec_count) * 100
            print(f"  {q_type:.<30} {count:>3} ({percentage:>5.1f}%)")
        
        print()
        print("Subject Distribution:")
        for subject, count in sorted(subject_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / spec_count) * 100
            print(f"  {subject:.<30} {count:>3} ({percentage:>5.1f}%)")
        
        print()
        print("=" * 70)
        print()
    
    def assign_difficulty(self, subject: str, topic: str, question_index: int) -> str:
        """Assign difficulty level based on subject and question index"""
        # First question is easier, subsequent ones harder
        if question_index == 0:
            return "easy"
        elif question_index == 1:
            return "medium"
        else:
            return "hard"
    
    def estimate_time(self, question_type: str) -> int:
        """Estimate time in seconds to answer question"""
        time_map = {
            "multiple_choice": 45,
            "true_false": 30,
            "fill_blank": 60,
            "matching": 90,
            "short_answer": 120
        }
        return time_map.get(question_type, 60)
    
    def assign_points(self, question_type: str) -> int:
        """Assign points based on question type"""
        points_map = {
            "multiple_choice": 1,
            "true_false": 1,
            "fill_blank": 2,
            "matching": 3,
            "short_answer": 5
        }
        return points_map.get(question_type, 1)
    
    def save_specifications(self, output_file="phase4_question_specs.json"):
        """Save question specifications to JSON file"""
        print(f"Saving specifications to {output_file}...")
        
        data = {
            "metadata": {
                "total_questions": len(self.question_specs),
                "subjects": len(self.curriculum),
                "question_types": len(set(spec["question_type"] for spec in self.question_specs)),
                "generated_at": "2026-01-10"
            },
            "specifications": self.question_specs
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(self.question_specs)} specifications")
        print(f"✓ File size: {Path(output_file).stat().st_size / 1024:.1f} KB")
        print()
    
    def print_sample_specs(self, count=5):
        """Print sample specifications"""
        print("=" * 70)
        print(f"SAMPLE SPECIFICATIONS (showing {count} of {len(self.question_specs)})")
        print("=" * 70)
        print()
        
        for i, spec in enumerate(self.question_specs[:count], 1):
            print(f"{i}. {spec['id']}")
            print(f"   Subject: {spec['subject']} | Topic: {spec['topic']}")
            print(f"   Type: {spec['question_type']} | Difficulty: {spec['difficulty']}")
            print(f"   Time: {spec['estimated_time']}s | Points: {spec['points']}")
            print()
        
        print("=" * 70)
        print()
    
    def generate_statistics(self):
        """Generate detailed statistics"""
        print("=" * 70)
        print("DETAILED STATISTICS")
        print("=" * 70)
        print()
        
        # By difficulty
        difficulty_counts = defaultdict(int)
        for spec in self.question_specs:
            difficulty_counts[spec['difficulty']] += 1
        
        print("Difficulty Distribution:")
        for difficulty in ['easy', 'medium', 'hard']:
            count = difficulty_counts[difficulty]
            percentage = (count / len(self.question_specs)) * 100
            print(f"  {difficulty.capitalize():.<30} {count:>3} ({percentage:>5.1f}%)")
        
        # Total time and points
        total_time = sum(spec['estimated_time'] for spec in self.question_specs)
        total_points = sum(spec['points'] for spec in self.question_specs)
        
        print()
        print("Question Bank Metrics:")
        print(f"  Total Questions: {len(self.question_specs)}")
        print(f"  Total Time: {total_time // 60} minutes ({total_time // 3600:.1f} hours)")
        print(f"  Total Points: {total_points}")
        print(f"  Average Points per Question: {total_points / len(self.question_specs):.1f}")
        
        print()
        print("=" * 70)
        print()
    
    def run_analysis(self):
        """Run complete analysis"""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 15 + "PHASE 4 QUESTION ANALYZER" + " " * 28 + "║")
        print("╚" + "=" * 68 + "╝")
        print("\n")
        
        # Generate specifications
        self.generate_question_specs()
        
        # Show statistics
        self.generate_statistics()
        
        # Show samples
        self.print_sample_specs(count=10)
        
        # Save to file
        self.save_specifications()
        
        print("=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Review phase4_question_specs.json")
        print("  2. Run phase4_generator.py to create actual questions")
        print("  3. Integrate with backend API")
        print("=" * 70)
        print()


if __name__ == "__main__":
    analyzer = Phase4Analyzer()
    analyzer.run_analysis()
