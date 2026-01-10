#!/usr/bin/env python3
"""
Phase 4 Generator - Practice Question Generator
Generates actual practice questions with answers and explanations
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

class Phase4Generator:
    """Generate practice questions from specifications"""
    
    def __init__(self, specs_file="phase4_question_specs.json"):
        self.specs_file = specs_file
        self.specs = []
        self.questions = []
        self.load_specifications()
        
        # Question templates by type
        self.templates = self.create_templates()
    
    def load_specifications(self):
        """Load question specifications"""
        print("Loading question specifications...")
        try:
            with open(self.specs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.specs = data.get('specifications', [])
            print(f"OK Loaded {len(self.specs)} specifications\n")
        except FileNotFoundError:
            print(f"Error: {self.specs_file} not found!")
            exit(1)
    
    def create_templates(self) -> Dict[str, Dict]:
        """Create question templates by subject and type"""
        return {
            "Mathematics": {
                "concepts": {
                    "Number Bases": ["binary", "octal", "hexadecimal", "base conversion"],
                    "Indices": ["laws of indices", "fractional indices", "negative indices"],
                    "Logarithms": ["log laws", "common log", "natural log"],
                    "Quadratic Equations": ["factorization", "completing square", "formula method"],
                    "Simultaneous Equations": ["elimination", "substitution", "graphical method"]
                }
            },
            "Physics": {
                "concepts": {
                    "Scalar and Vector Quantities": ["displacement", "velocity", "force", "momentum"],
                    "Motion": ["speed", "acceleration", "equations of motion", "free fall"],
                    "Force": ["Newton's laws", "friction", "tension", "equilibrium"],
                    "Work, Energy and Power": ["kinetic energy", "potential energy", "power calculation"]
                }
            },
            "Chemistry": {
                "concepts": {
                    "Atomic Structure": ["protons", "neutrons", "electrons", "atomic number"],
                    "Chemical Bonding": ["ionic", "covalent", "metallic", "hydrogen bonding"],
                    "Acids, Bases and Salts": ["pH scale", "neutralization", "indicators"]
                }
            },
            "Biology": {
                "concepts": {
                    "Cell Structure and Organization": ["cell membrane", "nucleus", "cytoplasm", "organelles"],
                    "Nutrition": ["photosynthesis", "digestion", "food tests", "balanced diet"],
                    "Transport": ["diffusion", "osmosis", "active transport"]
                }
            }
        }
    
    def generate_multiple_choice(self, spec: Dict) -> Dict:
        """Generate multiple choice question"""
        subject = spec['subject']
        topic = spec['topic']
        difficulty = spec['difficulty']
        
        # Generate question based on subject
        if subject == "Mathematics":
            if "Number Bases" in topic:
                if difficulty == "easy":
                    question = "Convert 1010₂ to base 10"
                    options = ["8", "10", "12", "16"]
                    correct = 1  # Index of correct answer
                    explanation = "1010₂ = (1×2³) + (0×2²) + (1×2¹) + (0×2⁰) = 8 + 0 + 2 + 0 = 10"
                else:
                    question = "What is the value of 2A₁₆ in base 8?"
                    options = ["42₈", "52₈", "62₈", "72₈"]
                    correct = 1
                    explanation = "2A₁₆ = 42₁₀ = 52₈ (2×8 + 2 = 42)"
            else:
                question = f"Which of the following is correct about {topic}?"
                options = ["Option A", "Option B", "Option C", "Option D"]
                correct = 0
                explanation = f"This relates to the fundamental principles of {topic}."
        
        elif subject == "Physics":
            if "Motion" in topic:
                question = "A car accelerates from rest to 20 m/s in 5 seconds. What is its acceleration?"
                options = ["2 m/s²", "4 m/s²", "5 m/s²", "10 m/s²"]
                correct = 1
                explanation = "a = (v - u) / t = (20 - 0) / 5 = 4 m/s²"
            else:
                question = f"What is the SI unit of {topic}?"
                options = ["Newton", "Joule", "Meter", "Kilogram"]
                correct = 0
                explanation = f"The SI unit is fundamental to understanding {topic}."
        
        elif subject == "Chemistry":
            if "Atomic Structure" in topic:
                question = "What is the atomic number of an element?"
                options = ["Number of protons", "Number of neutrons", "Number of electrons", "Mass number"]
                correct = 0
                explanation = "Atomic number is defined as the number of protons in the nucleus."
            else:
                question = f"Which statement about {topic} is true?"
                options = ["Statement A", "Statement B", "Statement C", "Statement D"]
                correct = 0
                explanation = f"This is a key concept in {topic}."
        
        elif subject == "Biology":
            question = f"Which of the following is true about {topic}?"
            options = ["Occurs in all living cells", "Requires energy", "Produces ATP", "None of the above"]
            correct = 0
            explanation = f"This is a fundamental process in {topic}."
        
        else:
            question = f"What is the main concept of {topic}?"
            options = ["Concept A", "Concept B", "Concept C", "Concept D"]
            correct = 0
            explanation = f"This is central to understanding {topic}."
        
        return {
            "id": spec['id'],
            "subject": subject,
            "topic": topic,
            "grade": spec['grade'],
            "question_type": "multiple_choice",
            "difficulty": difficulty,
            "question_text": question,
            "options": options,
            "correct_answer": correct,
            "explanation": explanation,
            "points": spec['points'],
            "estimated_time": spec['estimated_time'],
            "tags": spec['tags']
        }
    
    def generate_true_false(self, spec: Dict) -> Dict:
        """Generate true/false question"""
        subject = spec['subject']
        topic = spec['topic']
        difficulty = spec['difficulty']
        
        # Generate statement
        if subject == "Mathematics":
            statement = f"In {topic}, all operations follow the same rules as in base 10."
            correct = False
            explanation = "Different bases have different operational rules and digit representations."
        elif subject == "Physics":
            statement = f"In {topic}, energy is always conserved in all processes."
            correct = True
            explanation = "The law of conservation of energy states that energy cannot be created or destroyed."
        elif subject == "Chemistry":
            statement = f"All elements in {topic} have the same number of electrons."
            correct = False
            explanation = "Different elements have different numbers of electrons based on their atomic number."
        else:
            statement = f"{topic} is applicable only in theoretical situations."
            correct = False
            explanation = f"{topic} has many practical real-world applications."
        
        return {
            "id": spec['id'],
            "subject": subject,
            "topic": topic,
            "grade": spec['grade'],
            "question_type": "true_false",
            "difficulty": difficulty,
            "statement": statement,
            "correct_answer": correct,
            "explanation": explanation,
            "points": spec['points'],
            "estimated_time": spec['estimated_time'],
            "tags": spec['tags']
        }
    
    def generate_fill_blank(self, spec: Dict) -> Dict:
        """Generate fill-in-the-blank question"""
        subject = spec['subject']
        topic = spec['topic']
        
        if subject == "Mathematics":
            sentence = f"The process of converting a number from one base to another is called ______."
            answer = "base conversion"
        elif subject == "Physics":
            sentence = "The rate of change of velocity is called ______."
            answer = "acceleration"
        elif subject == "Chemistry":
            sentence = "The smallest unit of an element that retains its chemical properties is the ______."
            answer = "atom"
        elif subject == "Biology":
            sentence = "The process by which plants make their own food using sunlight is called ______."
            answer = "photosynthesis"
        else:
            sentence = f"The fundamental concept in {topic} is ______."
            answer = "key principle"
        
        return {
            "id": spec['id'],
            "subject": subject,
            "topic": topic,
            "grade": spec['grade'],
            "question_type": "fill_blank",
            "difficulty": spec['difficulty'],
            "sentence": sentence,
            "correct_answer": answer,
            "alternative_answers": [answer.lower(), answer.upper()],
            "explanation": f"This term is fundamental to understanding {topic}.",
            "points": spec['points'],
            "estimated_time": spec['estimated_time'],
            "tags": spec['tags']
        }
    
    def generate_matching(self, spec: Dict) -> Dict:
        """Generate matching question"""
        subject = spec['subject']
        topic = spec['topic']
        
        if subject == "Mathematics":
            column_a = ["Binary", "Octal", "Decimal", "Hexadecimal"]
            column_b = ["Base 2", "Base 8", "Base 10", "Base 16"]
            correct_pairs = {0: 0, 1: 1, 2: 2, 3: 3}
        elif subject == "Physics":
            column_a = ["Speed", "Velocity", "Acceleration", "Force"]
            column_b = ["Rate of change of velocity", "Distance per unit time", "Mass × acceleration", "Displacement per unit time"]
            correct_pairs = {0: 1, 1: 3, 2: 0, 3: 2}
        elif subject == "Chemistry":
            column_a = ["Proton", "Neutron", "Electron", "Nucleus"]
            column_b = ["Negatively charged", "No charge", "Center of atom", "Positively charged"]
            correct_pairs = {0: 3, 1: 1, 2: 0, 3: 2}
        else:
            column_a = ["Term 1", "Term 2", "Term 3", "Term 4"]
            column_b = ["Definition 1", "Definition 2", "Definition 3", "Definition 4"]
            correct_pairs = {0: 0, 1: 1, 2: 2, 3: 3}
        
        return {
            "id": spec['id'],
            "subject": subject,
            "topic": topic,
            "grade": spec['grade'],
            "question_type": "matching",
            "difficulty": spec['difficulty'],
            "instruction": "Match each term in Column A with its correct definition in Column B",
            "column_a": column_a,
            "column_b": column_b,
            "correct_pairs": correct_pairs,
            "explanation": f"These are fundamental terms and definitions in {topic}.",
            "points": spec['points'],
            "estimated_time": spec['estimated_time'],
            "tags": spec['tags']
        }
    
    def generate_short_answer(self, spec: Dict) -> Dict:
        """Generate short answer question"""
        subject = spec['subject']
        topic = spec['topic']
        difficulty = spec['difficulty']
        
        if subject == "Mathematics":
            question = f"Explain the process of converting a number from binary to decimal. Provide an example."
            sample_answer = "To convert binary to decimal, multiply each digit by powers of 2 from right to left. Example: 101₂ = (1×2²) + (0×2¹) + (1×2⁰) = 4 + 0 + 1 = 5₁₀"
        elif subject == "Physics":
            question = "Define acceleration and state its SI unit. Give an example of uniform acceleration."
            sample_answer = "Acceleration is the rate of change of velocity. SI unit: m/s². Example: A car starting from rest and reaching 20 m/s in 5 seconds has uniform acceleration of 4 m/s²."
        elif subject == "Chemistry":
            question = "Describe the structure of an atom and name its three main subatomic particles."
            sample_answer = "An atom consists of a nucleus (containing protons and neutrons) surrounded by electrons in shells. The three main subatomic particles are protons (positive charge), neutrons (no charge), and electrons (negative charge)."
        elif subject == "Biology":
            question = f"Explain the importance of {topic} in living organisms."
            sample_answer = f"{topic} is crucial for survival as it enables organisms to maintain life processes, grow, and respond to their environment."
        else:
            question = f"Discuss the main principles of {topic}."
            sample_answer = f"The main principles of {topic} include fundamental concepts that govern its application and understanding."
        
        return {
            "id": spec['id'],
            "subject": subject,
            "topic": topic,
            "grade": spec['grade'],
            "question_type": "short_answer",
            "difficulty": difficulty,
            "question_text": question,
            "sample_answer": sample_answer,
            "marking_criteria": [
                "Correct definition/explanation (2 points)",
                "Relevant example provided (2 points)",
                "Clear and coherent expression (1 point)"
            ],
            "points": spec['points'],
            "estimated_time": spec['estimated_time'],
            "tags": spec['tags']
        }
    
    def generate_question(self, spec: Dict) -> Dict:
        """Generate question based on type"""
        q_type = spec['question_type']
        
        if q_type == "multiple_choice":
            return self.generate_multiple_choice(spec)
        elif q_type == "true_false":
            return self.generate_true_false(spec)
        elif q_type == "fill_blank":
            return self.generate_fill_blank(spec)
        elif q_type == "matching":
            return self.generate_matching(spec)
        elif q_type == "short_answer":
            return self.generate_short_answer(spec)
        else:
            return None
    
    def generate_all_questions(self, limit=150):
        """Generate questions from specifications"""
        print("=" * 70)
        print("GENERATING PRACTICE QUESTIONS")
        print("=" * 70)
        print()
        
        # Sample specifications to stay within limit
        selected_specs = self.specs[:limit] if len(self.specs) > limit else self.specs
        
        subject_counts = defaultdict(int)
        type_counts = defaultdict(int)
        
        print(f"Generating {len(selected_specs)} questions...")
        print()
        
        for i, spec in enumerate(selected_specs, 1):
            question = self.generate_question(spec)
            if question:
                self.questions.append(question)
                subject_counts[spec['subject']] += 1
                type_counts[spec['question_type']] += 1
            
            if i % 25 == 0:
                print(f"  Generated {i} questions...")
        
        print(f"\nOK Generated {len(self.questions)} questions")
        print()
        print("=" * 70)
        print()
        
        # Statistics
        print("Generation Statistics:")
        print()
        print("By Question Type:")
        for q_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.questions)) * 100
            print(f"  {q_type:.<30} {count:>3} ({percentage:>5.1f}%)")
        
        print()
        print("By Subject:")
        for subject, count in sorted(subject_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.questions)) * 100
            print(f"  {subject:.<30} {count:>3} ({percentage:>5.1f}%)")
        
        print()
        print("=" * 70)
        print()
    
    def save_questions(self, output_file="generated_assets/questions/phase4_questions.json"):
        """Save generated questions to JSON"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Saving questions to {output_file}...")
        
        data = {
            "metadata": {
                "total_questions": len(self.questions),
                "question_types": len(set(q["question_type"] for q in self.questions)),
                "subjects": len(set(q["subject"] for q in self.questions)),
                "total_points": sum(q["points"] for q in self.questions),
                "total_time_minutes": sum(q["estimated_time"] for q in self.questions) // 60,
                "generated_at": "2026-01-10"
            },
            "questions": self.questions
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        size_kb = output_path.stat().st_size / 1024
        print(f"OK Saved {len(self.questions)} questions")
        print(f"OK File size: {size_kb:.1f} KB")
        print()
    
    def create_manifest(self, output_file="generated_assets/phase4_manifest.json"):
        """Create manifest file for Phase 4 assets"""
        output_path = Path(output_file)
        
        print(f"Creating manifest at {output_file}...")
        
        # Organize questions by subject and topic
        by_subject = defaultdict(lambda: defaultdict(list))
        
        for question in self.questions:
            subject = question['subject']
            topic = question['topic']
            
            by_subject[subject][topic].append({
                "id": question['id'],
                "question_type": question['question_type'],
                "difficulty": question['difficulty'],
                "points": question['points']
            })
        
        manifest = {
            "metadata": {
                "phase": 4,
                "asset_type": "practice_questions",
                "total_questions": len(self.questions),
                "subjects": len(by_subject),
                "generated_at": "2026-01-10"
            },
            "questions_by_subject": dict(by_subject)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        size_kb = output_path.stat().st_size / 1024
        print(f"OK Created manifest")
        print(f"OK File size: {size_kb:.1f} KB")
        print()
    
    def print_sample_questions(self, count=3):
        """Print sample generated questions"""
        print("=" * 70)
        print(f"SAMPLE QUESTIONS (showing {count} of {len(self.questions)})")
        print("=" * 70)
        print()
        
        for i, question in enumerate(self.questions[:count], 1):
            print(f"{i}. {question['question_type'].upper()} - {question['subject']}")
            print(f"   Topic: {question['topic']} | Difficulty: {question['difficulty']}")
            
            if question['question_type'] == 'multiple_choice':
                print(f"   Q: {question['question_text']}")
                for j, option in enumerate(question['options']):
                    marker = "✓" if j == question['correct_answer'] else " "
                    print(f"      {marker} {chr(65+j)}. {option}")
            elif question['question_type'] == 'true_false':
                print(f"   Statement: {question['statement']}")
                print(f"   Answer: {question['correct_answer']}")
            elif question['question_type'] == 'fill_blank':
                print(f"   Sentence: {question['sentence']}")
                print(f"   Answer: {question['correct_answer']}")
            
            print(f"   Explanation: {question['explanation']}")
            print()
        
        print("=" * 70)
        print()
    
    def run_generation(self, limit=150):
        """Run complete question generation"""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 15 + "PHASE 4 QUESTION GENERATOR" + " " * 27 + "║")
        print("╚" + "=" * 68 + "╝")
        print("\n")
        
        # Generate questions
        self.generate_all_questions(limit=limit)
        
        # Show samples
        self.print_sample_questions(count=5)
        
        # Save questions
        self.save_questions()
        
        # Create manifest
        self.create_manifest()
        
        print("=" * 70)
        print("✅ GENERATION COMPLETE")
        print("=" * 70)
        print()
        print(f"Generated: {len(self.questions)} practice questions")
        print(f"Location: generated_assets/questions/phase4_questions.json")
        print(f"Manifest: generated_assets/phase4_manifest.json")
        print()
        print("Next steps:")
        print("  1. Review generated questions")
        print("  2. Build Phase4AssetLoader backend integration")
        print("  3. Create React components for question display")
        print("=" * 70)
        print()


if __name__ == "__main__":
    generator = Phase4Generator()
    generator.run_generation(limit=150)
