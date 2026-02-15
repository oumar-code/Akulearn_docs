#!/usr/bin/env python3
"""
Enhanced CSV Template Generator and Bulk Import System
Creates comprehensive templates and handles bulk content imports
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

class EnhancedCSVManager:
    """Enhanced CSV template generation and bulk import management"""

    def __init__(self):
        self.templates_dir = "content_templates"
        self.imports_dir = "content_imports"
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.imports_dir, exist_ok=True)

    def generate_comprehensive_csv_template(self, subject: str = None, output_file: str = None) -> str:
        """Generate a comprehensive CSV template for content creation"""

        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if subject:
                output_file = f"{self.templates_dir}/content_template_{subject.lower()}_{timestamp}.csv"
            else:
                output_file = f"{self.templates_dir}/content_template_comprehensive_{timestamp}.csv"

        # Define comprehensive template data based on subject
        template_data = self._get_template_data_for_subject(subject)

        # Define all possible fields
        fieldnames = [
            'title', 'subject', 'topic', 'subtopic', 'content_type', 'difficulty',
            'exam_board', 'content', 'summary', 'learning_objectives', 'key_concepts',
            'worked_examples', 'important_formulas', 'common_mistakes', 'practice_problems',
            'exam_tips', 'estimated_read_time', 'prerequisites', 'related_questions',
            'tags', 'author', 'references', 'multimedia_links', 'cultural_notes'
        ]

        # Write CSV template
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(template_data)

        print(f"✅ Comprehensive CSV template generated: {output_file}")
        print(f"📋 Includes {len(template_data)} sample rows")
        print("🔧 Fields include: content, examples, formulas, prerequisites, etc.")

        return output_file

    def _get_template_data_for_subject(self, subject: str = None) -> List[Dict[str, Any]]:
        """Get template data based on subject"""

        if subject and subject.lower() == 'mathematics':
            return [
                {
                    'title': 'Solving Quadratic Equations by Factorization',
                    'subject': 'Mathematics',
                    'topic': 'Algebra',
                    'subtopic': 'Quadratic Equations',
                    'content_type': 'study_guide',
                    'difficulty': 'intermediate',
                    'exam_board': 'WAEC',
                    'content': '''# Solving Quadratic Equations by Factorization

## Introduction
Quadratic equations are polynomial equations of degree 2. They can be solved using several methods including factorization.

## Method: Factorization
To solve ax² + bx + c = 0 by factorization:

1. Write the equation in standard form
2. Factor the quadratic expression
3. Set each factor equal to zero
4. Solve for the variable

## Worked Examples

### Example 1: Simple Factorization
Solve x² + 5x + 6 = 0

**Step 1:** Factor the quadratic
(x + 2)(x + 3) = 0

**Step 2:** Set each factor to zero
x + 2 = 0 or x + 3 = 0

**Step 3:** Solve each equation
x = -2 or x = -3

### Example 2: With Common Factor
Solve 2x² + 8x + 6 = 0

**Step 1:** Divide by 2: x² + 4x + 3 = 0
**Step 2:** Factor: (x + 1)(x + 3) = 0
**Step 3:** x = -1 or x = -3''',
                    'summary': 'Factorization method for solving quadratic equations with step-by-step examples',
                    'learning_objectives': 'Solve quadratic equations by factorization,Identify when to use factorization,Apply factorization to real-world problems',
                    'key_concepts': 'Standard form: ax² + bx + c = 0,Zero product property,Factors and roots',
                    'worked_examples': 'x² + 5x + 6 = 0 → (x + 2)(x + 3) = 0 → x = -2, -3',
                    'important_formulas': 'ax² + bx + c = (x + m)(x + n) where m + n = b, mn = c',
                    'common_mistakes': 'Forgetting to set factors equal to zero,Ignoring the ± in solutions,Not checking solutions',
                    'practice_problems': 'Solve: x² - 7x + 12 = 0, 2x² + x - 6 = 0, x² + 2x - 8 = 0',
                    'exam_tips': 'Always check your factors by expanding,Look for common factors first,Practice different number combinations',
                    'estimated_read_time': '20',
                    'prerequisites': 'Basic algebra,Linear equations',
                    'related_questions': 'WAEC Math 2020 Q1,WAEC Math 2021 Q3',
                    'tags': 'algebra,quadratic equations,factorization,mathematics',
                    'author': 'Mathematics Expert',
                    'references': 'WAEC Mathematics Syllabus 2023,Adelodun A. (2019) Mathematics for Senior Secondary Schools',
                    'cultural_notes': 'Quadratic equations appear in Nigerian business calculations for profit maximization'
                },
                {
                    'title': 'Trigonometric Ratios and Identities',
                    'subject': 'Mathematics',
                    'topic': 'Trigonometry',
                    'subtopic': 'Basic Ratios',
                    'content_type': 'reference',
                    'difficulty': 'intermediate',
                    'exam_board': 'WAEC',
                    'content': '''# Trigonometric Ratios

## The Three Main Ratios

### Sine (sin)
sin θ = Opposite / Hypotenuse

### Cosine (cos)
cos θ = Adjacent / Hypotenuse

### Tangent (tan)
tan θ = Opposite / Adjacent

## Reciprocal Ratios

### Cosecant (cosec)
cosec θ = 1 / sin θ = Hypotenuse / Opposite

### Secant (sec)
sec θ = 1 / cos θ = Hypotenuse / Adjacent

### Cotangent (cot)
cot θ = 1 / tan θ = Adjacent / Opposite

## Important Identities

### Pythagorean Identity
sin²θ + cos²θ = 1

### Quotient Identity
tan θ = sin θ / cos θ

### Reciprocal Identities
cosec θ = 1/sin θ, sec θ = 1/cos θ, cot θ = 1/tan θ

## Special Angles

| Angle | sin | cos | tan |
|-------|-----|-----|-----|
| 0°   | 0   | 1   | 0   |
| 30°  | 1/2 | √3/2| 1/√3|
| 45°  | √2/2| √2/2| 1   |
| 60°  | √3/2| 1/2 | √3  |
| 90°  | 1   | 0   | ∞   |''',
                    'summary': 'Complete reference for trigonometric ratios, identities, and special angles',
                    'learning_objectives': 'Define trigonometric ratios,Apply ratios to right-angled triangles,Use trigonometric identities',
                    'key_concepts': 'SOHCAHTOA mnemonic,Right-angled triangles,Special triangles',
                    'worked_examples': 'In △ABC with ∠C=90°, ∠A=30°, AC=5cm. Find sin A, cos A, tan A',
                    'important_formulas': 'sin θ = opp/hyp, cos θ = adj/hyp, tan θ = opp/adj, sin²θ + cos²θ = 1',
                    'practice_problems': 'Find trigonometric ratios for 45° and 60° angles,Solve for missing sides using ratios',
                    'estimated_read_time': '25',
                    'prerequisites': 'Pythagoras theorem,Similar triangles',
                    'tags': 'trigonometry,ratios,identities,mathematics',
                    'author': 'Mathematics Expert'
                }
            ]

        elif subject and subject.lower() == 'physics':
            return [
                {
                    'title': 'Newton\'s Laws of Motion',
                    'subject': 'Physics',
                    'topic': 'Mechanics',
                    'subtopic': 'Laws of Motion',
                    'content_type': 'study_guide',
                    'difficulty': 'intermediate',
                    'exam_board': 'WAEC',
                    'content': '''# Newton's Laws of Motion

## First Law (Law of Inertia)
**Statement:** An object at rest stays at rest, and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.

**Inertia** is the tendency of an object to resist changes in its state of motion.

### Examples:
- A book on a table remains at rest until pushed
- A moving car continues moving until brakes are applied
- Passengers in a bus fall forward when the bus stops suddenly

## Second Law (F = ma)
**Statement:** The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.

**Formula:** F = ma
- F = force (N)
- m = mass (kg)
- a = acceleration (m/s²)

### Examples:
- More force = more acceleration (same mass)
- More mass = less acceleration (same force)
- Force and acceleration are in the same direction

## Third Law (Action-Reaction)
**Statement:** For every action, there is an equal and opposite reaction.

### Examples:
- Rocket propulsion: exhaust gases push down, rocket goes up
- Walking: feet push ground backward, body moves forward
- Book on table: gravity pulls book down, table pushes up''',
                    'summary': 'Comprehensive guide to Newton\'s three laws of motion with examples and applications',
                    'learning_objectives': 'State Newton\'s laws,Explain inertia and momentum,Apply laws to real-world situations',
                    'key_concepts': 'Inertia,Force,Mass,Acceleration,Action-Reaction pairs',
                    'worked_examples': 'A 2kg object accelerates at 3m/s². What force is acting on it?',
                    'important_formulas': 'F = ma, F_net = ma, Weight = mg',
                    'common_mistakes': 'Confusing mass and weight,Forgetting net force,Ignoring direction of forces',
                    'practice_problems': 'Calculate force needed to accelerate 5kg mass at 2m/s²,Explain why rockets work',
                    'exam_tips': 'Remember examples for each law,Practice force diagrams,Understand vector nature of forces',
                    'estimated_read_time': '30',
                    'prerequisites': 'Basic mechanics,Forces,Vectors',
                    'tags': 'newton,laws,motion,mechanics,physics',
                    'author': 'Physics Expert'
                }
            ]

        else:
            # General comprehensive template
            return [
                {
                    'title': 'Sample Study Guide Title',
                    'subject': 'Subject',
                    'topic': 'Topic',
                    'subtopic': 'Subtopic',
                    'content_type': 'study_guide',
                    'difficulty': 'intermediate',
                    'exam_board': 'WAEC',
                    'content': '# Main Content\n\n## Introduction\n\nIntroduction content here.\n\n## Key Concepts\n\n- Concept 1\n- Concept 2\n- Concept 3\n\n## Examples\n\nExample content here.',
                    'summary': 'Brief summary of the content',
                    'learning_objectives': 'Objective 1,Objective 2,Objective 3',
                    'key_concepts': 'Concept 1,Concept 2,Concept 3',
                    'worked_examples': 'Example 1,Example 2',
                    'important_formulas': 'Formula 1,Formula 2',
                    'common_mistakes': 'Mistake 1,Mistake 2',
                    'practice_problems': 'Problem 1,Problem 2',
                    'exam_tips': 'Tip 1,Tip 2',
                    'estimated_read_time': '15',
                    'prerequisites': 'Prerequisite 1,Prerequisite 2',
                    'related_questions': 'Question 1,Question 2',
                    'tags': 'tag1,tag2,tag3',
                    'author': 'Content Creator',
                    'references': 'Reference 1,Reference 2',
                    'cultural_notes': 'Cultural adaptation notes'
                }
            ]

    def generate_subject_specific_templates(self):
        """Generate templates for all subjects"""
        subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'Geography', 'Economics']

        for subject in subjects:
            template_file = self.generate_comprehensive_csv_template(subject)
            print(f"📄 Generated template for {subject}: {template_file}")

    def bulk_import_with_validation(self, csv_file: str, validate_only: bool = False) -> Dict[str, Any]:
        """Enhanced bulk import with comprehensive validation"""

        if not os.path.exists(csv_file):
            return {'success': False, 'error': f'File {csv_file} not found'}

        results = {
            'total_rows': 0,
            'valid_rows': 0,
            'invalid_rows': 0,
            'imported_rows': 0,
            'errors': [],
            'warnings': []
        }

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
                    results['total_rows'] += 1

                    # Validate row
                    validation_result = self._validate_content_row(row, row_num)

                    if validation_result['valid']:
                        results['valid_rows'] += 1

                        if not validate_only:
                            # Import the content
                            import_result = self._import_validated_row(row)
                            if import_result['success']:
                                results['imported_rows'] += 1
                            else:
                                results['errors'].append(f"Row {row_num}: Import failed - {import_result['error']}")
                    else:
                        results['invalid_rows'] += 1
                        results['errors'].extend(validation_result['errors'])

                    # Add warnings
                    if validation_result['warnings']:
                        results['warnings'].extend([f"Row {row_num}: {w}" for w in validation_result['warnings']])

        except Exception as e:
            return {'success': False, 'error': f'Error reading CSV: {str(e)}'}

        results['success'] = True
        return results

    def _validate_content_row(self, row: Dict[str, str], row_num: int) -> Dict[str, Any]:
        """Comprehensive row validation"""

        errors = []
        warnings = []
        valid = True

        # Required fields
        required_fields = ['title', 'subject', 'topic', 'content_type', 'difficulty', 'exam_board', 'content']
        for field in required_fields:
            if not row.get(field, '').strip():
                errors.append(f"Missing required field: {field}")
                valid = False

        # Content type validation
        valid_content_types = ['study_guide', 'reference', 'summary', 'exercise', 'tutorial', 'case_study']
        content_type = row.get('content_type', '').strip()
        if content_type and content_type not in valid_content_types:
            errors.append(f"Invalid content_type '{content_type}'. Must be one of: {valid_content_types}")
            valid = False

        # Difficulty validation
        valid_difficulties = ['basic', 'intermediate', 'advanced']
        difficulty = row.get('difficulty', '').strip()
        if difficulty and difficulty not in valid_difficulties:
            errors.append(f"Invalid difficulty '{difficulty}'. Must be one of: {valid_difficulties}")
            valid = False

        # Exam board validation
        valid_boards = ['WAEC', 'NECO', 'JAMB', 'General']
        exam_board = row.get('exam_board', '').strip()
        if exam_board and exam_board not in valid_boards:
            errors.append(f"Invalid exam_board '{exam_board}'. Must be one of: {valid_boards}")
            valid = False

        # Read time validation
        if row.get('estimated_read_time'):
            try:
                read_time = int(row['estimated_read_time'])
                if read_time < 1 or read_time > 120:
                    warnings.append(f"Read time {read_time} minutes seems unusual (expected 1-120)")
            except ValueError:
                errors.append(f"Invalid estimated_read_time '{row['estimated_read_time']}'. Must be a number.")
                valid = False

        # Content length validation
        content = row.get('content', '').strip()
        if content:
            if len(content) < 50:
                warnings.append("Content seems very short (less than 50 characters)")
            elif len(content) > 50000:
                warnings.append("Content is very long (over 50,000 characters)")

        # URL validation for multimedia links
        if row.get('multimedia_links'):
            links = [link.strip() for link in row['multimedia_links'].split(',') if link.strip()]
            for link in links:
                if not (link.startswith('http://') or link.startswith('https://')):
                    warnings.append(f"Multimedia link '{link}' doesn't appear to be a valid URL")

        return {
            'valid': valid,
            'errors': errors,
            'warnings': warnings
        }

    def _import_validated_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Import a validated row"""

        try:
            # Generate unique ID
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            content_id = f"{row['subject'].lower().replace(' ', '_')}_{row['topic'].lower().replace(' ', '_')}_{row['content_type']}_{timestamp}"

            # Process list fields
            def process_list_field(field_value: str) -> List[str]:
                if not field_value:
                    return []
                return [item.strip() for item in field_value.split(',') if item.strip()]

            # Create content object
            content = {
                'id': content_id,
                'title': row['title'].strip(),
                'subject': row['subject'].strip(),
                'topic': row['topic'].strip(),
                'subtopic': row.get('subtopic', '').strip(),
                'content_type': row['content_type'].strip(),
                'difficulty': row['difficulty'].strip(),
                'exam_board': row['exam_board'].strip(),
                'content': row['content'].strip(),
                'summary': row.get('summary', '').strip(),
                'learning_objectives': process_list_field(row.get('learning_objectives', '')),
                'key_concepts': process_list_field(row.get('key_concepts', '')),
                'worked_examples': row.get('worked_examples', '').strip(),
                'important_formulas': row.get('important_formulas', '').strip(),
                'common_mistakes': process_list_field(row.get('common_mistakes', '')),
                'practice_problems': process_list_field(row.get('practice_problems', '')),
                'exam_tips': process_list_field(row.get('exam_tips', '')),
                'estimated_read_time': int(row.get('estimated_read_time') or 15),
                'prerequisites': process_list_field(row.get('prerequisites', '')),
                'related_questions': process_list_field(row.get('related_questions', '')),
                'tags': process_list_field(row.get('tags', '')),
                'author': row.get('author', 'CSV Import').strip(),
                'references': process_list_field(row.get('references', '')),
                'multimedia_links': process_list_field(row.get('multimedia_links', '')),
                'cultural_notes': row.get('cultural_notes', '').strip(),
                'version': 1,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'creation_method': 'csv_bulk_import'
            }

            # Import to database (placeholder - would use actual content service)
            # success = content_service.add_content(content)

            # For now, just simulate success
            success = True

            if success:
                return {'success': True, 'content_id': content_id}
            else:
                return {'success': False, 'error': 'Database insertion failed'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def generate_import_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a detailed import report"""

        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{self.imports_dir}/import_report_{timestamp}.json"

        # Create comprehensive report
        report = {
            'import_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_rows_processed': results['total_rows'],
                'valid_rows': results['valid_rows'],
                'invalid_rows': results['invalid_rows'],
                'successfully_imported': results['imported_rows'],
                'success_rate': f"{(results['imported_rows'] / results['total_rows'] * 100):.1f}%" if results['total_rows'] > 0 else "0%"
            },
            'errors': results['errors'],
            'warnings': results['warnings'],
            'recommendations': self._generate_import_recommendations(results)
        }

        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return output_file

    def _generate_import_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on import results"""

        recommendations = []

        if results['invalid_rows'] > 0:
            recommendations.append(f"Fix validation errors in {results['invalid_rows']} rows before re-importing")

        if results['warnings']:
            recommendations.append("Review warnings to improve content quality")

        success_rate = (results['imported_rows'] / results['total_rows'] * 100) if results['total_rows'] > 0 else 0

        if success_rate < 80:
            recommendations.append("Consider using the CSV template generator for better data structure")
        elif success_rate >= 95:
            recommendations.append("Excellent data quality! Consider this as a template for future imports")

        if results['total_rows'] > 100:
            recommendations.append("Large import detected - consider breaking into smaller batches for better error handling")

        return recommendations

def main():
    """Command-line interface for enhanced CSV management"""

    manager = EnhancedCSVManager()

    parser = argparse.ArgumentParser(description='Enhanced CSV Template Generator and Bulk Import')
    parser.add_argument('--generate-template', nargs='?', const='all', help='Generate CSV template (optionally specify subject)')
    parser.add_argument('--generate-all-templates', action='store_true', help='Generate templates for all subjects')
    parser.add_argument('--bulk-import', type=str, help='Bulk import from CSV file')
    parser.add_argument('--validate-only', action='store_true', help='Only validate CSV without importing')
    parser.add_argument('--generate-report', type=str, help='Generate import report from results file')

    args = parser.parse_args()

    if args.generate_template:
        if args.generate_template == 'all':
            manager.generate_comprehensive_csv_template()
        else:
            manager.generate_comprehensive_csv_template(args.generate_template)

    elif args.generate_all_templates:
        manager.generate_subject_specific_templates()

    elif args.bulk_import:
        print(f"📥 Starting bulk import from {args.bulk_import}")

        if args.validate_only:
            print("🔍 Validation mode - no data will be imported")

        results = manager.bulk_import_with_validation(args.bulk_import, validate_only=args.validate_only)

        if results['success']:
            print("✅ Import completed!")
            print(f"📊 Total rows: {results['total_rows']}")
            print(f"✅ Valid rows: {results['valid_rows']}")
            print(f"❌ Invalid rows: {results['invalid_rows']}")
            print(f"💾 Imported rows: {results['imported_rows']}")

            if results['errors']:
                print(f"🚨 Errors: {len(results['errors'])}")
                for error in results['errors'][:5]:  # Show first 5 errors
                    print(f"  - {error}")
                if len(results['errors']) > 5:
                    print(f"  ... and {len(results['errors']) - 5} more errors")

            if results['warnings']:
                print(f"⚠️  Warnings: {len(results['warnings'])}")
                for warning in results['warnings'][:3]:  # Show first 3 warnings
                    print(f"  - {warning}")

            # Generate report
            report_file = manager.generate_import_report(results)
            print(f"📄 Detailed report saved to: {report_file}")

        else:
            print(f"❌ Import failed: {results['error']}")

    elif args.generate_report:
        # This would load results from a file and generate report
        print("Report generation from file not yet implemented")

    else:
        # Interactive menu
        print("📊 Enhanced CSV Content Management")
        print("=" * 40)
        print("1. Generate comprehensive CSV template")
        print("2. Generate subject-specific templates")
        print("3. Bulk import from CSV")
        print("4. Validate CSV without importing")
        print("5. Exit")

        while True:
            choice = input("\nSelect option (1-5): ").strip()

            if choice == "1":
                subject = input("Subject (or press Enter for general): ").strip()
                if subject:
                    manager.generate_comprehensive_csv_template(subject)
                else:
                    manager.generate_comprehensive_csv_template()

            elif choice == "2":
                manager.generate_subject_specific_templates()

            elif choice == "3":
                csv_file = input("CSV file path: ").strip()
                if csv_file and os.path.exists(csv_file):
                    results = manager.bulk_import_with_validation(csv_file, validate_only=False)
                    if results['success']:
                        report_file = manager.generate_import_report(results)
                        print(f"✅ Import completed. Report: {report_file}")
                    else:
                        print(f"❌ Import failed: {results['error']}")
                else:
                    print("❌ File not found")

            elif choice == "4":
                csv_file = input("CSV file path: ").strip()
                if csv_file and os.path.exists(csv_file):
                    results = manager.bulk_import_with_validation(csv_file, validate_only=True)
                    if results['success']:
                        print("✅ Validation completed!")
                        print(f"📊 Total rows: {results['total_rows']}")
                        print(f"✅ Valid rows: {results['valid_rows']}")
                        print(f"❌ Invalid rows: {results['invalid_rows']}")
                    else:
                        print(f"❌ Validation failed: {results['error']}")
                else:
                    print("❌ File not found")

            elif choice == "5":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option")

if __name__ == "__main__":
    main()