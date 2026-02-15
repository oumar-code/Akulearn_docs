#!/usr/bin/env python3
"""
CSV Content Importer for Akulearn
Semi-automated content creation with CSV import functionality
"""

import csv
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

# Add the connected_stack/backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'connected_stack', 'backend'))

try:
    from content_service import content_service
    from content_templates import CONTENT_TEMPLATES, generate_content_outline
except ImportError as e:
    print(f"ERROR: Could not import required modules: {e}")
    sys.exit(1)

class CSVContentImporter:
    """Import content from CSV files with validation and processing"""

    def __init__(self):
        self.stats = {
            'processed': 0,
            'imported': 0,
            'errors': 0,
            'skipped': 0
        }

    def validate_csv_row(self, row: Dict[str, str]) -> List[str]:
        """Validate a CSV row for required fields and data integrity"""
        errors = []

        # Required fields
        required_fields = ['title', 'subject', 'topic', 'content_type', 'difficulty', 'exam_board', 'content']
        for field in required_fields:
            value = row.get(field, '').strip() if row.get(field) else ''
            if not value:
                errors.append(f"Missing required field: {field}")

        # Validate content type
        valid_types = ['study_guide', 'reference', 'summary', 'exercise']
        content_type = row.get('content_type', '').strip() if row.get('content_type') else ''
        if content_type and content_type not in valid_types:
            errors.append(f"Invalid content_type '{content_type}'. Must be one of: {valid_types}")

        # Validate difficulty
        valid_difficulties = ['basic', 'intermediate', 'advanced']
        difficulty = row.get('difficulty', '').strip() if row.get('difficulty') else ''
        if difficulty and difficulty not in valid_difficulties:
            errors.append(f"Invalid difficulty '{difficulty}'. Must be one of: {valid_difficulties}")

        # Validate exam board
        valid_boards = ['WAEC', 'NECO', 'JAMB']
        exam_board = row.get('exam_board', '').strip() if row.get('exam_board') else ''
        if exam_board and exam_board not in valid_boards:
            errors.append(f"Invalid exam_board '{exam_board}'. Must be one of: {valid_boards}")

        # Validate estimated_read_time
        if row.get('estimated_read_time'):
            try:
                int(row['estimated_read_time'])
            except ValueError:
                errors.append(f"Invalid estimated_read_time '{row['estimated_read_time']}'. Must be a number.")

        return errors

    def process_csv_list_field(self, field_value: str) -> List[str]:
        """Process CSV fields that contain lists (comma-separated)"""
        if not field_value or field_value.strip() == '':
            return []

        # Split by comma and clean up whitespace
        items = [item.strip() for item in field_value.split(',')]
        return [item for item in items if item]  # Remove empty items

    def import_from_csv(self, csv_file: str, skip_errors: bool = False) -> Dict[str, Any]:
        """Import content from CSV file"""
        print(f"📥 Importing content from {csv_file}...")

        if not os.path.exists(csv_file):
            error_msg = f"❌ Error: File {csv_file} not found"
            print(error_msg)
            return {'success': False, 'error': error_msg}

        imported_items = []
        errors = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                # Try to detect delimiter, but fall back to comma
                try:
                    sample = f.read(1024)
                    f.seek(0)
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter
                except (csv.Error, UnicodeDecodeError):
                    # Fall back to comma delimiter
                    delimiter = ','
                    f.seek(0)

                reader = csv.DictReader(f, delimiter=delimiter)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
                    self.stats['processed'] += 1
                    print(f"Processing row {row_num}: {row.get('title', 'Unknown')}")

                    # Validate row
                    validation_errors = self.validate_csv_row(row)
                    if validation_errors:
                        error_msg = f"Row {row_num} validation errors: {'; '.join(validation_errors)}"
                        print(f"❌ {error_msg}")
                        errors.append(error_msg)
                        self.stats['errors'] += 1

                        if not skip_errors:
                            continue
                        else:
                            print("⚠️  Skipping invalid row due to skip_errors=True")
                            self.stats['skipped'] += 1
                            continue

                    # Process list fields
                    prerequisites = self.process_csv_list_field(row.get('prerequisites', ''))
                    related_questions = self.process_csv_list_field(row.get('related_questions', ''))
                    tags = self.process_csv_list_field(row.get('tags', ''))

                    # Generate unique ID
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    content_id = f"{row['subject'].lower().replace(' ', '_')}_{row['topic'].lower().replace(' ', '_')}_{row['content_type']}_{timestamp}"

                    # Create content object
                    content = {
                        'id': content_id,
                        'title': row.get('title', '').strip(),
                        'subject': row.get('subject', '').strip(),
                        'topic': row.get('topic', '').strip(),
                        'content_type': row.get('content_type', '').strip(),
                        'difficulty': row.get('difficulty', '').strip(),
                        'exam_board': row.get('exam_board', '').strip(),
                        'content': row.get('content', '').strip(),
                        'estimated_read_time': int(row.get('estimated_read_time') or 15),
                        'prerequisites': prerequisites,
                        'related_questions': related_questions,
                        'tags': tags if tags else [row.get('topic', '').lower(), row.get('subject', '').lower()],
                        'author': row.get('author', 'CSV Import').strip(),
                        'version': 1,
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }

                    # Import content
                    try:
                        success = content_service.add_content(content)
                        if success:
                            print(f"✅ Successfully imported: {content['title']}")
                            imported_items.append(content)
                            self.stats['imported'] += 1
                        else:
                            error_msg = f"Failed to import: {content['title']}"
                            print(f"❌ {error_msg}")
                            errors.append(error_msg)
                            self.stats['errors'] += 1
                    except Exception as e:
                        error_msg = f"Error importing {content['title']}: {str(e)}"
                        print(f"❌ {error_msg}")
                        errors.append(error_msg)
                        self.stats['errors'] += 1

        except Exception as e:
            error_msg = f"Error reading CSV file: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}

        # Print summary
        print(f"\n📊 Import Summary:")
        print(f"📄 Total rows processed: {self.stats['processed']}")
        print(f"✅ Successfully imported: {self.stats['imported']}")
        print(f"❌ Errors: {self.stats['errors']}")
        if skip_errors:
            print(f"⚠️  Skipped: {self.stats['skipped']}")

        return {
            'success': True,
            'stats': self.stats,
            'imported_items': imported_items,
            'errors': errors
        }

    def generate_csv_template(self, output_file: str = 'content_template.csv'):
        """Generate a CSV template file for content creation"""
        template_rows = [
            {
                'title': 'Introduction to Quadratic Equations',
                'subject': 'Mathematics',
                'topic': 'Algebra',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'exam_board': 'WAEC',
                'content': '# Quadratic Equations\n\n## What are quadratic equations?\nA quadratic equation is any equation that can be written as ax² + bx + c = 0.',
                'estimated_read_time': '20',
                'prerequisites': 'basic_algebra, linear_equations',
                'related_questions': 'waec_math_2020_q1, waec_math_2020_q2',
                'tags': 'algebra, quadratic, equations, mathematics',
                'author': 'Mathematics Expert'
            },
            {
                'title': 'Electricity Fundamentals Reference',
                'subject': 'Physics',
                'topic': 'Electricity',
                'content_type': 'reference',
                'difficulty': 'basic',
                'exam_board': 'WAEC',
                'content': '# Basic Electricity\n\n## Key Concepts\n- **Current**: Flow of electric charge\n- **Voltage**: Electric potential difference\n- **Resistance**: Opposition to current flow',
                'estimated_read_time': '15',
                'prerequisites': '',
                'related_questions': 'waec_physics_2020_q5',
                'tags': 'electricity, physics, current, voltage',
                'author': 'Physics Expert'
            }
        ]

        fieldnames = ['title', 'subject', 'topic', 'content_type', 'difficulty', 'exam_board',
                     'content', 'estimated_read_time', 'prerequisites', 'related_questions',
                     'tags', 'author']

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(template_rows)

            print(f"✅ CSV template generated: {output_file}")
            print("📋 Template includes sample rows for Mathematics and Physics content")
            print("🔧 Edit the template and use: python csv_importer.py --import your_file.csv")

        except Exception as e:
            print(f"❌ Error generating template: {e}")

    def create_bulk_content_from_template(self, template_name: str, csv_data: str) -> List[Dict[str, Any]]:
        """Create multiple content items from a template using CSV data"""
        if template_name not in CONTENT_TEMPLATES:
            print(f"❌ Template '{template_name}' not found")
            return []

        # Parse CSV data (assuming it's tab-separated for inline use)
        lines = csv_data.strip().split('\n')
        if len(lines) < 2:
            print("❌ CSV data must have at least a header row and one data row")
            return []

        # Simple CSV parsing (for tab-separated data)
        headers = [h.strip() for h in lines[0].split('\t')]
        content_items = []

        for line_num, line in enumerate(lines[1:], start=2):
            if not line.strip():
                continue

            values = [v.strip() for v in line.split('\t')]
            if len(values) != len(headers):
                print(f"⚠️  Row {line_num}: Expected {len(headers)} columns, got {len(values)}")
                continue

            row_data = dict(zip(headers, values))

            # Generate content using template
            outline = generate_content_outline(template_name, row_data.get('specific_topic', ''))

            if outline:
                # Merge CSV data with template structure
                content_item = {
                    'id': f"{outline['subject'].lower()}_{outline['topic'].lower()}_{outline['content_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'title': row_data.get('title', outline.get('title', f"Generated {template_name}")),
                    'subject': outline['subject'],
                    'topic': outline['topic'],
                    'content_type': outline['content_type'],
                    'difficulty': outline['difficulty'],
                    'exam_board': outline['exam_board'],
                    'content': self._generate_content_from_outline(outline, row_data),
                    'estimated_read_time': int(row_data.get('estimated_read_time', '15')),
                    'prerequisites': self.process_csv_list_field(row_data.get('prerequisites', '')),
                    'related_questions': self.process_csv_list_field(row_data.get('related_questions', '')),
                    'tags': self.process_csv_list_field(row_data.get('tags', '')),
                    'author': row_data.get('author', 'Bulk Generator'),
                    'version': 1,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }

                content_items.append(content_item)
                print(f"✅ Generated content: {content_item['title']}")

        return content_items

    def _generate_content_from_outline(self, outline: Dict[str, Any], data: Dict[str, str]) -> str:
        """Generate content markdown from template outline and data"""
        content_parts = []

        for section_name, section_config in outline['structure'].items():
            section_type = section_config['type']

            # Get content for this section
            section_content = data.get(section_name, outline.get('examples', {}).get(section_name, ''))

            if section_type == 'heading':
                content_parts.append(f"## {section_content}")
            elif section_type in ['bullet_list', 'list', 'principle_list']:
                content_parts.append(section_content)
            elif section_type == 'definition_list':
                content_parts.append(section_content)
            elif section_type == 'numbered_examples':
                content_parts.append(section_content)
            elif section_type == 'formula_box':
                content_parts.append(f"```\n{section_content}\n```")
            elif section_type == 'summary_quote':
                content_parts.append(f"> {section_content}")
            else:
                content_parts.append(section_content)

            content_parts.append("")  # Add spacing

        return "\n".join(content_parts)

