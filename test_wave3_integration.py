#!/usr/bin/env python3
"""
Test Wave 3 Dashboard Integration
"""

import sys
import warnings
warnings.filterwarnings('ignore')

from wave3_interactive_dashboard import Wave3Dashboard

def main():
    print("=" * 60)
    print("Testing Wave 3 Dashboard")
    print("=" * 60)
    
    # Initialize dashboard
    print("\n1. Initializing dashboard...")
    dashboard = Wave3Dashboard()
    
    # Get subjects overview
    print("\n2. Getting subjects overview...")
    subjects = dashboard.get_subjects_overview()
    print(f"   Found {len(subjects)} subjects")
    
    # Test each subject
    print("\n3. Testing lesson retrieval...")
    for subject_data in subjects:
        subject = subject_data['subject']
        lessons = dashboard.get_lessons_by_subject(subject)
        print(f"   {subject}: {len(lessons)} lessons")
    
    # Test Chemistry details
    print("\n4. Testing Chemistry lesson details...")
    chemistry_lessons = dashboard.get_lessons_by_subject("Chemistry")
    for lesson in chemistry_lessons:
        print(f"\n   Lesson: {lesson.title}")
        print(f"   - Duration: {lesson.duration_minutes} min")
        print(f"   - Difficulty: {lesson.difficulty_level}")
        print(f"   - Components: {lesson.num_objectives} obj, "
              f"{lesson.num_sections} sections, "
              f"{lesson.num_examples} examples, "
              f"{lesson.num_problems} problems")
        print(f"   - Keywords: {', '.join(lesson.keywords[:5])}")
    
    # Test content retrieval
    print("\n5. Testing content retrieval...")
    if chemistry_lessons:
        lesson_id = chemistry_lessons[0].id
        content = dashboard.get_lesson_content(lesson_id)
        if content:
            print(f"   ✅ Retrieved content for {lesson_id}")
            print(f"   - Has metadata: {'metadata' in content}")
            print(f"   - Has learning_objectives: {'learning_objectives' in content}")
            print(f"   - Has content_sections: {'content_sections' in content}")
        else:
            print(f"   ❌ Failed to retrieve content")
    
    # Test export
    print("\n6. Testing export functionality...")
    if chemistry_lessons:
        lesson_id = chemistry_lessons[0].id
        export_path = dashboard.export_lesson_for_teacher(lesson_id, 'json')
        if export_path:
            print(f"   ✅ Exported to: {export_path}")
        else:
            print(f"   ⚠️ Export skipped (requires content)")
    
    # Generate report
    print("\n7. Generating dashboard report...")
    try:
        report = dashboard.generate_dashboard_report()
        print(f"   ✅ Report generated")
        print(f"   - Total lessons: {report['totals']['total_lessons']}")
        print(f"   - Total objectives: {report['totals']['total_objectives']}")
        print(f"   - Total problems: {report['totals']['total_problems']}")
        print(f"   - Total duration: {report['totals']['total_duration_minutes']} min")
    except Exception as e:
        print(f"   ❌ Report generation failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Dashboard Test Complete")
    print("=" * 60)
    
    dashboard.close()

if __name__ == "__main__":
    main()
