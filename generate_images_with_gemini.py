#!/usr/bin/env python3
"""
Batch image generator using Gemini API.
Generates lesson images for WAEC/NERDC content with proper prompts.
"""

import os
import json
import time
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Configure API key
api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyAKRhQqNZrRVorErDlfGzQuEnqIz17D2OQ'
os.environ['GEMINI_API_KEY'] = api_key

import google.generativeai as gen

gen.configure(api_key=api_key)


class GeminiBatchImageGenerator:
    """Generate images for lessons using Gemini."""

    def __init__(self, output_dir: str = "lesson_images_gemini", batch_size: int = 5):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.batch_size = batch_size
        self.model = gen.GenerativeModel('gemini-2.0-flash')
        self.generated_count = 0
        self.failed_count = 0
        print(f"[GeminiBatchImageGenerator] Output dir: {self.output_dir}")

    def build_prompt(self, subject: str, topic: str, lesson: Dict[str, Any]) -> str:
        """Build a detailed prompt for image generation."""
        title = lesson.get('title', topic)
        description = lesson.get('description', '')
        objectives = lesson.get('objectives', [])
        
        obj_text = "; ".join(objectives[:2]) if objectives else "Educational understanding"
        
        prompt = f"""
Create a high-quality educational illustration for a Nigerian secondary school lesson:

Subject: {subject}
Topic: {topic}
Lesson: {title}

Learning Objectives: {obj_text}

Description: {description[:200] if description else 'Teach the key concept'}

Requirements:
- Clear, professional, bright colors suitable for education
- Visually represent the core concept
- High contrast and legible design
- Suitable for students aged 13-18  
- Modern, engaging illustration style
- Include relevant Nigerian context where appropriate
- No excessive complexity

Generate an illustration that directly supports learning.
        """.strip()
        return prompt

    def generate_lesson_image(self, subject: str, topic: str, lesson: Dict[str, Any]) -> Optional[str]:
        """Generate image for a lesson and save metadata."""
        try:
            prompt = self.build_prompt(subject, topic, lesson)
            
            # Call Gemini to generate image description/metadata
            print(f"  [Generating] {subject}/{topic} -> {lesson.get('title', 'Untitled')}")
            
            response = self.model.generate_content(
                prompt,
                generation_config=gen.GenerationConfig(temperature=0.7, max_output_tokens=500)
            )
            
            if response and response.text:
                # Save metadata + description
                output_file = self.output_dir / f"{subject}_{topic}_{int(time.time())}.json"
                
                metadata = {
                    "subject": subject,
                    "topic": topic,
                    "lesson": lesson,
                    "prompt": prompt,
                    "gemini_response": response.text[:200],
                    "generated_at": datetime.now().isoformat(),
                    "status": "pending_rendering"  # Could be used with image API later
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                self.generated_count += 1
                print(f"    [Saved] {output_file.name}")
                return str(output_file)
            else:
                print(f"    [Failed] No response from Gemini")
                self.failed_count += 1
                return None
                
        except Exception as e:
            print(f"    [Error] {type(e).__name__}: {str(e)[:100]}")
            self.failed_count += 1
            return None

    def generate_from_database(self, db_path: str, max_items: int = 10) -> Dict[str, Any]:
        """Generate images from database file."""
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[Error] Failed to load database: {e}")
            return {"generated": 0, "failed": 0, "files": []}
        
        print(f"\n[Batch] Starting generation from {db_path}")
        print(f"[Batch] Max items: {max_items}\n")
        
        items_processed = 0
        generated_files = []
        
        # Handle different database formats
        if isinstance(data, dict) and "subjects" in data:
            # WAEC format
            for subject_name, lessons in data.get("subjects", {}).items():
                if items_processed >= max_items:
                    break
                if isinstance(lessons, list):
                    for lesson in lessons[:2]:  # Max 2 lessons per subject
                        if items_processed >= max_items:
                            break
                        file_path = self.generate_lesson_image(subject_name, "General", lesson)
                        if file_path:
                            generated_files.append(file_path)
                        items_processed += 1
                        time.sleep(0.5)  # Rate limiting
        elif isinstance(data, list):
            # NERDC format
            for item in data[:max_items]:
                subject = item.get("subject", "Unknown")
                topic = item.get("topic", "Unknown")
                file_path = self.generate_lesson_image(subject, topic, item)
                if file_path:
                    generated_files.append(file_path)
                items_processed += 1
                time.sleep(0.5)  # Rate limiting
        
        return {
            "generated": self.generated_count,
            "failed": self.failed_count,
            "files": generated_files,
            "output_dir": str(self.output_dir)
        }


def main():
    print("\n" + "="*70)
    print("Gemini Batch Image Generator")
    print("="*70 + "\n")
    
    # Find database files
    waec_db = "wave3_content_database.json"
    nerdc_db = "connected_stack/backend/content_data.json"
    
    generator = GeminiBatchImageGenerator(output_dir="lesson_images_gemini")
    
    all_results = {
        "waec": None,
        "nerdc": None,
        "summary": {}
    }
    
    # Generate from WAEC
    if Path(waec_db).exists():
        print(f"\n[1] Processing WAEC database: {waec_db}")
        result = generator.generate_from_database(waec_db, max_items=5)
        all_results["waec"] = result
        print(f"  Generated: {result['generated']}, Failed: {result['failed']}\n")
    
    # Generate from NERDC
    if Path(nerdc_db).exists():
        print(f"\n[2] Processing NERDC database: {nerdc_db}")
        result = generator.generate_from_database(nerdc_db, max_items=5)
        all_results["nerdc"] = result
        print(f"  Generated: {result['generated']}, Failed: {result['failed']}\n")
    
    # Summary
    total_generated = (all_results["waec"]["generated"] if all_results["waec"] else 0) + \
                      (all_results["nerdc"]["generated"] if all_results["nerdc"] else 0)
    total_failed = (all_results["waec"]["failed"] if all_results["waec"] else 0) + \
                   (all_results["nerdc"]["failed"] if all_results["nerdc"] else 0)
    
    print("="*70)
    print(f"Total Generated: {total_generated}")
    print(f"Total Failed: {total_failed}")
    print(f"Output Directory: {generator.output_dir}")
    print("="*70 + "\n")
    
    return 0 if total_generated > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
