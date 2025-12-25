#!/usr/bin/env python3
"""
Lesson JSON to Markdown Renderer
Converts structured lesson JSON to student-friendly Markdown textbooks
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

class LessonRenderer:
    """Render lesson JSON to markdown format"""

    def __init__(self, json_path: str, output_path: str = None):
        self.json_path = json_path
        with open(json_path, 'r', encoding='utf-8') as f:
            self.lesson = json.load(f)
        
        # Determine output path
        if output_path is None:
            subject = self.lesson['metadata']['subject']
            level = self.lesson['metadata']['level']
            lesson_num = self.lesson['metadata']['lesson'].zfill(2)
            lesson_title = self.lesson['metadata']['lesson_title'].lower().replace(' ', '_')
            output_path = f"content/ai_rendered/textbooks/{subject}/{level}/lesson_{lesson_num}_{lesson_title}.md"
        
        self.output_path = output_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    def render(self) -> str:
        """Generate markdown content"""
        md = []
        meta = self.lesson['metadata']

        # Title
        md.append(f"# {meta['lesson_title']}")
        md.append(f"\n**{meta['subject']} | {meta['level']} | Unit {meta['unit']}: {meta['unit_title']}**")
        md.append(f"\n---\n")

        # Metadata summary
        md.append("## Lesson Information\n")
        md.append(f"- **Duration**: {meta['duration_minutes']} minutes")
        md.append(f"- **Estimated Pages**: {meta['estimated_pages']}")
        md.append(f"- **NERDC Code**: {meta['curriculum_alignment']['nerdc_code']}")
        md.append(f"- **NERDC Description**: {meta['curriculum_alignment']['nerdc_description']}")
        md.append(f"- **WAEC Topic**: {meta['curriculum_alignment']['waec_topic']} ({meta['curriculum_alignment']['waec_weighting']})")
        md.append(f"- **Learning Level**: {meta['learning_level'].capitalize()}")

        # Learning objectives
        md.append("\n## Learning Objectives\n")
        md.append("By the end of this lesson, you will be able to:\n")
        for i, obj in enumerate(self.lesson['learning_objectives'], 1):
            md.append(f"{i}. {obj}")

        # Prerequisites
        md.append("\n## Prerequisites\n")
        md.append("Before starting this lesson, ensure you understand:\n")
        for prereq in self.lesson['prerequisites']:
            md.append(f"- {prereq}")

        # Content sections
        md.append("\n## Content\n")
        for section in self.lesson['content_sections']:
            md.append(f"\n### {section['section_id']}: {section['title']}")
            md.append(f"\n*Duration: {section['duration_minutes']} minutes*\n")
            md.append(f"{section['content']}\n")

        # Worked examples
        md.append("\n## Worked Examples\n")
        for example in self.lesson['worked_examples']:
            md.append(f"\n### Example {example['example_id']}: {example['title']}\n")
            md.append(f"**Context**: {example['context']}\n")
            md.append(f"**Problem**: {example['problem']}\n")
            md.append(f"**Solution**:\n```\n{example['solution']}\n```\n")
            md.append(f"**Skills Tested**: {', '.join(example['skills_tested'])}\n")

        # Practice problems
        md.append("\n## Practice Problems\n")
        
        # Basic tier
        basic_probs = [p for p in self.lesson['practice_problems'] if p['tier'] == 'basic']
        if basic_probs:
            md.append("\n### Basic Level\n")
            for prob in basic_probs:
                md.append(f"\n**{prob['problem_id']}**: {prob['problem']}\n")
                md.append(f"> **Answer**: {prob['answer']}\n")
                md.append(f"> **Explanation**: {prob['explanation']}\n")

        # Core tier
        core_probs = [p for p in self.lesson['practice_problems'] if p['tier'] == 'core']
        if core_probs:
            md.append("\n### Core Level\n")
            for prob in core_probs:
                md.append(f"\n**{prob['problem_id']}**: {prob['problem']}\n")
                md.append(f"> **Answer**: {prob['answer']}\n")
                md.append(f"> **Explanation**: {prob['explanation']}\n")

        # Challenge tier
        challenge_probs = [p for p in self.lesson['practice_problems'] if p['tier'] == 'challenge']
        if challenge_probs:
            md.append("\n### Challenge Level\n")
            for prob in challenge_probs:
                md.append(f"\n**{prob['problem_id']}**: {prob['problem']}\n")
                md.append(f"> **Answer**: {prob['answer']}\n")
                md.append(f"> **Explanation**: {prob['explanation']}\n")

        # Glossary
        md.append("\n## Glossary\n")
        for term in self.lesson['glossary']:
            md.append(f"\n**{term['term']}**: {term['definition']}")
            md.append(f"\n- *Example*: {term['example']}\n")

        # Assessment
        md.append("\n## Assessment\n")
        
        md.append("\n### Quick Checks (Understanding Check)\n")
        for i, check in enumerate(self.lesson['assessment']['quick_checks'], 1):
            md.append(f"{i}. {check}\n")

        if self.lesson['assessment'].get('end_of_lesson_quiz'):
            md.append("\n### End-of-Lesson Quiz\n")
            for i, q in enumerate(self.lesson['assessment']['end_of_lesson_quiz'], 1):
                md.append(f"\n**{i}. {q['question']}**\n")
                for option in q['options']:
                    md.append(f"- {option}\n")
                md.append(f"> **Correct Answer**: {q['correct']}\n")

        if self.lesson['assessment'].get('exam_style_questions'):
            md.append("\n### WAEC Exam-Style Questions\n")
            for i, q in enumerate(self.lesson['assessment']['exam_style_questions'], 1):
                md.append(f"\n**{i}. {q['question']}**\n")
                md.append(f"> **Answer Guide**: {q['answer_guide']}\n")

        # Summary
        md.append("\n## Summary\n")
        md.append(f"\nThis lesson covered the fundamentals of {meta['subject']} at {meta['level']} level.")
        md.append(f"\nKey topics included:\n")
        for section in self.lesson['content_sections']:
            md.append(f"- {section['section_id']}: {section['title']}\n")

        # Additional resources
        if self.lesson['resources'].get('visual_aids'):
            md.append("\n## Visual Aids & Resources\n")
            for aid in self.lesson['resources']['visual_aids']:
                md.append(f"\n- **{aid['title']}** ({aid['type']}): {aid['description']}\n")

        # Footer
        md.append("\n---\n")
        md.append(f"\n**Prepared for**: {meta['subject']} {meta['level']}\n")
        md.append(f"**WAEC Tags**: {', '.join(self.lesson['waec_tags'][:5])}...\n")
        md.append(f"**Learning Path**: Unit {meta['unit']} → {meta['unit_title']}\n")

        return '\n'.join(md)

    def save(self):
        """Save rendered markdown to file"""
        content = self.render()
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Rendered to: {self.output_path}")
        return self.output_path


def batch_render(source_dir: str = "content/ai_generated/textbooks", 
                output_dir: str = "content/ai_rendered/textbooks"):
    """Render all lesson JSON files in a directory"""
    
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return

    json_files = list(source_path.rglob("*.json"))
    print(f"🔍 Found {len(json_files)} lesson JSON files")

    rendered = []
    for json_file in json_files:
        try:
            renderer = LessonRenderer(str(json_file))
            renderer.save()
            rendered.append(str(renderer.output_path))
        except Exception as e:
            print(f"❌ Error rendering {json_file}: {e}")

    print(f"\n✅ Rendered {len(rendered)} lessons to Markdown")
    return rendered


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Render specific file
        json_path = sys.argv[1]
        renderer = LessonRenderer(json_path)
        renderer.save()
    else:
        # Batch render all lessons
        print("🚀 Batch rendering all lesson JSON files...\n")
        batch_render()
