#!/usr/bin/env python3
"""
Wave 3 Interactive Dashboard
Comprehensive content browsing, search, progress tracking, and export
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import argparse


@dataclass
class LessonSummary:
    """Summary of a lesson for dashboard display"""
    id: str
    subject: str
    title: str
    description: str
    duration_minutes: int
    difficulty_level: str
    num_objectives: int
    num_sections: int
    num_examples: int
    num_problems: int
    nerdc_codes: List[str]
    waec_topics: List[str]
    keywords: List[str]
    prerequisites: List[str]


@dataclass
class StudentProgress:
    """Student progress tracking"""
    student_id: str
    lesson_id: str
    status: str  # not_started, in_progress, completed
    progress_percentage: float
    time_spent_minutes: int
    completed_problems: List[str]
    assessment_score: Optional[float]
    last_accessed: str


class Wave3Dashboard:
    """
    Interactive dashboard for Wave 3 content management
    """

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password",
                 use_neo4j: bool = True):
        self.uri = neo4j_uri
        self.user = neo4j_user
        self.password = neo4j_password
        self.driver = None
        self.neo4j_available = False
        
        self.subjects = [
            "Chemistry", "Biology", "English Language", "Economics",
            "Geography", "History", "Computer Science"
        ]
        
        if use_neo4j:
            self._connect()

    def _connect(self):
        """Connect to Neo4j"""
        try:
            # Try to import neo4j
            from neo4j import GraphDatabase, basic_auth
            
            # Check if port is open
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 7687))
            sock.close()
            
            if result != 0:
                # Port not open, use filesystem
                return
            
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=basic_auth(self.user, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            self.neo4j_available = True
            print("✅ Connected to Neo4j")
        except Exception:
            pass  # Silently fall back to filesystem

    def get_subjects_overview(self) -> List[Dict[str, Any]]:
        """Get overview of all subjects with lesson counts"""
        if not self.driver:
            return self._get_subjects_from_filesystem()
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Lesson)
                WHERE l.wave = 3 AND l.grade = 'SS1'
                RETURN l.subject as subject, 
                       count(l) as lesson_count,
                       avg(l.duration_minutes) as avg_duration,
                       collect(DISTINCT l.difficulty_level) as difficulty_levels
                ORDER BY subject
            """)
            
            subjects = []
            for record in result:
                subjects.append({
                    'subject': record['subject'],
                    'lesson_count': record['lesson_count'],
                    'avg_duration': round(record['avg_duration'], 1),
                    'difficulty_levels': record['difficulty_levels']
                })
            
            return subjects

    def _get_subjects_from_filesystem(self) -> List[Dict[str, Any]]:
        """Fallback: Get subjects from filesystem"""
        subjects = []
        for subject in self.subjects:
            lesson_dir = Path(f"content/ai_generated/textbooks/{subject}/SS1")
            if lesson_dir.exists():
                lesson_count = len(list(lesson_dir.glob("*.json")))
                subjects.append({
                    'subject': subject,
                    'lesson_count': lesson_count,
                    'avg_duration': 90.0,
                    'difficulty_levels': ['intermediate']
                })
        return subjects

    def get_lessons_by_subject(self, subject: str) -> List[LessonSummary]:
        """Get all lessons for a subject"""
        if not self.driver:
            return self._get_lessons_from_filesystem(subject)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Lesson)
                WHERE l.subject = $subject AND l.wave = 3
                OPTIONAL MATCH (l)-[:HAS_OBJECTIVE]->(lo:LearningObjective)
                OPTIONAL MATCH (l)-[:HAS_SECTION]->(cs:ContentSection)
                OPTIONAL MATCH (l)-[:HAS_EXAMPLE]->(we:WorkedExample)
                OPTIONAL MATCH (l)-[:HAS_PROBLEM]->(pp:PracticeProblem)
                OPTIONAL MATCH (l)-[:REQUIRES_PREREQUISITE]->(prereq:Lesson)
                RETURN l.id as id,
                       l.subject as subject,
                       l.title as title,
                       l.description as description,
                       l.duration_minutes as duration,
                       l.difficulty_level as difficulty,
                       l.nerdc_codes as nerdc_codes,
                       l.waec_topics as waec_topics,
                       l.keywords as keywords,
                       count(DISTINCT lo) as num_objectives,
                       count(DISTINCT cs) as num_sections,
                       count(DISTINCT we) as num_examples,
                       count(DISTINCT pp) as num_problems,
                       collect(DISTINCT prereq.id) as prerequisites
                ORDER BY l.id
            """, {"subject": subject})
            
            lessons = []
            for record in result:
                lessons.append(LessonSummary(
                    id=record['id'],
                    subject=record['subject'],
                    title=record['title'],
                    description=record['description'],
                    duration_minutes=record['duration'],
                    difficulty_level=record['difficulty'],
                    num_objectives=record['num_objectives'],
                    num_sections=record['num_sections'],
                    num_examples=record['num_examples'],
                    num_problems=record['num_problems'],
                    nerdc_codes=record['nerdc_codes'] or [],
                    waec_topics=record['waec_topics'] or [],
                    keywords=record['keywords'] or [],
                    prerequisites=record['prerequisites']
                ))
            
            return lessons

    def _get_lessons_from_filesystem(self, subject: str) -> List[LessonSummary]:
        """Fallback: Get lessons from filesystem"""
        lessons = []
        lesson_dir = Path(f"content/ai_generated/textbooks/{subject}/SS1")
        
        if not lesson_dir.exists():
            return lessons
        
        for lesson_file in sorted(lesson_dir.glob("*.json")):
            try:
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata = data.get('metadata', {})
                    
                    lessons.append(LessonSummary(
                        id=lesson_file.stem,
                        subject=subject,
                        title=metadata.get('title', ''),
                        description=metadata.get('description', ''),
                        duration_minutes=metadata.get('duration_minutes', 90),
                        difficulty_level=metadata.get('difficulty_level', 'intermediate'),
                        num_objectives=len(data.get('learning_objectives', [])),
                        num_sections=len(data.get('content_sections', [])),
                        num_examples=len(data.get('worked_examples', [])),
                        num_problems=len(data.get('practice_problems', [])),
                        nerdc_codes=metadata.get('nerdc_references', []),
                        waec_topics=metadata.get('waec_tags', []),
                        keywords=metadata.get('keywords', []),
                        prerequisites=data.get('prerequisites', [])
                    ))
            except Exception as e:
                print(f"⚠️ Error loading {lesson_file}: {e}")
        
        return lessons

    def search_by_nerdc_code(self, nerdc_code: str) -> List[LessonSummary]:
        """Search lessons by NERDC curriculum code"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Lesson)-[:ALIGNS_WITH_NERDC]->(n:NERDCCode)
                WHERE n.code CONTAINS $code AND l.wave = 3
                OPTIONAL MATCH (l)-[:HAS_OBJECTIVE]->(lo:LearningObjective)
                OPTIONAL MATCH (l)-[:HAS_SECTION]->(cs:ContentSection)
                OPTIONAL MATCH (l)-[:HAS_EXAMPLE]->(we:WorkedExample)
                OPTIONAL MATCH (l)-[:HAS_PROBLEM]->(pp:PracticeProblem)
                RETURN DISTINCT l.id as id,
                       l.subject as subject,
                       l.title as title,
                       l.description as description,
                       l.duration_minutes as duration,
                       l.difficulty_level as difficulty,
                       l.nerdc_codes as nerdc_codes,
                       l.waec_topics as waec_topics,
                       l.keywords as keywords,
                       count(DISTINCT lo) as num_objectives,
                       count(DISTINCT cs) as num_sections,
                       count(DISTINCT we) as num_examples,
                       count(DISTINCT pp) as num_problems
                ORDER BY l.subject, l.id
            """, {"code": nerdc_code})
            
            return self._process_lesson_results(result)

    def search_by_waec_topic(self, waec_topic: str) -> List[LessonSummary]:
        """Search lessons by WAEC exam topic"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Lesson)-[:ALIGNS_WITH_WAEC]->(w:WAECTopic)
                WHERE w.topic CONTAINS $topic AND l.wave = 3
                OPTIONAL MATCH (l)-[:HAS_OBJECTIVE]->(lo:LearningObjective)
                OPTIONAL MATCH (l)-[:HAS_SECTION]->(cs:ContentSection)
                OPTIONAL MATCH (l)-[:HAS_EXAMPLE]->(we:WorkedExample)
                OPTIONAL MATCH (l)-[:HAS_PROBLEM]->(pp:PracticeProblem)
                RETURN DISTINCT l.id as id,
                       l.subject as subject,
                       l.title as title,
                       l.description as description,
                       l.duration_minutes as duration,
                       l.difficulty_level as difficulty,
                       l.nerdc_codes as nerdc_codes,
                       l.waec_topics as waec_topics,
                       l.keywords as keywords,
                       count(DISTINCT lo) as num_objectives,
                       count(DISTINCT cs) as num_sections,
                       count(DISTINCT we) as num_examples,
                       count(DISTINCT pp) as num_problems
                ORDER BY l.subject, l.id
            """, {"topic": waec_topic})
            
            return self._process_lesson_results(result)

    def search_by_keyword(self, keyword: str) -> List[LessonSummary]:
        """Search lessons by keyword"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Lesson)
                WHERE l.wave = 3 AND (
                    any(k IN l.keywords WHERE toLower(k) CONTAINS toLower($keyword))
                    OR toLower(l.title) CONTAINS toLower($keyword)
                    OR toLower(l.description) CONTAINS toLower($keyword)
                )
                OPTIONAL MATCH (l)-[:HAS_OBJECTIVE]->(lo:LearningObjective)
                OPTIONAL MATCH (l)-[:HAS_SECTION]->(cs:ContentSection)
                OPTIONAL MATCH (l)-[:HAS_EXAMPLE]->(we:WorkedExample)
                OPTIONAL MATCH (l)-[:HAS_PROBLEM]->(pp:PracticeProblem)
                RETURN l.id as id,
                       l.subject as subject,
                       l.title as title,
                       l.description as description,
                       l.duration_minutes as duration,
                       l.difficulty_level as difficulty,
                       l.nerdc_codes as nerdc_codes,
                       l.waec_topics as waec_topics,
                       l.keywords as keywords,
                       count(DISTINCT lo) as num_objectives,
                       count(DISTINCT cs) as num_sections,
                       count(DISTINCT we) as num_examples,
                       count(DISTINCT pp) as num_problems
                ORDER BY l.subject, l.id
            """, {"keyword": keyword})
            
            return self._process_lesson_results(result)

    def _process_lesson_results(self, result) -> List[LessonSummary]:
        """Process Neo4j results into LessonSummary objects"""
        lessons = []
        for record in result:
            lessons.append(LessonSummary(
                id=record['id'],
                subject=record['subject'],
                title=record['title'],
                description=record['description'],
                duration_minutes=record['duration'],
                difficulty_level=record['difficulty'],
                num_objectives=record['num_objectives'],
                num_sections=record['num_sections'],
                num_examples=record['num_examples'],
                num_problems=record['num_problems'],
                nerdc_codes=record['nerdc_codes'] or [],
                waec_topics=record['waec_topics'] or [],
                keywords=record['keywords'] or [],
                prerequisites=[]
            ))
        return lessons

    def get_lesson_content(self, lesson_id: str) -> Optional[Dict]:
        """Get full lesson content for rendering"""
        # Load from filesystem
        for subject in self.subjects:
            lesson_path = Path(f"content/ai_generated/textbooks/{subject}/SS1/{lesson_id}.json")
            if lesson_path.exists():
                with open(lesson_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return None

    def get_cross_subject_connections(self, lesson_id: str) -> List[Dict]:
        """Get cross-subject connections for a lesson"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l1:Lesson {id: $lesson_id})-[r:CONNECTS_TO]-(l2:Lesson)
                RETURN l2.id as connected_lesson_id,
                       l2.subject as subject,
                       l2.title as title,
                       r.type as connection_type
            """, {"lesson_id": lesson_id})
            
            connections = []
            for record in result:
                connections.append({
                    'lesson_id': record['connected_lesson_id'],
                    'subject': record['subject'],
                    'title': record['title'],
                    'connection_type': record['connection_type']
                })
            
            return connections

    def track_student_progress(self, student_id: str, lesson_id: str,
                               status: str, progress_percentage: float,
                               time_spent_minutes: int = 0,
                               completed_problems: List[str] = None,
                               assessment_score: Optional[float] = None):
        """Track student progress for a lesson"""
        if not self.driver:
            print("⚠️ Progress tracking requires Neo4j connection")
            return
        
        with self.driver.session() as session:
            session.run("""
                MERGE (s:Student {id: $student_id})
                MERGE (l:Lesson {id: $lesson_id})
                MERGE (s)-[p:STUDYING]->(l)
                SET p.status = $status,
                    p.progress_percentage = $progress_percentage,
                    p.time_spent_minutes = $time_spent_minutes,
                    p.completed_problems = $completed_problems,
                    p.assessment_score = $assessment_score,
                    p.last_accessed = datetime()
            """, {
                "student_id": student_id,
                "lesson_id": lesson_id,
                "status": status,
                "progress_percentage": progress_percentage,
                "time_spent_minutes": time_spent_minutes,
                "completed_problems": completed_problems or [],
                "assessment_score": assessment_score
            })
            
            print(f"✅ Progress tracked: {student_id} - {lesson_id} ({status})")

    def get_student_progress(self, student_id: str) -> List[StudentProgress]:
        """Get all progress records for a student"""
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Student {id: $student_id})-[p:STUDYING]->(l:Lesson)
                WHERE l.wave = 3
                RETURN l.id as lesson_id,
                       p.status as status,
                       p.progress_percentage as progress_percentage,
                       p.time_spent_minutes as time_spent_minutes,
                       p.completed_problems as completed_problems,
                       p.assessment_score as assessment_score,
                       toString(p.last_accessed) as last_accessed
                ORDER BY p.last_accessed DESC
            """, {"student_id": student_id})
            
            progress_list = []
            for record in result:
                progress_list.append(StudentProgress(
                    student_id=student_id,
                    lesson_id=record['lesson_id'],
                    status=record['status'],
                    progress_percentage=record['progress_percentage'],
                    time_spent_minutes=record['time_spent_minutes'],
                    completed_problems=record['completed_problems'] or [],
                    assessment_score=record['assessment_score'],
                    last_accessed=record['last_accessed']
                ))
            
            return progress_list

    def export_lesson_for_teacher(self, lesson_id: str, output_format: str = 'json') -> str:
        """Export lesson content for teacher use"""
        lesson_data = self.get_lesson_content(lesson_id)
        
        if not lesson_data:
            print(f"❌ Lesson not found: {lesson_id}")
            return ""
        
        output_dir = Path("exports/teacher_resources")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if output_format == 'json':
            output_file = output_dir / f"{lesson_id}_teacher_resource.json"
            
            # Add teacher notes
            teacher_resource = {
                "lesson_id": lesson_id,
                "exported_at": datetime.now().isoformat(),
                "lesson_data": lesson_data,
                "teaching_notes": {
                    "duration": lesson_data.get('metadata', {}).get('duration_minutes', 90),
                    "difficulty": lesson_data.get('metadata', {}).get('difficulty_level', 'intermediate'),
                    "materials_needed": [],
                    "preparation_tips": [
                        "Review all worked examples before class",
                        "Prepare additional local examples if needed",
                        "Test practice problems to gauge difficulty",
                        "Prepare assessment rubric"
                    ],
                    "differentiation_strategies": lesson_data.get('differentiation_strategies', [])
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(teacher_resource, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported: {output_file}")
            return str(output_file)
        
        elif output_format == 'markdown':
            # Load rendered markdown
            for subject in self.subjects:
                md_path = Path(f"content/ai_rendered/textbooks/{subject}/SS1/{lesson_id}.md")
                if md_path.exists():
                    output_file = output_dir / f"{lesson_id}_teacher_resource.md"
                    
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add teacher header
                    teacher_content = f"""# Teacher Resource: {lesson_data.get('metadata', {}).get('title', '')}

**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Subject:** {lesson_data.get('metadata', {}).get('subject', '')}
**Duration:** {lesson_data.get('metadata', {}).get('duration_minutes', 90)} minutes
**Difficulty:** {lesson_data.get('metadata', {}).get('difficulty_level', 'intermediate')}

---

{content}
"""
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(teacher_content)
                    
                    print(f"✅ Exported: {output_file}")
                    return str(output_file)
        
        return ""

    def generate_dashboard_report(self, output_file: str = None) -> Dict:
        """Generate comprehensive dashboard report"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"reports/wave3_dashboard_report_{timestamp}.json"
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "wave": 3,
            "grade": "SS1",
            "subjects": {},
            "totals": {
                "total_lessons": 0,
                "total_objectives": 0,
                "total_examples": 0,
                "total_problems": 0,
                "total_duration_minutes": 0
            },
            "curriculum_alignment": {
                "nerdc_codes": set(),
                "waec_topics": set()
            }
        }
        
        # Get data for each subject
        for subject in self.subjects:
            lessons = self.get_lessons_by_subject(subject)
            
            if lessons:
                subject_data = {
                    "lesson_count": len(lessons),
                    "lessons": [asdict(lesson) for lesson in lessons],
                    "total_duration": sum(l.duration_minutes for l in lessons),
                    "avg_objectives": sum(l.num_objectives for l in lessons) / len(lessons),
                    "avg_examples": sum(l.num_examples for l in lessons) / len(lessons),
                    "avg_problems": sum(l.num_problems for l in lessons) / len(lessons)
                }
                
                report["subjects"][subject] = subject_data
                report["totals"]["total_lessons"] += len(lessons)
                report["totals"]["total_objectives"] += sum(l.num_objectives for l in lessons)
                report["totals"]["total_examples"] += sum(l.num_examples for l in lessons)
                report["totals"]["total_problems"] += sum(l.num_problems for l in lessons)
                report["totals"]["total_duration_minutes"] += subject_data["total_duration"]
                
                # Collect curriculum codes
                for lesson in lessons:
                    report["curriculum_alignment"]["nerdc_codes"].update(lesson.nerdc_codes)
                    report["curriculum_alignment"]["waec_topics"].update(lesson.waec_topics)
        
        # Convert sets to lists for JSON serialization
        report["curriculum_alignment"]["nerdc_codes"] = sorted(list(report["curriculum_alignment"]["nerdc_codes"]))
        report["curriculum_alignment"]["waec_topics"] = sorted(list(report["curriculum_alignment"]["waec_topics"]))
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dashboard report generated: {output_file}")
        return report

    def print_subject_menu(self):
        """Print interactive subject menu"""
        print("\n" + "=" * 60)
        print("Wave 3 Interactive Dashboard - SS1 Curriculum")
        print("=" * 60)
        
        subjects = self.get_subjects_overview()
        
        print("\n📚 Available Subjects:\n")
        for idx, subject in enumerate(subjects, 1):
            print(f"  {idx}. {subject['subject']:<20} "
                  f"({subject['lesson_count']} lessons, "
                  f"~{subject['avg_duration']:.0f} min avg)")
        
        print("\n  0. Exit")
        return subjects

    def print_lesson_list(self, lessons: List[LessonSummary]):
        """Print list of lessons"""
        print("\n" + "-" * 60)
        print(f"Found {len(lessons)} lesson(s):\n")
        
        for idx, lesson in enumerate(lessons, 1):
            print(f"{idx}. {lesson.title}")
            print(f"   Subject: {lesson.subject} | Duration: {lesson.duration_minutes} min | "
                  f"Difficulty: {lesson.difficulty_level}")
            print(f"   Components: {lesson.num_objectives} objectives, {lesson.num_sections} sections, "
                  f"{lesson.num_examples} examples, {lesson.num_problems} problems")
            if lesson.keywords:
                print(f"   Keywords: {', '.join(lesson.keywords[:5])}")
            print()

    def interactive_mode(self):
        """Run dashboard in interactive mode"""
        while True:
            subjects = self.print_subject_menu()
            
            try:
                choice = input("\n👉 Select subject (0-7): ").strip()
                
                if choice == '0':
                    print("\n👋 Goodbye!")
                    break
                
                idx = int(choice) - 1
                if 0 <= idx < len(subjects):
                    subject = subjects[idx]['subject']
                    lessons = self.get_lessons_by_subject(subject)
                    self.print_lesson_list(lessons)
                    
                    input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid choice")
                
            except (ValueError, IndexError):
                print("❌ Invalid input")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Wave 3 Interactive Dashboard")
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--subject', '-s', type=str,
                       help='Get lessons for specific subject')
    parser.add_argument('--search-nerdc', type=str,
                       help='Search by NERDC code')
    parser.add_argument('--search-waec', type=str,
                       help='Search by WAEC topic')
    parser.add_argument('--search-keyword', type=str,
                       help='Search by keyword')
    parser.add_argument('--export', '-e', type=str,
                       help='Export lesson ID for teacher use')
    parser.add_argument('--format', '-f', type=str, default='json',
                       choices=['json', 'markdown'],
                       help='Export format (default: json)')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate dashboard report')
    
    args = parser.parse_args()
    
    dashboard = Wave3Dashboard()
    
    try:
        if args.interactive:
            dashboard.interactive_mode()
        
        elif args.subject:
            lessons = dashboard.get_lessons_by_subject(args.subject)
            dashboard.print_lesson_list(lessons)
        
        elif args.search_nerdc:
            lessons = dashboard.search_by_nerdc_code(args.search_nerdc)
            dashboard.print_lesson_list(lessons)
        
        elif args.search_waec:
            lessons = dashboard.search_by_waec_topic(args.search_waec)
            dashboard.print_lesson_list(lessons)
        
        elif args.search_keyword:
            lessons = dashboard.search_by_keyword(args.search_keyword)
            dashboard.print_lesson_list(lessons)
        
        elif args.export:
            dashboard.export_lesson_for_teacher(args.export, args.format)
        
        elif args.report:
            dashboard.generate_dashboard_report()
        
        else:
            # Default: show overview
            subjects = dashboard.get_subjects_overview()
            print("\n📊 Wave 3 Dashboard Overview:\n")
            for subject in subjects:
                print(f"  {subject['subject']:<20} {subject['lesson_count']} lessons")
            print("\nUse --help for more options")
    
    finally:
        dashboard.close()


if __name__ == "__main__":
    main()
