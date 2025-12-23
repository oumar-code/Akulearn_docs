#!/usr/bin/env python3
"""
Akulearn Content Creation Strategies Implementation
Comprehensive system for manual, semi-automated, and automated content creation
"""

import json
import os
import sys
import csv
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse
import re
from pathlib import Path

# Add the connected_stack/backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'connected_stack', 'backend'))

try:
    from content_service import content_service
    from content_templates import CONTENT_TEMPLATES, generate_content_outline
except ImportError as e:
    print(f"ERROR: Could not import required modules: {e}")
    sys.exit(1)

class ContentCreationStrategies:
    """
    Comprehensive content creation system implementing three phases:
    1. Manual Content Creation
    2. Semi-Automated Content Creation
    3. Automated Content Processing
    """

    def __init__(self):
        self.templates = CONTENT_TEMPLATES
        self.stats = {
            'manual_created': 0,
            'csv_imported': 0,
            'auto_generated': 0,
            'ai_enhanced': 0,
            'external_integrated': 0,
            'errors': 0
        }

    # ============================================================================
    # PHASE 1: MANUAL CONTENT CREATION
    # ============================================================================

    def manual_content_creation_wizard(self):
        """Interactive manual content creation with templates"""
        print("🎯 PHASE 1: Manual Content Creation Wizard")
        print("=" * 50)

        # Show available templates
        print("\n📋 Available Templates:")
        templates_list = list(self.templates.keys())
        for i, template_name in enumerate(templates_list, 1):
            template = self.templates[template_name]
            print(f"{i}. {template_name}")
            print(f"   {template['subject']} - {template['topic']} ({template['content_type']})")

        # Get template choice
        while True:
            try:
                choice = input("\nSelect template (number or name): ").strip()
                if choice.isdigit():
                    template_name = templates_list[int(choice) - 1]
                else:
                    template_name = choice

                if template_name in self.templates:
                    break
                else:
                    print("❌ Invalid template selection")
            except (ValueError, IndexError):
                print("❌ Invalid input")

        template = self.templates[template_name]
        print(f"\n✅ Selected: {template['subject']} - {template['topic']}")

        # Collect content data
        content_data = self._collect_manual_content_data(template)

        # Generate content
        content = self._generate_content_from_template(template_name, content_data)

        if content:
            # Save options
            self._save_manual_content(content)

        return content

    def _collect_manual_content_data(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Collect content data through interactive prompts"""
        data = {}

        # Basic metadata
        data['title'] = input(f"Title: ").strip()
        data['author'] = input("Author [Content Creator]: ").strip() or "Content Creator"
        data['specific_topic'] = input(f"Specific topic within {template['topic']}: ").strip()

        # Read time
        while True:
            read_time = input("Estimated read time (minutes) [15]: ").strip()
            if not read_time:
                data['estimated_read_time'] = 15
                break
            try:
                data['estimated_read_time'] = int(read_time)
                break
            except ValueError:
                print("❌ Please enter a valid number")

        # Tags and prerequisites
        tags_input = input("Tags (comma-separated): ").strip()
        if tags_input:
            data['tags'] = [tag.strip() for tag in tags_input.split(',')]

        prereqs = input("Prerequisites (comma-separated, optional): ").strip()
        if prereqs:
            data['prerequisites'] = [p.strip() for p in prereqs.split(',')]

        # Content sections based on template structure
        print(f"\n📝 Content Sections for {template['content_type'].replace('_', ' ')}:")
        for section_name, section_config in template.get('structure', {}).items():
            required = section_config.get('required', False)
            description = section_config.get('description', '')

            print(f"\n{section_name.upper()} {'(Required)' if required else '(Optional)'}")
            if description:
                print(f"Description: {description}")

            if 'examples' in template and section_name in template['examples']:
                example = template['examples'][section_name]
                print(f"Example: {example[:100]}{'...' if len(example) > 100 else ''}")

            # Get user input
            if required:
                content = input(f"Enter {section_name} content: ").strip()
                while not content:
                    print("❌ This section is required")
                    content = input(f"Enter {section_name} content: ").strip()
                data[section_name] = content
            else:
                content = input(f"Enter {section_name} content (or press Enter to skip): ").strip()
                if content:
                    data[section_name] = content

        return data

    def _generate_content_from_template(self, template_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate content from template and data"""
        if template_name not in self.templates:
            print(f"❌ Template '{template_name}' not found")
            return None

        template = self.templates[template_name]

        # Generate content ID
        content_id = f"{template['subject'].lower()}_{template['topic'].lower()}_{template['content_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Build content from template structure
        content_parts = []

        # Title
        title = data.get('title', template.get('title_template', 'Generated Content').format(
            topic=template['topic'],
            specific_topic=data.get('specific_topic', '')
        ))
        content_parts.append(f"# {title}\n")

        # Generate content based on template structure
        for section_name, section_config in template.get('structure', {}).items():
            if section_name in data:
                section_content = data[section_name]

                # Format based on section type
                section_type = section_config.get('type', 'paragraph')

                if section_type == 'heading':
                    content_parts.append(f"## {section_content}")
                elif section_type == 'bullet_list':
                    content_parts.append(f"## {section_name.replace('_', ' ').title()}\n{section_content}")
                elif section_type == 'numbered_examples':
                    content_parts.append(f"## {section_name.replace('_', ' ').title()}\n{section_content}")
                elif section_type == 'formula_box':
                    content_parts.append(f"## {section_name.replace('_', ' ').title()}\n\n```math\n{section_content}\n```")
                elif section_type == 'summary_quote':
                    content_parts.append(f"> {section_content}")
                else:
                    content_parts.append(f"## {section_name.replace('_', ' ').title()}\n\n{section_content}")

                content_parts.append("")  # Add spacing

        full_content = "\n".join(content_parts)

        # Create content object
        content = {
            "id": content_id,
            "title": title,
            "subject": template["subject"],
            "topic": template["topic"],
            "content_type": template["content_type"],
            "difficulty": template["difficulty"],
            "exam_board": template["exam_board"],
            "content": full_content,
            "estimated_read_time": data.get("estimated_read_time", 15),
            "prerequisites": data.get("prerequisites", []),
            "related_questions": data.get("related_questions", []),
            "tags": data.get("tags", [template["topic"].lower(), template["subject"].lower()]),
            "author": data.get("author", "Content Creator"),
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "creation_method": "manual"
        }

        print("✅ Content generated successfully!")
        return content

    def _save_manual_content(self, content: Dict[str, Any]):
        """Save manually created content with options"""
        print(f"\n💾 Content: {content['title']}")

        # Save to database
        save_db = input("Save to database? (y/n): ").strip().lower()
        if save_db == 'y':
            success = content_service.add_content(content)
            if success:
                print("✅ Saved to database")
                self.stats['manual_created'] += 1
            else:
                print("❌ Failed to save to database")

        # Export to JSON
        export_json = input("Export to JSON file? (y/n): ").strip().lower()
        if export_json == 'y':
            filename = f"{content['id']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([content], f, indent=2, ensure_ascii=False)
            print(f"✅ Exported to {filename}")

    # ============================================================================
    # PHASE 1B: SEMI-AUTOMATED CONTENT CREATION
    # ============================================================================

    def csv_bulk_import(self, csv_file: str, skip_errors: bool = False) -> Dict[str, Any]:
        """Enhanced CSV import with validation and bulk processing"""
        print("📊 PHASE 1B: Semi-Automated CSV Import")
        print("=" * 50)

        if not os.path.exists(csv_file):
            return {'success': False, 'error': f'File {csv_file} not found'}

        imported_items = []
        errors = []

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                # Detect delimiter
                sample = f.read(1024)
                f.seek(0)
                try:
                    import csv as csv_module
                    sniffer = csv_module.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter
                except:
                    delimiter = ','

                reader = csv.DictReader(f, delimiter=delimiter)

                for row_num, row in enumerate(reader, start=2):
                    print(f"Processing row {row_num}: {row.get('title', 'Unknown')}")

                    # Validate and process row
                    content = self._process_csv_row(row, row_num)
                    if content:
                        # Save to database
                        success = content_service.add_content(content)
                        if success:
                            imported_items.append(content)
                            self.stats['csv_imported'] += 1
                            print(f"✅ Imported: {content['title']}")
                        else:
                            errors.append(f"Failed to save: {content['title']}")
                    else:
                        if not skip_errors:
                            errors.append(f"Row {row_num}: Validation failed")

        except Exception as e:
            return {'success': False, 'error': str(e)}

        return {
            'success': True,
            'imported': len(imported_items),
            'errors': len(errors),
            'items': imported_items
        }

    def _process_csv_row(self, row: Dict[str, str], row_num: int) -> Optional[Dict[str, Any]]:
        """Process a single CSV row into content"""
        # Required fields validation
        required = ['title', 'subject', 'topic', 'content_type', 'difficulty', 'exam_board', 'content']
        for field in required:
            if not row.get(field, '').strip():
                print(f"❌ Row {row_num}: Missing required field '{field}'")
                return None

        # Validate content type, difficulty, exam board
        if row['content_type'] not in ['study_guide', 'reference', 'summary', 'exercise']:
            print(f"❌ Row {row_num}: Invalid content_type '{row['content_type']}'")
            return None

        if row['difficulty'] not in ['basic', 'intermediate', 'advanced']:
            print(f"❌ Row {row_num}: Invalid difficulty '{row['difficulty']}'")
            return None

        if row['exam_board'] not in ['WAEC', 'NECO', 'JAMB']:
            print(f"❌ Row {row_num}: Invalid exam_board '{row['exam_board']}'")
            return None

        # Generate ID
        content_id = f"{row['subject'].lower().replace(' ', '_')}_{row['topic'].lower().replace(' ', '_')}_{row['content_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Process list fields
        def process_list_field(field_value: str) -> List[str]:
            if not field_value:
                return []
            return [item.strip() for item in field_value.split(',') if item.strip()]

        content = {
            'id': content_id,
            'title': row['title'].strip(),
            'subject': row['subject'].strip(),
            'topic': row['topic'].strip(),
            'content_type': row['content_type'].strip(),
            'difficulty': row['difficulty'].strip(),
            'exam_board': row['exam_board'].strip(),
            'content': row['content'].strip(),
            'estimated_read_time': int(row.get('estimated_read_time') or 15),
            'prerequisites': process_list_field(row.get('prerequisites', '')),
            'related_questions': process_list_field(row.get('related_questions', '')),
            'tags': process_list_field(row.get('tags', '')) or [row['topic'].lower(), row['subject'].lower()],
            'author': row.get('author', 'CSV Import').strip(),
            'version': 1,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'creation_method': 'csv_import'
        }

        return content

    def generate_csv_template(self, output_file: str = 'content_import_template.csv'):
        """Generate an enhanced CSV template"""
        template_data = [
            {
                'title': 'Introduction to Quadratic Equations',
                'subject': 'Mathematics',
                'topic': 'Algebra',
                'content_type': 'study_guide',
                'difficulty': 'intermediate',
                'exam_board': 'WAEC',
                'content': '# Quadratic Equations\n\n## What are quadratic equations?\n\nA quadratic equation is any equation that can be written in the form ax² + bx + c = 0.\n\n## Solving Methods\n\n### 1. Factoring\n(x + 2)(x - 3) = 0\n\n### 2. Quadratic Formula\nx = [-b ± √(b² - 4ac)] / 2a\n\n### 3. Completing the Square\nAdd (b/2)² to both sides',
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
                'content': '# Basic Electricity\n\n## Key Concepts\n\n- **Current (I)**: Rate of flow of electric charge, measured in Amperes (A)\n- **Voltage (V)**: Electric potential difference, measured in Volts (V)\n- **Resistance (R)**: Opposition to current flow, measured in Ohms (Ω)\n- **Power (P)**: Rate of energy transfer, measured in Watts (W)\n\n## Important Formulas\n\n- V = IR (Ohm\'s Law)\n- P = VI (Power)\n- P = I²R (Power in terms of current)\n- P = V²/R (Power in terms of voltage)',
                'estimated_read_time': '15',
                'prerequisites': '',
                'related_questions': 'waec_physics_2020_q5, waec_physics_2020_q6',
                'tags': 'electricity, physics, current, voltage, resistance, power',
                'author': 'Physics Expert'
            }
        ]

        fieldnames = ['title', 'subject', 'topic', 'content_type', 'difficulty', 'exam_board',
                     'content', 'estimated_read_time', 'prerequisites', 'related_questions',
                     'tags', 'author']

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(template_data)

        print(f"✅ Enhanced CSV template generated: {output_file}")
        print("📋 Template includes sample content for Mathematics and Physics")
        print("🔧 Edit the template and use: python content_strategies.py --csv-import your_file.csv")

    def json_bulk_import(self, json_file: str) -> Dict[str, Any]:
        """Import content from JSON file"""
        print("📄 PHASE 1B: JSON Bulk Import")

        if not os.path.exists(json_file):
            return {'success': False, 'error': f'File {json_file} not found'}

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                data = [data]

            imported_items = []
            for item in data:
                # Validate required fields
                required = ['title', 'subject', 'topic', 'content_type', 'difficulty', 'exam_board', 'content']
                if all(key in item for key in required):
                    # Add metadata if missing
                    if 'id' not in item:
                        item['id'] = f"{item['subject'].lower()}_{item['topic'].lower()}_{item['content_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    if 'created_at' not in item:
                        item['created_at'] = datetime.now().isoformat()
                    if 'updated_at' not in item:
                        item['updated_at'] = datetime.now().isoformat()
                    if 'creation_method' not in item:
                        item['creation_method'] = 'json_import'

                    success = content_service.add_content(item)
                    if success:
                        imported_items.append(item)
                        self.stats['csv_imported'] += 1
                        print(f"✅ Imported: {item['title']}")
                    else:
                        print(f"❌ Failed to import: {item['title']}")
                else:
                    print(f"❌ Invalid item: missing required fields")

            return {
                'success': True,
                'imported': len(imported_items),
                'items': imported_items
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    # ============================================================================
    # PHASE 1C: AUTOMATED CONTENT PROCESSING
    # ============================================================================

    def automated_content_generation(self, subject: str, topic: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate content automatically using templates and patterns"""
        print("🤖 PHASE 1C: Automated Content Generation")
        print("=" * 50)
        print(f"Generating {count} content items for {subject} - {topic}")

        generated_content = []

        # Find appropriate template
        template_key = self._find_best_template(subject, topic)
        if not template_key:
            print(f"❌ No suitable template found for {subject}/{topic}")
            return []

        template = self.templates[template_key]

        # Generate multiple content items
        for i in range(count):
            try:
                content = self._generate_automated_content(template, subject, topic, i + 1)
                if content:
                    success = content_service.add_content(content)
                    if success:
                        generated_content.append(content)
                        self.stats['auto_generated'] += 1
                        print(f"✅ Generated: {content['title']}")
                    else:
                        print(f"❌ Failed to save: {content['title']}")
            except Exception as e:
                print(f"❌ Error generating content {i+1}: {e}")

        return generated_content

    def _find_best_template(self, subject: str, topic: str) -> Optional[str]:
        """Find the best template for automated generation"""
        subject_lower = subject.lower()
        topic_lower = topic.lower()

        # Exact match
        for key, template in self.templates.items():
            if (template["subject"].lower() == subject_lower and
                template["topic"].lower() == topic_lower):
                return key

        # Subject match
        subject_templates = [k for k, t in self.templates.items()
                           if t["subject"].lower() == subject_lower]
        if subject_templates:
            return subject_templates[0]

        return None

    def _generate_automated_content(self, template: Dict[str, Any], subject: str, topic: str, index: int) -> Optional[Dict[str, Any]]:
        """Generate a single automated content item"""
        # Generate unique ID
        content_id = f"{subject.lower()}_{topic.lower()}_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{index}"

        # Generate title variations
        title_variations = [
            f"Understanding {topic} - Part {index}",
            f"{topic} Fundamentals - Module {index}",
            f"Mastering {topic} - Lesson {index}",
            f"{topic} Concepts - Section {index}",
            f"Exploring {topic} - Chapter {index}"
        ]
        title = title_variations[(index - 1) % len(title_variations)]

        # Generate content based on template
        content_parts = [f"# {title}\n"]

        # Add sections based on template structure
        for section_name, section_config in template.get('structure', {}).items():
            if section_config.get('required', False):
                section_title = section_name.replace('_', ' ').title()
                content_parts.append(f"## {section_title}\n")

                # Generate content based on section type
                section_content = self._generate_section_content(section_name, section_config, subject, topic)
                content_parts.append(section_content + "\n")

        full_content = "\n".join(content_parts)

        content = {
            "id": content_id,
            "title": title,
            "subject": subject,
            "topic": topic,
            "content_type": template["content_type"],
            "difficulty": template["difficulty"],
            "exam_board": template["exam_board"],
            "content": full_content,
            "estimated_read_time": 15,
            "prerequisites": [],
            "related_questions": [],
            "tags": [topic.lower(), subject.lower(), "auto_generated"],
            "author": "Automated Content Generator",
            "version": 1,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "creation_method": "automated"
        }

        return content

    def _generate_section_content(self, section_name: str, section_config: Dict[str, Any], subject: str, topic: str) -> str:
        """Generate content for a specific section"""
        section_type = section_config.get('type', 'paragraph')

        if section_type == 'heading':
            return f"### {topic} Overview"
        elif section_type == 'bullet_list':
            return f"- Key concept 1 about {topic}\n- Key concept 2 about {topic}\n- Key concept 3 about {topic}"
        elif section_type == 'definition_list':
            return f"**Definition 1**: Explanation of concept in {topic}\n\n**Definition 2**: Another important concept"
        elif section_type == 'numbered_examples':
            return "1. Example problem 1\n2. Example problem 2\n3. Example problem 3"
        elif section_type == 'formula_box':
            return f"```\n# Sample formula for {topic}\nF = ma  # Force equals mass times acceleration\n```"
        elif section_type == 'summary_quote':
            return f"> Summary of key points about {topic} in {subject}"
        else:
            return f"This section covers important aspects of {topic} in {subject}."

    def ai_enhanced_content_generation(self, base_content: Dict[str, Any], enhancements: List[str]) -> Optional[Dict[str, Any]]:
        """AI-assisted content enhancement (placeholder for future AI integration)"""
        print("🧠 PHASE 1C: AI-Enhanced Content Generation")

        # This is a placeholder for future AI integration
        # In a real implementation, this would call AI services like OpenAI, Claude, etc.

        enhanced_content = base_content.copy()

        for enhancement in enhancements:
            if enhancement == 'expand_examples':
                # Add more detailed examples
                enhanced_content['content'] += "\n\n## Additional Examples\n\nMore detailed examples would be added here by AI."
            elif enhancement == 'add_quiz':
                # Add quiz questions
                enhanced_content['content'] += "\n\n## Practice Quiz\n\n1. Question 1?\n2. Question 2?"
            elif enhancement == 'cultural_adaptation':
                # Adapt for Nigerian context
                enhanced_content['content'] += "\n\n## Nigerian Context\n\nRelevant Nigerian examples and applications."
            elif enhancement == 'multimedia_suggestions':
                # Suggest multimedia elements
                enhanced_content['content'] += "\n\n## Multimedia Resources\n\n- Suggested video: [Link]\n- Interactive diagram: [Link]"

        enhanced_content['ai_enhanced'] = True
        enhanced_content['enhancements'] = enhancements
        enhanced_content['updated_at'] = datetime.now().isoformat()

        # Save enhanced content
        success = content_service.add_content(enhanced_content)
        if success:
            self.stats['ai_enhanced'] += 1
            print(f"✅ AI-enhanced: {enhanced_content['title']}")
            return enhanced_content

        return None

    def external_content_integration(self, source_url: str, content_type: str = 'article') -> Optional[Dict[str, Any]]:
        """Integrate content from external sources"""
        print("🌐 PHASE 1C: External Content Integration")

        try:
            # This is a placeholder for web scraping/API integration
            # In a real implementation, this would scrape or fetch from educational APIs

            # Simulate fetching external content
            external_content = {
                'title': f'External Content from {source_url}',
                'content': f'Content fetched from {source_url} would be processed and formatted here.',
                'source_url': source_url,
                'content_type': content_type,
                'author': 'External Source',
                'creation_method': 'external_integration'
            }

            # Process and format the content
            processed_content = self._process_external_content(external_content)

            if processed_content:
                success = content_service.add_content(processed_content)
                if success:
                    self.stats['external_integrated'] += 1
                    print(f"✅ Integrated external content: {processed_content['title']}")
                    return processed_content

        except Exception as e:
            print(f"❌ Error integrating external content: {e}")

        return None

    def _process_external_content(self, external_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process and format external content"""
        # Clean and format the content
        processed = external_content.copy()

        # Generate ID
        processed['id'] = f"external_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Add metadata
        processed.update({
            'subject': 'General',  # Would be determined by content analysis
            'topic': 'External Content',
            'difficulty': 'intermediate',
            'exam_board': 'General',
            'estimated_read_time': 10,
            'version': 1,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })

        return processed

    def automated_formatting_and_structuring(self, raw_content: str, target_format: str = 'markdown') -> str:
        """Automatically format and structure raw content"""
        print("🔧 PHASE 1C: Automated Formatting and Structuring")

        # Basic text processing and structuring
        formatted_content = raw_content

        # Add headings if missing
        if not formatted_content.startswith('#'):
            lines = formatted_content.split('\n')
            if len(lines) > 0:
                lines[0] = f"# {lines[0]}"
                formatted_content = '\n'.join(lines)

        # Add basic structure
        if '## ' not in formatted_content:
            formatted_content += "\n\n## Overview\n\nContent overview would be generated here."

        # Add metadata section
        formatted_content += "\n\n## Key Points\n\n- Point 1\n- Point 2\n- Point 3"

        return formatted_content

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def show_stats(self):
        """Display creation statistics"""
        print("\n📊 Content Creation Statistics")
        print("=" * 40)
        print(f"Manual Content Created: {self.stats['manual_created']}")
        print(f"CSV/JSON Imported: {self.stats['csv_imported']}")
        print(f"Auto Generated: {self.stats['auto_generated']}")
        print(f"AI Enhanced: {self.stats['ai_enhanced']}")
        print(f"External Integrated: {self.stats['external_integrated']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Total Content Items: {sum(self.stats.values()) - self.stats['errors']}")

    def export_content_library(self, filename: str = 'content_library.json'):
        """Export all content to a library file"""
        try:
            # This would fetch all content from the database
            # For now, just create an empty library structure
            library = {
                'exported_at': datetime.now().isoformat(),
                'total_items': 0,
                'subjects': {},
                'content': []
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(library, f, indent=2, ensure_ascii=False)

            print(f"✅ Content library exported to {filename}")

        except Exception as e:
            print(f"❌ Error exporting library: {e}")

def main():
    """Main content creation strategies interface"""
    strategies = ContentCreationStrategies()

    parser = argparse.ArgumentParser(description='Akulearn Content Creation Strategies')
    parser.add_argument('--manual', action='store_true', help='Start manual content creation wizard')
    parser.add_argument('--csv-import', type=str, help='Import content from CSV file')
    parser.add_argument('--json-import', type=str, help='Import content from JSON file')
    parser.add_argument('--generate-csv-template', action='store_true', help='Generate CSV import template')
    parser.add_argument('--auto-generate', nargs=3, metavar=('SUBJECT', 'TOPIC', 'COUNT'), help='Auto-generate content (subject topic count)')
    parser.add_argument('--external-integrate', type=str, help='Integrate content from external URL')
    parser.add_argument('--stats', action='store_true', help='Show content creation statistics')
    parser.add_argument('--export-library', type=str, nargs='?', const='content_library.json', help='Export content library')

    args = parser.parse_args()

    if args.manual:
        strategies.manual_content_creation_wizard()

    elif args.csv_import:
        result = strategies.csv_bulk_import(args.csv_import)
        if result['success']:
            print(f"✅ Successfully imported {result['imported']} items")
        else:
            print(f"❌ Import failed: {result['error']}")

    elif args.json_import:
        result = strategies.json_bulk_import(args.json_import)
        if result['success']:
            print(f"✅ Successfully imported {result['imported']} items")
        else:
            print(f"❌ Import failed: {result['error']}")

    elif args.generate_csv_template:
        strategies.generate_csv_template()

    elif args.auto_generate:
        subject, topic, count = args.auto_generate
        try:
            count = int(count)
            content = strategies.automated_content_generation(subject, topic, count)
            print(f"✅ Generated {len(content)} content items")
        except ValueError:
            print("❌ Count must be a number")

    elif args.external_integrate:
        content = strategies.external_content_integration(args.external_integrate)
        if content:
            print("✅ External content integrated")
        else:
            print("❌ External content integration failed")

    elif args.stats:
        strategies.show_stats()

    elif args.export_library:
        strategies.export_content_library(args.export_library)

    else:
        # Interactive menu
        print("🎯 Akulearn Content Creation Strategies")
        print("=" * 50)
        print("1. Manual Content Creation Wizard")
        print("2. CSV Bulk Import")
        print("3. JSON Bulk Import")
        print("4. Generate CSV Template")
        print("5. Automated Content Generation")
        print("6. External Content Integration")
        print("7. Show Statistics")
        print("8. Export Content Library")
        print("9. Exit")

        while True:
            choice = input("\nSelect option (1-9): ").strip()

            if choice == "1":
                strategies.manual_content_creation_wizard()

            elif choice == "2":
                csv_file = input("Enter CSV file path: ").strip()
                if csv_file:
                    result = strategies.csv_bulk_import(csv_file)
                    if result['success']:
                        print(f"✅ Successfully imported {result['imported']} items")
                    else:
                        print(f"❌ Import failed: {result['error']}")

            elif choice == "3":
                json_file = input("Enter JSON file path: ").strip()
                if json_file:
                    result = strategies.json_bulk_import(json_file)
                    if result['success']:
                        print(f"✅ Successfully imported {result['imported']} items")
                    else:
                        print(f"❌ Import failed: {result['error']}")

            elif choice == "4":
                strategies.generate_csv_template()

            elif choice == "5":
                subject = input("Subject: ").strip()
                topic = input("Topic: ").strip()
                count = input("Number of items to generate: ").strip()
                if subject and topic and count.isdigit():
                    content = strategies.automated_content_generation(subject, topic, int(count))
                    print(f"✅ Generated {len(content)} content items")

            elif choice == "6":
                url = input("External content URL: ").strip()
                if url:
                    content = strategies.external_content_integration(url)
                    if content:
                        print("✅ External content integrated")
                    else:
                        print("❌ External content integration failed")

            elif choice == "7":
                strategies.show_stats()

            elif choice == "8":
                filename = input("Export filename [content_library.json]: ").strip()
                if not filename:
                    filename = 'content_library.json'
                strategies.export_content_library(filename)

            elif choice == "9":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option")

if __name__ == "__main__":
    main()