def main():
    """Main CSV import interface"""
    parser = argparse.ArgumentParser(description="CSV Content Importer for Akulearn")
    parser.add_argument('--import', dest='import_file', help='Import content from CSV file')
    parser.add_argument('--template', action='store_true', help='Generate CSV template file')
    parser.add_argument('--skip-errors', action='store_true', help='Continue importing despite validation errors')
    parser.add_argument('--bulk-generate', nargs=2, metavar=('TEMPLATE', 'CSV_DATA'),
                       help='Generate content from template using inline CSV data')

    args = parser.parse_args()

    importer = CSVContentImporter()

    if args.import_file:
        result = importer.import_from_csv(args.import_file, skip_errors=args.skip_errors)
        if not result.get('success', False):
            sys.exit(1)

    elif args.template:
        importer.generate_csv_template()

    elif args.bulk_generate:
        template_name, csv_data = args.bulk_generate
        content_items = importer.create_bulk_content_from_template(template_name, csv_data)

        if content_items:
            # Save generated content
            output_file = f"bulk_generated_{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(content_items, f, indent=2, ensure_ascii=False)
            print(f"✅ Generated content saved to {output_file}")

            # Import to database
            imported = 0
            for item in content_items:
                if content_service.add_content(item):
                    imported += 1

            print(f"✅ Imported {imported}/{len(content_items)} items to database")

    else:
        print("🎯 Akulearn CSV Content Importer")
        print("=" * 40)
        print("Usage examples:")
        print("  python csv_importer.py --template                    # Generate CSV template")
        print("  python csv_importer.py --import content.csv         # Import from CSV")
        print("  python csv_importer.py --import content.csv --skip-errors  # Skip validation errors")
        print("\nCSV Format Requirements:")
        print("  Required columns: title, subject, topic, content_type, difficulty, exam_board, content")
        print("  Optional columns: estimated_read_time, prerequisites, related_questions, tags, author")
        print("  List fields (prerequisites, related_questions, tags) should be comma-separated")

if __name__ == "__main__":
    main()