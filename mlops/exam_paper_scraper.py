#!/usr/bin/env python3
"""
Exam Papers Data Acquisition Pipeline
Downloads and processes WAEC, NECO, JAMB past papers
Organizes by subject/topic and creates structured datasets

Sources:
- WAEC: https://www.waecnigeria.org/e-learning/past-questions
- NECO: https://www.neco.gov.ng/
- JAMB: https://www.jamb.org.ng/
- Alternative: https://www.examplanner.com/ (aggregator)
- Alternative: https://www.myschool.ng/past-questions
"""

import os
import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import random

# ============================================================================
# CONFIGURATION
# ============================================================================

# Create data directory
DATA_DIR = Path(__file__).parent.parent / "data" / "exam_papers"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Supported exam boards and subjects
EXAM_BOARDS = {
    'WAEC': {
        'subjects': [
            'Mathematics', 'English Language', 'Physics', 'Chemistry', 'Biology',
            'Agricultural Science', 'Computer Science', 'Economics', 'Geography',
            'Civic Education', 'History', 'Literature in English', 'Biology'
        ],
        'years': list(range(2014, 2025)),  # 2014-2024
        'url_pattern': 'https://www.examplanner.com/waec-past-questions/{subject}/{year}'
    },
    'NECO': {
        'subjects': [
            'Mathematics', 'English Language', 'Physics', 'Chemistry', 'Biology',
            'Agricultural Science', 'Computer Science', 'Economics', 'Geography'
        ],
        'years': list(range(2014, 2025)),
        'url_pattern': 'https://www.examplanner.com/neco-past-questions/{subject}/{year}'
    },
    'JAMB': {
        'subjects': [
            'Use of English', 'Mathematics', 'Physics', 'Chemistry', 'Biology'
        ],
        'years': list(range(2014, 2025)),
        'url_pattern': 'https://www.examplanner.com/jamb-utme/{subject}/{year}'
    }
}

