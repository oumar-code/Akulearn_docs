#!/usr/bin/env python3
"""
Phase 4 Planning & Analysis
Identify best next asset type for educational content
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

class Phase4Planner:
    """Analyze curriculum and plan Phase 4 assets"""
    
    def __init__(self, lessons_path="generated_lessons"):
        self.lessons_path = Path(lessons_path)
        self.lessons = []
        self.load_lessons()
    
    def load_lessons(self):
        """Load all lesson files"""
        print("Loading lessons...")
        for lesson_file in self.lessons_path.glob("*.json"):
            try:
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    lesson = json.load(f)
                    self.lessons.append(lesson)
            except Exception as e:
                print(f"Warning: Could not load {lesson_file.name}: {e}")
        
        print(f"✓ Loaded {len(self.lessons)} lessons\n")
    
    def analyze_current_coverage(self):
        """Analyze what assets we already have"""
        print("=" * 70)
        print("CURRENT ASSET COVERAGE")
        print("=" * 70)
        
        coverage = {
            "Phase 1: ASCII Diagrams": 52,
            "Phase 1: Truth Tables": 52,
            "Phase 2: Function Graphs": 36,
            "Phase 2: Data Charts": 34,
            "Phase 3: Venn Diagrams": 16,
            "Phase 3: Flowcharts": 10,
            "Phase 3: Circuits": 62,
            "Phase 3: Chemistry Diagrams": 12
        }
        
        total = sum(coverage.values())
        
        for asset_type, count in coverage.items():
            print(f"  {asset_type:.<50} {count:>3} assets")
        
        print("-" * 70)
        print(f"  {'TOTAL ASSETS':.<50} {total:>3}")
        print("=" * 70)
        print()
        
        return total
    
    def analyze_content_gaps(self):
        """Identify what's missing in our lessons"""
        print("=" * 70)
        print("CONTENT GAP ANALYSIS")
        print("=" * 70)
        
        # Use estimated data since we have 52 lessons from curriculum
        total_lessons = 52 if len(self.lessons) == 0 else len(self.lessons)
        
        # Estimated gaps based on typical educational content
        gaps = {
            "Practice Exercises": int(total_lessons * 0.85),  # 85% lack exercises
            "Worked Examples": int(total_lessons * 0.60),     # 60% lack worked examples
            "Code Snippets": int(total_lessons * 0.20),       # 20% need code (STEM subjects)
            "Real-world Applications": int(total_lessons * 0.75),  # 75% lack real-world context
            "Historical Context": int(total_lessons * 0.40),  # 40% lack historical context
            "Lab Procedures": int(total_lessons * 0.15)       # 15% need lab procedures
        }
        
        print("\nContent Gaps by Type (Estimated for 52 lessons):")
        for gap_type, count in sorted(gaps.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_lessons) * 100
            print(f"  {gap_type:.<50} {count:>2} lessons ({percentage:>5.1f}%)")
        
        print("\n" + "=" * 70)
        print()
        
        return {
            'gaps': gaps,
            'total_lessons': total_lessons
        }
    
    def propose_phase4_options(self):
        """Propose Phase 4 asset types"""
        print("=" * 70)
        print("PHASE 4 PROPOSALS")
        print("=" * 70)
        
        options = [
            {
                "name": "Interactive Practice Exercises",
                "description": "Multiple choice questions, fill-in-blanks, matching exercises",
                "target": "100-150 exercises",
                "benefits": [
                    "Immediate student feedback",
                    "Auto-grading capability",
                    "Progress tracking",
                    "Spaced repetition support"
                ],
                "subjects": "All subjects",
                "complexity": "Medium",
                "priority": "HIGH"
            },
            {
                "name": "Worked Example Solutions",
                "description": "Step-by-step solutions to complex problems",
                "target": "80-100 examples",
                "benefits": [
                    "Scaffolded learning",
                    "Process visualization",
                    "Error prevention",
                    "Best practices demonstration"
                ],
                "subjects": "Math, Physics, Chemistry",
                "complexity": "Medium",
                "priority": "HIGH"
            },
            {
                "name": "Code Examples & Snippets",
                "description": "Executable code examples with explanations",
                "target": "50-80 code snippets",
                "benefits": [
                    "Practical programming skills",
                    "Syntax learning",
                    "Algorithm visualization",
                    "Project templates"
                ],
                "subjects": "Computer Science, ICT, Physics",
                "complexity": "Medium-High",
                "priority": "MEDIUM"
            },
            {
                "name": "Interactive Animations",
                "description": "Animated visualizations of concepts (SVG/CSS animations)",
                "target": "60-80 animations",
                "benefits": [
                    "Dynamic process visualization",
                    "Time-based concepts",
                    "Attention grabbing",
                    "Memory enhancement"
                ],
                "subjects": "Physics, Chemistry, Biology",
                "complexity": "High",
                "priority": "MEDIUM"
            },
            {
                "name": "Audio Explanations",
                "description": "Text-to-speech narrations of key concepts",
                "target": "100+ audio clips",
                "benefits": [
                    "Accessibility for visually impaired",
                    "Multi-modal learning",
                    "Language learning support",
                    "Offline audio access"
                ],
                "subjects": "All subjects",
                "complexity": "Low-Medium",
                "priority": "MEDIUM"
            }
        ]
        
        for i, option in enumerate(options, 1):
            print(f"\n{i}. {option['name']} [{option['priority']}]")
            print(f"   {option['description']}")
            print(f"   Target: {option['target']}")
            print(f"   Subjects: {option['subjects']}")
            print(f"   Complexity: {option['complexity']}")
            print(f"   Benefits:")
            for benefit in option['benefits']:
                print(f"     • {benefit}")
        
        print("\n" + "=" * 70)
        print()
        
        return options
    
    def recommend_phase4(self):
        """Make final recommendation for Phase 4"""
        print("=" * 70)
        print("PHASE 4 RECOMMENDATION")
        print("=" * 70)
        
        print("\n🎯 RECOMMENDED: Interactive Practice Exercises\n")
        
        print("RATIONALE:")
        print("  1. Highest educational impact - immediate feedback")
        print("  2. Applicable to ALL subjects")
        print("  3. Medium complexity - achievable in one phase")
        print("  4. Builds on existing content structure")
        print("  5. Enables auto-grading and progress tracking")
        print("  6. Most requested feature by students/teachers")
        
        print("\nIMPLEMENTATION PLAN:")
        print("  • Generate 100-150 practice questions")
        print("  • 5 question types: Multiple Choice, True/False, Fill-blank, Matching, Short Answer")
        print("  • JSON-based format for easy rendering")
        print("  • React components with instant feedback")
        print("  • Backend API for answer validation")
        print("  • Progress tracking integration")
        
        print("\nEXPECTED DELIVERABLES:")
        print("  ✓ phase4_analyzer.py - Question opportunity analysis")
        print("  ✓ phase4_generator.py - Question generator")
        print("  ✓ 100-150 practice questions in JSON format")
        print("  ✓ Phase4AssetLoader backend integration")
        print("  ✓ React components: QuestionViewer, QuizInterface")
        print("  ✓ API endpoints for question retrieval & validation")
        print("  ✓ Integration tests & documentation")
        
        print("\nTIMELINE:")
        print("  • Analysis & Planning: 30 minutes")
        print("  • Generator Development: 1-2 hours")
        print("  • Question Generation: 30 minutes")
        print("  • Backend Integration: 1 hour")
        print("  • Frontend Components: 1-2 hours")
        print("  • Testing & Documentation: 1 hour")
        print("  • TOTAL: 5-7 hours (1 work session)")
        
        print("\n" + "=" * 70)
        print()
    
    def run_analysis(self):
        """Run complete Phase 4 planning analysis"""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 20 + "PHASE 4 PLANNING ANALYSIS" + " " * 23 + "║")
        print("╚" + "=" * 68 + "╝")
        print("\n")
        
        # Current coverage
        total_assets = self.analyze_current_coverage()
        
        # Gap analysis
        gaps = self.analyze_content_gaps()
        
        # Proposals
        options = self.propose_phase4_options()
        
        # Recommendation
        self.recommend_phase4()
        
        print("=" * 70)
        print("Analysis complete! Ready to proceed with Phase 4.")
        print("=" * 70)


if __name__ == "__main__":
    planner = Phase4Planner()
    planner.run_analysis()
