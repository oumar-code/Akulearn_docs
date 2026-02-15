#!/usr/bin/env python3
"""
Content Generation Script for Akudemy JAMB Preparation
Generates study guides, questions, and mock exams from templates

Usage:
    python content_generator.py --subject Chemistry --topic "Organic Chemistry" --type guide
    python content_generator.py --subject Biology --type mock --count 3
    python content_generator.py --type bulk --subjects all
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import random

# ============================================================================
# 1. CONFIGURATION
# ============================================================================

class ContentConfig:
    """Configuration for content generation"""
    
    SUBJECTS = {
        "Chemistry": {
            "topics": [
                "Organic Chemistry - Nomenclature",
                "Atomic Structure",
                "Bonding & Structure",
                "Stoichiometry",
                "Equilibrium",
                "Electrochemistry"
            ],
            "questionsPerTopic": 50,
            "videoMinutes": 5
        },
        "Biology": {
            "topics": [
                "Cell Structure",
                "Photosynthesis",
                "Respiration",
                "Genetics",
                "Ecology",
                "Human Systems"
            ],
            "questionsPerTopic": 40,
            "videoMinutes": 5
        },
        "English": {
            "topics": [
                "Comprehension",
                "Vocabulary",
                "Grammar",
                "Essay Writing",
                "Oral English"
            ],
            "questionsPerTopic": 30,
            "videoMinutes": 3
        },
        "Mathematics": {
            "topics": [
                "Algebra",
                "Geometry",
                "Trigonometry",
                "Statistics",
                "Calculus"
            ],
            "questionsPerTopic": 45,
            "videoMinutes": 6
        }
    }
    
    DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
    EXAM_BOARDS = ["JAMB", "WAEC", "NECO"]
    OUTPUT_DIR = "generated_content"


# ============================================================================
# 2. STUDY GUIDE GENERATOR
# ============================================================================

class StudyGuideGenerator:
    """Generate study guides for topics"""
    
    def __init__(self, subject: str, topic: str):
        self.subject = subject
        self.topic = topic
        self.created_at = datetime.now().isoformat()
    
    def generate_guide_metadata(self) -> Dict:
        """Generate metadata for study guide"""
        return {
            "subject": self.subject,
            "topic": self.topic,
            "difficulty": "intermediate",
            "estimatedReadTime": 15,
            "videoLinkMinutes": ContentConfig.SUBJECTS[self.subject]["videoMinutes"],
            "targetExamBoards": ContentConfig.EXAM_BOARDS,
            "lastUpdated": self.created_at,
            "contentStatus": "Ready for expert review"
        }
    
    def generate_key_concepts(self, count: int = 3) -> List[Dict]:
        """Generate key concepts for topic"""
        concepts = []
        for i in range(count):
            concept = {
                "conceptNumber": i + 1,
                "title": f"Key Concept {i + 1}: {self.topic} (To be filled by expert)",
                "explanation": f"Detailed explanation of {self.topic} component {i + 1}",
                "examples": [
                    f"Example 1: Demonstration of concept",
                    f"Example 2: Real-world application"
                ],
                "memorize": f"Key takeaway for this concept"
            }
            concepts.append(concept)
        return concepts
    
    def generate_study_guide(self) -> Dict:
        """Generate complete study guide"""
        return {
            "studyGuide": {
                "metadata": self.generate_guide_metadata(),
                "title": f"{self.subject}: {self.topic}",
                "objective": f"Master {self.topic} for JAMB/WAEC/NECO exams",
                
                "keyConceptsSection": {
                    "title": "3 Key Concepts",
                    "concepts": self.generate_key_concepts(3)
                },
                
                "practiceQuestionsSection": {
                    "title": "5 Practice Questions",
                    "instructions": "Attempt before reviewing answers",
                    "questions": []  # Will be filled by question generator
                },
                
                "examTipsSection": {
                    "title": "How to Ace JAMB Questions",
                    "tips": [
                        {
                            "tip": 1,
                            "strategy": "Understand the concept deeply",
                            "action": "Review key concepts 2-3 times"
                        },
                        {
                            "tip": 2,
                            "strategy": "Practice similar questions",
                            "action": "Do 50+ questions on this topic"
                        },
                        {
                            "tip": 3,
                            "strategy": "Learn common mistakes",
                            "action": "Study explanations for wrong answers"
                        }
                    ]
                },
                
                "createdAt": self.created_at,
                "status": "Template - Ready for expert content"
            }
        }


# ============================================================================
# 3. QUESTION GENERATOR
# ============================================================================

class QuestionGenerator:
    """Generate multiple-choice questions for topics"""
    
    def __init__(self, subject: str, topic: str, difficulty: str = "medium"):
        self.subject = subject
        self.topic = topic
        self.difficulty = difficulty
        self.question_count = 0
    
    def generate_question(self, question_number: int) -> Dict:
        """Generate a single question"""
        difficulty_percentages = {
            "easy": {"reasoning": "70%", "calculation": "30%"},
            "medium": {"reasoning": "50%", "calculation": "50%"},
            "hard": {"reasoning": "30%", "calculation": "70%"}
        }
        
        question = {
            "id": f"{self.subject.lower()}_{self.topic.lower().replace(' ', '_')}_{question_number:03d}",
            "number": question_number,
            "difficulty": self.difficulty,
            "subject": self.subject,
            "topic": self.topic,
            "question_text": f"[Question {question_number} on {self.topic} - To be filled by expert]",
            
            "options": [
                {"label": "A", "text": "Option A - To be filled"},
                {"label": "B", "text": "Option B - To be filled"},
                {"label": "C", "text": "Option C - To be filled"},
                {"label": "D", "text": "Option D - To be filled"}
            ],
            
            "correctAnswer": random.choice(["A", "B", "C", "D"]),
            "explanation": f"Why the correct answer is right - {self.difficulty} level explanation",
            "keyLearning": f"Key concept tested: {self.topic}",
            "sourceExam": random.choice(["JAMB 2024", "JAMB 2023", "Practice", "Generated"]),
            
            "createdAt": datetime.now().isoformat(),
            "reviewStatus": "Template - Needs expert validation"
        }
        return question
    
    def generate_questions_batch(self, count: int) -> List[Dict]:
        """Generate multiple questions"""
        questions = []
        for i in range(1, count + 1):
            questions.append(self.generate_question(i))
        return questions


# ============================================================================
# 4. MOCK EXAM GENERATOR
# ============================================================================

class MockExamGenerator:
    """Generate mock exams"""
    
    STANDARD_STRUCTURE = {
        "English": {"questions": 40, "time_minutes": 60},
        "Mathematics": {"questions": 40, "time_minutes": 60},
        "Science1": {"questions": 50, "time_minutes": 30},  # Chemistry
        "Science2": {"questions": 50, "time_minutes": 30}   # Biology
    }
    
    def __init__(self, mock_number: int):
        self.mock_number = mock_number
        self.created_at = datetime.now().isoformat()
    
    def generate_mock_structure(self) -> Dict:
        """Generate mock exam structure"""
        return {
            "mockExam": {
                "id": f"full_mock_{self.mock_number:03d}",
                "name": f"Full Mock Exam #{self.mock_number}",
                "duration": 180,
                "durationUnit": "minutes",
                "totalQuestions": 180,
                
                "sections": [
                    {
                        "sectionNumber": 1,
                        "subject": "English Language",
                        "questionCount": 40,
                        "timeAllocationMinutes": 60,
                        "avgTimePerQuestion": 1.5,
                        "questionsGenerated": 0,
                        "status": "Template - Needs 40 questions"
                    },
                    {
                        "sectionNumber": 2,
                        "subject": "Mathematics",
                        "questionCount": 40,
                        "timeAllocationMinutes": 60,
                        "avgTimePerQuestion": 1.5,
                        "questionsGenerated": 0,
                        "status": "Template - Needs 40 questions"
                    },
                    {
                        "sectionNumber": 3,
                        "subject": "Chemistry",
                        "questionCount": 50,
                        "timeAllocationMinutes": 30,
                        "avgTimePerQuestion": 0.6,
                        "questionsGenerated": 0,
                        "status": "Template - Needs 50 questions"
                    },
                    {
                        "sectionNumber": 4,
                        "subject": "Biology",
                        "questionCount": 50,
                        "timeAllocationMinutes": 30,
                        "avgTimePerQuestion": 0.6,
                        "questionsGenerated": 0,
                        "status": "Template - Needs 50 questions"
                    }
                ],
                
                "createdAt": self.created_at,
                "status": "Template - Ready for question population"
            }
        }
    
    def generate_quick_mock(self, subject: str, question_count: int = 20) -> Dict:
        """Generate quick mock for single subject"""
        return {
            "quickMock": {
                "id": f"quick_mock_{subject.lower()}_{datetime.now().strftime('%Y%m%d')}",
                "name": f"Quick {subject} Mock",
                "duration": 30,
                "totalQuestions": question_count,
                "subject": subject,
                "purpose": "Daily skill-building",
                "questionsGenerated": 0,
                "createdAt": self.created_at,
                "status": f"Template - Needs {question_count} questions"
            }
        }


# ============================================================================
# 5. BULK CONTENT GENERATOR
# ============================================================================

class BulkContentGenerator:
    """Generate content in bulk"""
    
    def __init__(self, output_dir: str = ContentConfig.OUTPUT_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.generation_log = []
    
    def generate_all_study_guides(self) -> Dict[str, int]:
        """Generate study guides for all subjects and topics"""
        stats = {}
        
        for subject, config in ContentConfig.SUBJECTS.items():
            stats[subject] = {"guides": 0, "questions": 0}
            
            for topic in config["topics"]:
                # Generate guide
                guide_gen = StudyGuideGenerator(subject, topic)
                guide = guide_gen.generate_study_guide()
                
                # Generate questions for guide
                q_gen = QuestionGenerator(subject, topic, "medium")
                questions = q_gen.generate_questions_batch(5)
                guide["studyGuide"]["practiceQuestionsSection"]["questions"] = questions
                
                # Save guide
                filename = f"{subject.lower()}_{topic.lower().replace(' ', '_')}_guide.json"
                filepath = self.output_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(guide, f, indent=2, ensure_ascii=False)
                
                stats[subject]["guides"] += 1
                stats[subject]["questions"] += len(questions)
                
                self.generation_log.append({
                    "type": "study_guide",
                    "subject": subject,
                    "topic": topic,
                    "status": "generated",
                    "file": str(filepath)
                })
        
        return stats
    
    def generate_question_banks(self, questions_per_topic: int = 50) -> Dict[str, int]:
        """Generate question banks for each subject"""
        stats = {}
        
        for subject, config in ContentConfig.SUBJECTS.items():
            all_questions = []
            
            for topic in config["topics"]:
                for difficulty in ContentConfig.DIFFICULTY_LEVELS:
                    q_count = questions_per_topic // 3  # Divide by 3 difficulty levels
                    
                    q_gen = QuestionGenerator(subject, topic, difficulty)
                    questions = q_gen.generate_questions_batch(q_count)
                    all_questions.extend(questions)
            
            # Save question bank
            filename = f"{subject.lower()}_question_bank.json"
            filepath = self.output_dir / filename
            
            question_bank = {
                "subject": subject,
                "totalQuestions": len(all_questions),
                "generatedAt": datetime.now().isoformat(),
                "questions": all_questions
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(question_bank, f, indent=2, ensure_ascii=False)
            
            stats[subject] = len(all_questions)
            
            self.generation_log.append({
                "type": "question_bank",
                "subject": subject,
                "totalQuestions": len(all_questions),
                "status": "generated",
                "file": str(filepath)
            })
        
        return stats
    
    def generate_mock_exams(self, count: int = 3) -> Dict[str, int]:
        """Generate mock exams"""
        stats = {"mocks_generated": 0, "total_questions": 0}
        
        for i in range(1, count + 1):
            mock_gen = MockExamGenerator(i)
            mock = mock_gen.generate_mock_structure()
            
            # Save mock
            filename = f"mock_exam_{i:03d}.json"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mock, f, indent=2, ensure_ascii=False)
            
            stats["mocks_generated"] += 1
            stats["total_questions"] += mock["mockExam"]["totalQuestions"]
            
            self.generation_log.append({
                "type": "mock_exam",
                "mockNumber": i,
                "totalQuestions": 180,
                "status": "template_generated",
                "file": str(filepath)
            })
        
        return stats
    
    def generate_all(self) -> Dict:
        """Generate all content"""
        print("\n" + "="*60)
        print("🚀 AKUDEMY CONTENT GENERATION")
        print("="*60 + "\n")
        
        print("📚 Generating Study Guides...")
        guide_stats = self.generate_all_study_guides()
        print(f"✅ Generated {sum(s['guides'] for s in guide_stats.values())} study guides")
        print(f"✅ Generated {sum(s['questions'] for s in guide_stats.values())} practice questions\n")
        
        print("🎯 Generating Question Banks...")
        qbank_stats = self.generate_question_banks(50)
        total_questions = sum(qbank_stats.values())
        print(f"✅ Generated {total_questions} total questions\n")
        
        print("📝 Generating Mock Exams...")
        mock_stats = self.generate_mock_exams(3)
        print(f"✅ Generated {mock_stats['mocks_generated']} mock exams")
        print(f"✅ {mock_stats['total_questions']} total questions in mocks\n")
        
        print("="*60)
        print("GENERATION COMPLETE!")
        print("="*60)
        print(f"📁 Output Directory: {self.output_dir.absolute()}")
        print(f"📊 Total Logs: {len(self.generation_log)} entries")
        print("\nGenerated Files:")
        for log in self.generation_log[:5]:
            print(f"  - {log['type']}: {log['subject']}")
        if len(self.generation_log) > 5:
            print(f"  ... and {len(self.generation_log) - 5} more files")
        
        return {
            "guides": guide_stats,
            "questions": qbank_stats,
            "mocks": mock_stats,
            "output_dir": str(self.output_dir),
            "total_logs": len(self.generation_log)
        }


# ============================================================================
# 6. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution"""
    
    # Create bulk generator
    generator = BulkContentGenerator()
    
    # Generate all content
    results = generator.generate_all()
    
    # Print results
    print("\n📊 SUMMARY")
    print(f"Study Guides per subject: {results['guides']}")
    print(f"Question Banks: {results['questions']}")
    print(f"Mock Exams: {results['mocks']}")


if __name__ == "__main__":
    main()
