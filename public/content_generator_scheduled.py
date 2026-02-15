#!/usr/bin/env python3
"""
Content Generator with Automated Scheduling
Generates and schedules content creation daily

Usage:
    python content_generator_scheduled.py --start-daily
    python content_generator_scheduled.py --run-once
"""

import json
import os
import schedule
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

# ============================================================================
# 1. CONFIGURATION
# ============================================================================

class ScheduledContentConfig:
    """Configuration for scheduled content generation"""
    
    OUTPUT_DIR = "generated_content"
    LOG_FILE = "content_generation.log"
    
    # Daily generation schedule
    DAILY_SCHEDULE = {
        "10:00": "generate_study_guides",  # Morning: Study guides
        "14:00": "generate_questions",     # Afternoon: Questions
        "18:00": "generate_mocks"          # Evening: Mock exams
    }
    
    SUBJECTS = {
        "Chemistry": ["Atomic Structure", "Bonding", "Stoichiometry"],
        "Biology": ["Cell Biology", "Genetics", "Ecology"],
        "English": ["Grammar", "Vocabulary", "Literature"],
        "Mathematics": ["Trigonometry", "Statistics", "Calculus"]
    }


# ============================================================================
# 2. LOGGING SYSTEM
# ============================================================================

class ContentLogger:
    """Log all content generation activities"""
    
    def __init__(self, log_file: str = ScheduledContentConfig.LOG_FILE):
        self.log_file = Path(log_file)
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create log file if it doesn't exist"""
        if not self.log_file.exists():
            self.log_file.touch()
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        
        # Write to file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
        
        # Print to console
        print(log_message)
    
    def log_success(self, message: str):
        """Log a success message"""
        self.log(f"✅ {message}", "SUCCESS")
    
    def log_error(self, message: str):
        """Log an error message"""
        self.log(f"❌ {message}", "ERROR")
    
    def log_info(self, message: str):
        """Log an info message"""
        self.log(f"ℹ️  {message}", "INFO")


# ============================================================================
# 3. CONTENT GENERATOR (SCHEDULED)
# ============================================================================