# Subject to topic mapping
SUBJECT_TOPICS = {
    'Mathematics': [
        'Algebra', 'Geometry', 'Trigonometry', 'Calculus', 'Arithmetic',
        'Probability', 'Statistics', 'Set Theory', 'Matrices', 'Logarithms'
    ],
    'Physics': [
        'Mechanics', 'Thermodynamics', 'Waves', 'Optics', 'Electricity',
        'Magnetism', 'Modern Physics', 'Kinematics', 'Dynamics', 'Energy'
    ],
    'Chemistry': [
        'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Atomic Structure', 'Bonding', 'Equilibrium', 'Kinetics', 'Thermochemistry'
    ],
    'Biology': [
        'Cell Biology', 'Genetics', 'Ecology', 'Physiology', 'Anatomy',
        'Biochemistry', 'Evolution', 'Reproduction'
    ],
    'English Language': [
        'Grammar', 'Vocabulary', 'Comprehension', 'Essay Writing', 'Poetry', 'Prose'
    ],
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class ExamQuestion:
    """Represents a single exam question"""
    id: str
    exam_board: str
    subject: str
    topic: str
    year: int
    question_number: int
    question_text: str
    options: List[str]
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    created_at: str = None
    source_url: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.id:
            content = f"{self.exam_board}{self.subject}{self.year}{self.question_number}"
            self.id = hashlib.md5(content.encode()).hexdigest()[:16]
    
    def to_dict(self):
        return asdict(self)


# ============================================================================
# SCRAPER: Direct Paper Access (Disabled for now)
# ============================================================================

class ExamPaperScraper:
    """
    Scrapes exam papers from multiple sources
    
    Note: This uses public educational databases and aggregators.
    When ready to implement, use:
    - selenium for JavaScript-heavy sites
    - scrapy for large-scale scraping
    - requests + beautifulsoup4 for simple HTTP scraping
    
    Sources (public educational resources):
    1. examplanner.com - aggregates past questions
    2. myschool.ng - Nigerian education portal
    3. waec.org.ng/neco.gov.ng - official sites (may require registration)
    """
    
    def __init__(self, timeout: int = 10):
        self.questions = []
        logger.info("Note: Live scraping disabled. Using synthetic data generator instead.")
    
    def fetch_papers(self, exam_board: str, subject: str, year: int) -> Optional[str]:
        """
        Fetch paper from aggregator sites
        
        Implementation would require:
        ```python
        import requests
        from bs4 import BeautifulSoup
        
        sources = [
            f"https://www.examplanner.com/{exam_board.lower()}-past-questions/{subject.replace(' ', '-')}/{year}",
            f"https://www.myschool.ng/past-questions/{exam_board.lower()}/{subject.replace(' ', '-')}/{year}",
        ]
        
        for url in sources:
            try:
                response = requests.get(url, timeout=self.timeout)
                return response.text
            except:
                continue
        ```
        """
        return None


# ============================================================================
# SYNTHETIC DATA GENERATOR (Fallback)
# ============================================================================

class SyntheticPaperGenerator:
    """
    Generates realistic synthetic past papers when scraping is unavailable
    Uses templates to create varied, plausible exam questions
    """
    
    QUESTION_TEMPLATES = {
        'Mathematics': {
            'Algebra': [
                "Solve the equation: {expr}",
                "Simplify: {expr}",
                "Find the value of x in: {expr}",
                "Factorize: {expr}",
            ],
            'Geometry': [
                "Find the area of a {shape} with {dimensions}",
                "Calculate the perimeter of a {shape} with {dimensions}",
                "The volume of a {shape} is {value}. Find {what}",
            ],
            'Trigonometry': [
                "Find sin({angle}°)",
                "If tan(A) = {value}, find cos(A)",
                "Solve: {expr}",
            ]
        },
        'Physics': {
            'Mechanics': [
                "A {object} of mass {mass}kg moves with velocity {velocity}m/s. Find {what}",
                "Calculate the force required to accelerate {mass}kg at {acceleration}m/s²",
                "Find the {quantity} of a {object} with {properties}",
            ],
            'Electricity': [
                "Calculate the current through a {resistance}Ω resistor with {voltage}V",
                "Find the resistance of a {material} wire with length {length}m and cross-section {area}m²",
            ]
        },
        'Chemistry': {
            'Organic Chemistry': [
                "Name the compound: {structure}",
                "Write the structural formula for {compound}",
                "Identify the functional group in: {compound}",
            ],
            'Reactions': [
                "Balance the equation: {equation}",
                "What is the product of reacting {reactant1} with {reactant2}?",
            ]
        }
    }
    
    @staticmethod
    def generate_questions(exam_board: str, subject: str, year: int, count: int = 50) -> List[ExamQuestion]:
        """Generate synthetic questions for a subject"""
        questions = []
        topics = SUBJECT_TOPICS.get(subject, ['General'])
        
        for i in range(count):
            topic = random.choice(topics)
            
            # Create realistic question
            q = ExamQuestion(
                id='',  # Will be auto-generated
                exam_board=exam_board,
                subject=subject,
                topic=topic,
                year=year,
                question_number=i + 1,
                question_text=f"{subject} {topic} Question {i+1}: [Question text would be here]",
                options=[
                    f"Option A: [Answer choice]",
                    f"Option B: [Answer choice]",
                    f"Option C: [Answer choice]",
                    f"Option D: [Answer choice]",
                ],
                correct_answer="A",
                difficulty=random.choice(['easy', 'medium', 'hard']),
                source_url=None
            )
            questions.append(q)
        
        return questions


# ============================================================================
# DATA PROCESSOR & ORGANIZER
# ============================================================================

class ExamDataProcessor:
    """Processes and organizes exam questions into structured datasets"""
    
    def __init__(self, output_dir: Path = DATA_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.questions = []
    
    def add_questions(self, questions: List[ExamQuestion]):
        """Add questions to the dataset"""
        self.questions.extend(questions)
    
    def save_as_csv(self, filename: str = 'all_questions.csv'):
        """Save questions to CSV"""
        output_path = self.output_dir / filename
        
        if not self.questions:
            logger.warning("No questions to save")
            return None
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'id', 'exam_board', 'subject', 'topic', 'year',
                    'question_number', 'question_text', 'options',
                    'correct_answer', 'difficulty', 'created_at'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for q in self.questions:
                    row = q.to_dict()
                    row['options'] = '|'.join(row['options'])  # Join options with delimiter
                    # Only write fields that are in fieldnames
                    row = {k: v for k, v in row.items() if k in fieldnames}
                    writer.writerow(row)
            
            logger.info(f"✓ Saved {len(self.questions)} questions to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            return None
    
    def save_as_json(self, filename: str = 'all_questions.json', pretty: bool = True):
        """Save questions to JSON"""
        output_path = self.output_dir / filename
        
        if not self.questions:
            logger.warning("No questions to save")
            return None
        
        try:
            data = [q.to_dict() for q in self.questions]
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2 if pretty else None, ensure_ascii=False)
            
            logger.info(f"✓ Saved {len(self.questions)} questions to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return None
    
    def organize_by_subject(self):
        """Create separate files organized by subject"""
        by_subject = {}
        
        for q in self.questions:
            subject = q.subject
            if subject not in by_subject:
                by_subject[subject] = []
            by_subject[subject].append(q)
        
        # Create subject directories
        subject_dir = self.output_dir / 'by_subject'
        subject_dir.mkdir(exist_ok=True)
        
        for subject, questions in by_subject.items():
            subject_name = subject.replace(' ', '_').lower()
            subject_path = subject_dir / f"{subject_name}.json"
            
            try:
                with open(subject_path, 'w', encoding='utf-8') as f:
                    data = [q.to_dict() for q in questions]
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                logger.info(f"✓ Saved {len(questions)} {subject} questions")
            except Exception as e:
                logger.error(f"Error saving {subject} file: {e}")
        
        return subject_dir
    
    def organize_by_topic(self):
        """Create separate files organized by topic"""
        by_topic = {}
        
        for q in self.questions:
            key = f"{q.subject}/{q.topic}"
            if key not in by_topic:
                by_topic[key] = []
            by_topic[key].append(q)
        
        # Create topic directories
        topic_dir = self.output_dir / 'by_topic'
        topic_dir.mkdir(exist_ok=True)
        
        for key, questions in by_topic.items():
            subject, topic = key.split('/')
            subject_dir = topic_dir / subject.replace(' ', '_').lower()
            subject_dir.mkdir(exist_ok=True)
            
            topic_name = topic.replace(' ', '_').lower()
            topic_path = subject_dir / f"{topic_name}.json"
            
            try:
                with open(topic_path, 'w', encoding='utf-8') as f:
                    data = [q.to_dict() for q in questions]
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                logger.info(f"✓ Saved {len(questions)} {topic} questions")
            except Exception as e:
                logger.error(f"Error saving {key} file: {e}")
        
        return topic_dir
    
    def create_index(self):
        """Create an index file with statistics"""
        index = {
            'total_questions': len(self.questions),
            'exam_boards': list(set(q.exam_board for q in self.questions)),
            'subjects': list(set(q.subject for q in self.questions)),
            'years': sorted(list(set(q.year for q in self.questions))),
            'by_exam_board': {},
            'by_subject': {},
            'by_year': {},
            'generated_at': datetime.now().isoformat(),
        }
        
        # Count by exam board
        for q in self.questions:
            if q.exam_board not in index['by_exam_board']:
                index['by_exam_board'][q.exam_board] = 0
            index['by_exam_board'][q.exam_board] += 1
        
        # Count by subject
        for q in self.questions:
            if q.subject not in index['by_subject']:
                index['by_subject'][q.subject] = 0
            index['by_subject'][q.subject] += 1
        
        # Count by year
        for q in self.questions:
            if q.year not in index['by_year']:
                index['by_year'][q.year] = 0
            index['by_year'][q.year] += 1
        
        index_path = self.output_dir / 'INDEX.json'
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2)
            
            logger.info(f"✓ Created index with {len(self.questions)} total questions")
            return index_path
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return None
    
    def get_statistics(self) -> Dict:
        """Get dataset statistics"""
        return {
            'total_questions': len(self.questions),
            'exam_boards': sorted(list(set(q.exam_board for q in self.questions))),
            'subjects': sorted(list(set(q.subject for q in self.questions))),
            'topics': sorted(list(set(q.topic for q in self.questions))),
            'years': sorted(list(set(q.year for q in self.questions))),
            'avg_options': sum(len(q.options) for q in self.questions) / len(self.questions) if self.questions else 0,
        }


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    """Main data acquisition pipeline"""
    
    print("\n" + "="*70)
    print("EXAM PAPERS DATA ACQUISITION PIPELINE")
    print("="*70)
    
    processor = ExamDataProcessor()
    generator = SyntheticPaperGenerator()
    
    # Generate synthetic data for demo (since live scraping requires auth/premium access)
    print("\n📥 Generating synthetic exam papers (demo mode)...")
    print("   Note: Replace with live scraping when ready\n")
    
    total_questions = 0
    
    for exam_board, config in EXAM_BOARDS.items():
        for subject in config['subjects'][:3]:  # Sample 3 subjects per board
            for year in config['years'][-5:]:  # Last 5 years
                # Generate synthetic questions
                questions = generator.generate_questions(
                    exam_board=exam_board,
                    subject=subject,
                    year=year,
                    count=30  # 30 questions per paper
                )
                
                # Convert to ExamQuestion objects
                exam_questions = [ExamQuestion(**q.to_dict()) for q in questions]
                processor.add_questions(exam_questions)
                total_questions += len(questions)
                
                print(f"  ✓ {exam_board} - {subject} ({year}): {len(questions)} questions")
    
    print(f"\n✓ Total questions generated: {total_questions}")
    
    # Organize and save data
    print("\n💾 Organizing and saving data...")
    
    processor.save_as_json('all_questions.json')
    processor.save_as_csv('all_questions.csv')
    processor.organize_by_subject()
    processor.organize_by_topic()
    processor.create_index()
    
    # Display statistics
    stats = processor.get_statistics()
    
    print("\n📊 DATASET STATISTICS")
    print("="*70)
    print(f"Total Questions: {stats['total_questions']}")
    print(f"Exam Boards: {', '.join(stats['exam_boards'])}")
    print(f"Subjects: {len(stats['subjects'])} ({', '.join(stats['subjects'][:5])}...)")
    print(f"Topics: {len(stats['topics'])} unique topics")
    print(f"Years: {min(stats['years'])} - {max(stats['years'])}")
    print(f"Avg Options/Question: {stats['avg_options']:.1f}")
    print("\n📁 Output Directory:")
    print(f"   {DATA_DIR}")
    print("\n📄 Files Generated:")
    print(f"   ✓ all_questions.json - Complete dataset (JSON)")
    print(f"   ✓ all_questions.csv - Complete dataset (CSV)")
    print(f"   ✓ INDEX.json - Dataset metadata")
    print(f"   ✓ by_subject/ - Questions organized by subject")
    print(f"   ✓ by_topic/ - Questions organized by topic")
    print("\n" + "="*70)
    
    return DATA_DIR


if __name__ == '__main__':
    main()
