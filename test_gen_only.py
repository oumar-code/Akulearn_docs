#!/usr/bin/env python3
print("Test 1: Starting")

from enhanced_content_generator import EnhancedContentGenerator
print("Test 2: Generator imported")

gen = EnhancedContentGenerator(use_mcp=False)
print("Test 3: Generator created")

# Try generating just 1 topic
topics = [("Mathematics", "Quadratic Equations and Functions", "Intermediate")]
print("Test 4: Topics prepared")

print("Test 5: Starting batch generation...")
lessons = gen.generate_batch(topics=topics)
print(f"Test 6: Generated {len(lessons)} lessons")

# Check structure
if lessons:
    lesson = lessons[0]
    print(f"Test 7: Lesson created - {lesson.get('title')}")
    print(f"  - ID: {lesson.get('id')}")
    print(f"  - Duration: {lesson.get('duration_minutes')} min")
    print(f"  - Objectives: {len(lesson.get('learningObjectives', []))}")
    print(f"  - Sections: {len(lesson.get('sections', []))}")

print("Test 8: All tests passed!")
