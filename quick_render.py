#!/usr/bin/env python3
from render_lessons import LessonRenderer
import os

json_files = [
    "content/ai_generated/textbooks/Mathematics/SS1/lesson_02_indices.json",
    "content/ai_generated/textbooks/Mathematics/SS1/lesson_03_algebraic_expressions.json",
    "content/ai_generated/textbooks/Physics/SS1/lesson_02_motion.json",
    "content/ai_generated/textbooks/Physics/SS1/lesson_03_forces.json",
]

print("📚 Rendering Wave 2 Lessons...\n")
for json_file in json_files:
    if os.path.exists(json_file):
        try:
            renderer = LessonRenderer(json_file)
            renderer.save()
        except Exception as e:
            print(f"❌ Error: {json_file} - {str(e)[:100]}")
    else:
        print(f"❌ Not found: {json_file}")

print("\n✨ Complete!")
