#!/usr/bin/env python3
"""Quick batch render for Wave 2 lessons"""

import os
import sys
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from render_lessons import LessonRenderer

# List of lesson JSON files to render
lessons = [
    "content/ai_generated/textbooks/Mathematics/SS1/lesson_02_indices.json",
    "content/ai_generated/textbooks/Mathematics/SS1/lesson_03_algebraic_expressions.json",
    "content/ai_generated/textbooks/Physics/SS1/lesson_02_motion.json",
    "content/ai_generated/textbooks/Physics/SS1/lesson_03_forces.json",
]

print("🎓 Batch Rendering Wave 2 Lessons...\n")

for json_file in lessons:
    try:
        if os.path.exists(json_file):
            renderer = LessonRenderer(json_file)
            renderer.save()
            print(f"✅ {json_file}")
        else:
            print(f"❌ File not found: {json_file}")
    except Exception as e:
        print(f"❌ Error rendering {json_file}: {e}")

print("\n✨ Batch render complete!")