class ScheduledContentGenerator:
    """Generate content on a schedule"""
    
    def __init__(self):
        self.logger = ContentLogger()
        self.output_dir = Path(ScheduledContentConfig.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        self.generation_stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        """Load generation statistics"""
        stats_file = self.output_dir / "generation_stats.json"
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                return json.load(f)
        return {
            "total_guides": 0,
            "total_questions": 0,
            "total_mocks": 0,
            "last_generated": None
        }
    
    def save_stats(self):
        """Save generation statistics"""
        stats_file = self.output_dir / "generation_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.generation_stats, f, indent=2)
    
    def generate_study_guides(self):
        """Generate study guides daily"""
        self.logger.log_info("Starting study guide generation...")
        
        guides_created = 0
        for subject, topics in ScheduledContentConfig.SUBJECTS.items():
            for topic in topics:
                guide_data = {
                    "subject": subject,
                    "topic": topic,
                    "generated_at": datetime.now().isoformat(),
                    "template_status": "Auto-generated template",
                    "expert_review_needed": True
                }
                
                # Save guide
                filename = f"{subject.lower()}_{topic.lower().replace(' ', '_')}_guide.json"
                filepath = self.output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(guide_data, f, indent=2)
                
                guides_created += 1
        
        self.generation_stats["total_guides"] += guides_created
        self.generation_stats["last_generated"] = datetime.now().isoformat()
        self.save_stats()
        
        self.logger.log_success(f"Generated {guides_created} study guide templates")
        return guides_created
    
    def generate_questions(self):
        """Generate practice questions daily"""
        self.logger.log_info("Starting question generation...")
        
        questions_created = 0
        for subject, topics in ScheduledContentConfig.SUBJECTS.items():
            for topic in topics:
                # Generate 10 questions per topic
                questions = []
                for i in range(10):
                    question = {
                        "id": f"{subject.lower()}_{topic.lower().replace(' ', '_')}_{i:03d}",
                        "subject": subject,
                        "topic": topic,
                        "question_text": f"[Auto-generated Q{i+1} - Needs expert content]",
                        "difficulty": ["easy", "medium", "hard"][i % 3],
                        "generated_at": datetime.now().isoformat()
                    }
                    questions.append(question)
                
                # Save questions
                filename = f"{subject.lower()}_{topic.lower().replace(' ', '_')}_questions.json"
                filepath = self.output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({"questions": questions}, f, indent=2)
                
                questions_created += len(questions)
        
        self.generation_stats["total_questions"] += questions_created
        self.save_stats()
        
        self.logger.log_success(f"Generated {questions_created} practice questions")
        return questions_created
    
    def generate_mocks(self):
        """Generate mock exams daily"""
        self.logger.log_info("Starting mock exam generation...")
        
        mock_number = self.generation_stats["total_mocks"] + 1
        mock_data = {
            "id": f"mock_{mock_number:03d}",
            "name": f"Mock Exam #{mock_number}",
            "generated_at": datetime.now().isoformat(),
            "totalQuestions": 180,
            "sections": [
                {"subject": "English", "questions": 40},
                {"subject": "Mathematics", "questions": 40},
                {"subject": "Chemistry", "questions": 50},
                {"subject": "Biology", "questions": 50}
            ],
            "template_status": "Auto-generated structure"
        }
        
        # Save mock
        filename = f"mock_exam_{mock_number:03d}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mock_data, f, indent=2)
        
        self.generation_stats["total_mocks"] += 1
        self.save_stats()
        
        self.logger.log_success(f"Generated mock exam #{mock_number}")
        return 1
    
    def generate_all_once(self):
        """Generate all content once"""
        self.logger.log_info("=" * 60)
        self.logger.log_info("STARTING BULK CONTENT GENERATION")
        self.logger.log_info("=" * 60)
        
        guides = self.generate_study_guides()
        questions = self.generate_questions()
        mocks = self.generate_mocks()
        
        self.logger.log_info("=" * 60)
        self.logger.log_info("GENERATION COMPLETE")
        self.logger.log_info(f"Guides: {guides} | Questions: {questions} | Mocks: {mocks}")
        self.logger.log_info("=" * 60)
    
    def schedule_daily_generation(self):
        """Schedule daily content generation"""
        self.logger.log_info("Setting up daily content generation schedule...")
        
        # Schedule tasks
        schedule.every().day.at("10:00").do(self.generate_study_guides)
        schedule.every().day.at("14:00").do(self.generate_questions)
        schedule.every().day.at("18:00").do(self.generate_mocks)
        
        self.logger.log_success("Daily schedule configured")
        self.logger.log_info("Task 1: Generate study guides at 10:00 AM")
        self.logger.log_info("Task 2: Generate questions at 2:00 PM")
        self.logger.log_info("Task 3: Generate mocks at 6:00 PM")
        
        # Run scheduler
        self.logger.log_info("Scheduler is now running. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.log_info("Scheduler stopped by user")


# ============================================================================
# 4. PROGRESS REPORTER
# ============================================================================

class ProgressReporter:
    """Report on content generation progress"""
    
    def __init__(self, output_dir: str = ScheduledContentConfig.OUTPUT_DIR):
        self.output_dir = Path(output_dir)
    
    def generate_report(self) -> str:
        """Generate a progress report"""
        stats_file = self.output_dir / "generation_stats.json"
        
        if not stats_file.exists():
            return "No generation data found"
        
        with open(stats_file, 'r') as f:
            stats = json.load(f)
        
        report = f"""
        ╔════════════════════════════════════════════════════════════════╗
        ║        CONTENT GENERATION PROGRESS REPORT                     ║
        ║        Generated: {stats.get('last_generated', 'Never')}                  ║
        ╚════════════════════════════════════════════════════════════════╝
        
        📊 STATISTICS
        ─────────────────────────────────────────────────────────────────
        Study Guides:        {stats.get('total_guides', 0):>3} 
        Practice Questions:  {stats.get('total_questions', 0):>3}
        Mock Exams:          {stats.get('total_mocks', 0):>3}
        ─────────────────────────────────────────────────────────────────
        
        📈 PROGRESS
        ─────────────────────────────────────────────────────────────────
        Guides (Target: 50)      [{stats.get('total_guides', 0)}/50] {int(stats.get('total_guides', 0)*100/50)}%
        Questions (Target: 2000) [{stats.get('total_questions', 0)}/2000] {int(stats.get('total_questions', 0)*100/2000)}%
        Mocks (Target: 10)       [{stats.get('total_mocks', 0)}/10] {int(stats.get('total_mocks', 0)*100/10)}%
        ─────────────────────────────────────────────────────────────────
        
        🎯 NEXT ACTIONS
        ─────────────────────────────────────────────────────────────────
        ✓ Continue daily generation
        ✓ Review generated content quality
        ✓ Distribute to expert reviewers
        ✓ Monitor student feedback
        ─────────────────────────────────────────────────────────────────
        """
        
        return report
    
    def display_report(self):
        """Display progress report"""
        print(self.generate_report())


# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point"""
    
    generator = ScheduledContentGenerator()
    reporter = ProgressReporter()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--run-once":
            generator.generate_all_once()
            reporter.display_report()
        
        elif command == "--start-daily":
            generator.schedule_daily_generation()
        
        elif command == "--report":
            reporter.display_report()
        
        else:
            print("Usage:")
            print("  python content_generator_scheduled.py --run-once    # Generate all content once")
            print("  python content_generator_scheduled.py --start-daily # Start daily scheduler")
            print("  python content_generator_scheduled.py --report      # Show progress report")
    
    else:
        # Default: run once and show report
        generator.generate_all_once()
        reporter.display_report()


if __name__ == "__main__":
    main()
