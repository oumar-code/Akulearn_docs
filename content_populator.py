#!/usr/bin/env python3
"""
Content Population Script for Akulearn
Programmatically imports educational content into the platform

Usage:
    python content_populator.py --import sample_content.json
    python content_populator.py --generate-sample
    python content_populator.py --stats
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add the connected_stack/backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'connected_stack', 'backend'))

try:
    from content_service import content_service
except ImportError:
    print("ERROR: Could not import content_service. Make sure connected_stack/backend/content_service.py exists.")
    sys.exit(1)

class ContentPopulator:
    """Handles programmatic content population for Akulearn"""

    def __init__(self):
        self.content_count = 0
        self.error_count = 0

    def validate_content(self, content: Dict) -> List[str]:
        """Validate content structure and required fields"""
        errors = []

        required_fields = [
            'id', 'title', 'subject', 'topic', 'content_type',
            'difficulty', 'exam_board', 'content'
        ]

        for field in required_fields:
            if field not in content:
                errors.append(f"Missing required field: {field}")

        # Validate content type
        valid_types = ['study_guide', 'reference', 'summary', 'exercise']
        if content.get('content_type') not in valid_types:
            errors.append(f"Invalid content_type. Must be one of: {valid_types}")

        # Validate difficulty
        valid_difficulties = ['basic', 'intermediate', 'advanced']
        if content.get('difficulty') not in valid_difficulties:
            errors.append(f"Invalid difficulty. Must be one of: {valid_difficulties}")

        # Validate exam board
        valid_boards = ['WAEC', 'NECO', 'JAMB']
        if content.get('exam_board') not in valid_boards:
            errors.append(f"Invalid exam_board. Must be one of: {valid_boards}")

        return errors

    def import_from_json(self, json_file: str) -> Dict[str, int]:
        """Import content from JSON file"""
        print(f"📥 Importing content from {json_file}...")

        if not os.path.exists(json_file):
            print(f"❌ Error: File {json_file} not found")
            return {'imported': 0, 'errors': 1}

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content_list = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format in {json_file}: {e}")
            return {'imported': 0, 'errors': 1}

        imported = 0
        errors = 0

        for i, content_data in enumerate(content_list, 1):
            print(f"Processing content {i}/{len(content_list)}: {content_data.get('title', 'Unknown')}")

            # Validate content
            validation_errors = self.validate_content(content_data)
            if validation_errors:
                print(f"❌ Validation errors for content {content_data.get('id', 'unknown')}:")
                for error in validation_errors:
                    print(f"   - {error}")
                errors += 1
                continue

            # Add timestamps if not present
            if 'created_at' not in content_data:
                content_data['created_at'] = datetime.now().isoformat()
            if 'updated_at' not in content_data:
                content_data['updated_at'] = datetime.now().isoformat()

            # Import content
            try:
                success = content_service.add_content(content_data)
                if success:
                    print(f"✅ Successfully imported: {content_data['title']}")
                    imported += 1
                else:
                    print(f"❌ Failed to import: {content_data['title']}")
                    errors += 1
            except Exception as e:
                print(f"❌ Error importing {content_data.get('title', 'Unknown')}: {e}")
                errors += 1

        print(f"\n📊 Import Summary:")
        print(f"✅ Successfully imported: {imported}")
        print(f"❌ Errors: {errors}")

        return {'imported': imported, 'errors': errors}

    def generate_sample_content(self) -> Dict[str, int]:
        """Generate sample content for testing"""
        print("🎯 Generating sample content...")

        sample_content = [
            {
                "id": "sample_math_algebra_001",
                "title": "Introduction to Algebra",
                "subject": "Mathematics",
                "topic": "Algebra",
                "content_type": "study_guide",
                "difficulty": "basic",
                "exam_board": "WAEC",
                "content": "# Introduction to Algebra\n\n## What is Algebra?\nAlgebra is a branch of mathematics that deals with symbols and the rules for manipulating these symbols.\n\n## Basic Concepts\n- **Variables**: Letters that represent unknown values\n- **Constants**: Fixed values\n- **Expressions**: Combinations of variables and constants\n\n## Simple Equations\nAn equation is a statement that two expressions are equal.\n\nExample: 2x + 3 = 7\n\nTo solve: Subtract 3 from both sides: 2x = 4\nDivide by 2: x = 2",
                "estimated_read_time": 10,
                "prerequisites": [],
                "related_questions": [],
                "tags": ["algebra", "equations", "variables"],
                "author": "Mathematics Expert",
                "version": 1
            },
            {
                "id": "sample_physics_mechanics_001",
                "title": "Basic Mechanics Reference",
                "subject": "Physics",
                "topic": "Mechanics",
                "content_type": "reference",
                "difficulty": "basic",
                "exam_board": "WAEC",
                "content": "# Basic Mechanics\n\n## Newton's Laws\n1. **First Law**: An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an unbalanced force.\n2. **Second Law**: F = ma (Force equals mass times acceleration)\n3. **Third Law**: For every action, there is an equal and opposite reaction.\n\n## Key Formulas\n- **Speed**: v = d/t\n- **Acceleration**: a = (v-u)/t\n- **Force**: F = ma\n- **Weight**: W = mg",
                "estimated_read_time": 8,
                "prerequisites": [],
                "related_questions": [],
                "tags": ["physics", "mechanics", "newton", "laws"],
                "author": "Physics Expert",
                "version": 1
            }
        ]

        imported = 0
        errors = 0

        for content_data in sample_content:
            try:
                success = content_service.add_content(content_data)
                if success:
                    print(f"✅ Generated: {content_data['title']}")
                    imported += 1
                else:
                    print(f"❌ Failed to generate: {content_data['title']}")
                    errors += 1
            except Exception as e:
                print(f"❌ Error generating {content_data['title']}: {e}")
                errors += 1

        print(f"\n📊 Generation Summary:")
        print(f"✅ Successfully generated: {imported}")
        print(f"❌ Errors: {errors}")

        return {'generated': imported, 'errors': errors}

    def get_statistics(self) -> Dict[str, Any]:
        """Get content statistics"""
        try:
            return content_service.get_content_stats()
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}

def main():
    parser = argparse.ArgumentParser(description="Content Population Script for Akulearn")
    parser.add_argument('--import', dest='import_file', help='Import content from JSON file')
    parser.add_argument('--generate-sample', action='store_true', help='Generate sample content')
    parser.add_argument('--stats', action='store_true', help='Show content statistics')

    args = parser.parse_args()

    populator = ContentPopulator()

    if args.import_file:
        result = populator.import_from_json(args.import_file)
        if result['errors'] > 0:
            sys.exit(1)

    elif args.generate_sample:
        result = populator.generate_sample_content()
        if result['errors'] > 0:
            sys.exit(1)

    elif args.stats:
        stats = populator.get_statistics()
        if stats:
            print("\n📊 Content Statistics:")
            print(f"Total Content: {stats.get('total_content', 0)}")
            print("By Subject:")
            for subject, count in stats.get('subjects', {}).items():
                print(f"  - {subject}: {count}")
            print("By Content Type:")
            for ct, count in stats.get('content_types', {}).items():
                print(f"  - {ct}: {count}")
        else:
            print("❌ Could not retrieve statistics")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()