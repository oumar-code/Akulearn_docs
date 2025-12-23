#!/usr/bin/env python3
"""
Content Validation and Quality Assurance System
Comprehensive validation, quality checks, and content enhancement
"""

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import argparse
from collections import Counter

class ContentValidator:
    """Comprehensive content validation and quality assurance"""

    def __init__(self):
        self.validation_rules = self._load_validation_rules()
        self.quality_metrics = {}
        self.validation_reports = []

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules for different content types"""

        return {
            'study_guide': {
                'required_fields': ['title', 'subject', 'topic', 'content', 'learning_objectives'],
                'min_content_length': 500,
                'max_content_length': 50000,
                'required_sections': ['introduction', 'key_concepts', 'examples'],
                'quality_checks': ['structure', 'completeness', 'readability', 'accuracy']
            },
            'reference': {
                'required_fields': ['title', 'subject', 'topic', 'content'],
                'min_content_length': 200,
                'max_content_length': 25000,
                'required_sections': ['definitions', 'examples'],
                'quality_checks': ['structure', 'accuracy', 'completeness']
            },
            'summary': {
                'required_fields': ['title', 'subject', 'topic', 'content', 'summary'],
                'min_content_length': 100,
                'max_content_length': 5000,
                'quality_checks': ['conciseness', 'accuracy', 'completeness']
            },
            'exercise': {
                'required_fields': ['title', 'subject', 'topic', 'content', 'practice_problems'],
                'min_content_length': 200,
                'max_content_length': 15000,
                'required_sections': ['problems', 'solutions'],
                'quality_checks': ['difficulty_balance', 'solution_quality', 'variety']
            },
            'tutorial': {
                'required_fields': ['title', 'subject', 'topic', 'content', 'learning_objectives'],
                'min_content_length': 800,
                'max_content_length': 30000,
                'required_sections': ['introduction', 'steps', 'examples', 'practice'],
                'quality_checks': ['step_by_step', 'examples', 'progression', 'engagement']
            },
            'case_study': {
                'required_fields': ['title', 'subject', 'topic', 'content'],
                'min_content_length': 600,
                'max_content_length': 20000,
                'required_sections': ['scenario', 'analysis', 'conclusion'],
                'quality_checks': ['real_world_relevance', 'analysis_depth', 'conclusion_quality']
            }
        }

    def validate_content(self, content: Dict[str, Any], strict_mode: bool = False) -> Dict[str, Any]:
        """Comprehensive content validation"""

        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 0,
            'quality_breakdown': {},
            'recommendations': [],
            'validation_timestamp': datetime.now().isoformat()
        }

        content_type = content.get('content_type', 'study_guide')

        # Basic field validation
        field_validation = self._validate_required_fields(content, content_type)
        validation_result['errors'].extend(field_validation['errors'])
        validation_result['warnings'].extend(field_validation['warnings'])

        # Content structure validation
        structure_validation = self._validate_content_structure(content, content_type)
        validation_result['errors'].extend(structure_validation['errors'])
        validation_result['warnings'].extend(structure_validation['warnings'])

        # Content quality checks
        quality_result = self._assess_content_quality(content, content_type)
        validation_result['quality_score'] = quality_result['score']
        validation_result['quality_breakdown'] = quality_result['breakdown']
        validation_result['warnings'].extend(quality_result['warnings'])

        # Subject-specific validation
        subject_validation = self._validate_subject_specific_rules(content)
        validation_result['errors'].extend(subject_validation['errors'])
        validation_result['warnings'].extend(subject_validation['warnings'])

        # Cultural adaptation check
        cultural_check = self._check_cultural_adaptation(content)
        validation_result['warnings'].extend(cultural_check['warnings'])
        validation_result['recommendations'].extend(cultural_check['recommendations'])

        # Determine overall validity
        if validation_result['errors']:
            validation_result['is_valid'] = False
        elif strict_mode and validation_result['quality_score'] < 70:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Quality score too low ({validation_result['quality_score']}) for strict mode")

        # Generate recommendations
        validation_result['recommendations'].extend(self._generate_improvement_recommendations(content, validation_result))

        return validation_result

    def _validate_required_fields(self, content: Dict[str, Any], content_type: str) -> Dict[str, List[str]]:
        """Validate required fields based on content type"""

        errors = []
        warnings = []

        rules = self.validation_rules.get(content_type, self.validation_rules['study_guide'])
        required_fields = rules['required_fields']

        for field in required_fields:
            if field not in content or not content[field]:
                errors.append(f"Missing required field: {field}")
            elif isinstance(content[field], str) and len(content[field].strip()) == 0:
                errors.append(f"Empty required field: {field}")
            elif isinstance(content[field], list) and len(content[field]) == 0:
                errors.append(f"Empty required field: {field}")

        # Check for obviously placeholder content
        placeholder_indicators = ['lorem ipsum', 'placeholder', 'todo', 'tbd', 'coming soon']
        for field, value in content.items():
            if isinstance(value, str):
                lower_value = value.lower()
                for indicator in placeholder_indicators:
                    if indicator in lower_value:
                        warnings.append(f"Field '{field}' contains placeholder text: '{indicator}'")

        return {'errors': errors, 'warnings': warnings}

    def _validate_content_structure(self, content: Dict[str, Any], content_type: str) -> Dict[str, List[str]]:
        """Validate content structure and formatting"""

        errors = []
        warnings = []

        rules = self.validation_rules.get(content_type, self.validation_rules['study_guide'])
        main_content = content.get('content', '')

        # Length validation
        min_length = rules['min_content_length']
        max_length = rules['max_content_length']

        if len(main_content) < min_length:
            errors.append(f"Content too short ({len(main_content)} chars, minimum {min_length})")
        elif len(main_content) > max_length:
            warnings.append(f"Content very long ({len(main_content)} chars, maximum {max_length})")

        # Required sections check
        if 'required_sections' in rules:
            required_sections = rules['required_sections']
            content_lower = main_content.lower()

            for section in required_sections:
                # Check for section headers (markdown style)
                section_patterns = [
                    f'# {section}',
                    f'## {section}',
                    f'### {section}',
                    f'**{section}**',
                    f'{section}:'
                ]

                found = any(pattern.lower() in content_lower for pattern in section_patterns)
                if not found:
                    warnings.append(f"Missing section: '{section}' (check content structure)")

        # Markdown formatting check
        if main_content.strip():
            # Check for basic markdown elements
            has_headers = '#' in main_content
            has_lists = any(marker in main_content for marker in ['- ', '* ', '1. ', '2. '])

            if not has_headers and len(main_content) > 1000:
                warnings.append("Long content without headers - consider adding section breaks")

            if not has_lists and 'example' in main_content.lower():
                warnings.append("Content mentions examples but no lists found - consider formatting as bullet points")

        # Check for broken formatting
        broken_patterns = [
            (r'\*\*\s*\*\*', 'Empty bold formatting'),
            (r'__\s*__', 'Empty italic formatting'),
            (r'\[\]\(\)', 'Empty link formatting'),
            (r'!\[\]\(\)', 'Empty image formatting')
        ]

        for pattern, description in broken_patterns:
            if re.search(pattern, main_content):
                warnings.append(f"Broken markdown formatting: {description}")

        return {'errors': errors, 'warnings': warnings}

    def _assess_content_quality(self, content: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Assess overall content quality"""

        quality_scores = {
            'structure': 0,
            'completeness': 0,
            'readability': 0,
            'accuracy': 0,
            'engagement': 0,
            'cultural_relevance': 0
        }

        warnings = []

        # Structure quality (0-20 points)
        main_content = content.get('content', '')
        if main_content:
            # Check for proper heading hierarchy
            h1_count = main_content.count('# ')
            h2_count = main_content.count('## ')
            h3_count = main_content.count('### ')

            if h1_count == 1 and h2_count >= 1:
                quality_scores['structure'] = 20
            elif h2_count >= 1:
                quality_scores['structure'] = 15
            elif h1_count >= 1:
                quality_scores['structure'] = 10
            else:
                quality_scores['structure'] = 5
                warnings.append("Content lacks clear section structure")

        # Completeness quality (0-25 points)
        completeness_score = 0
        optional_fields = ['summary', 'learning_objectives', 'key_concepts', 'worked_examples',
                          'practice_problems', 'exam_tips', 'prerequisites']

        filled_optional = sum(1 for field in optional_fields if content.get(field))
        completeness_score = min(25, filled_optional * 3)
        quality_scores['completeness'] = completeness_score

        if completeness_score < 10:
            warnings.append("Content lacks supporting materials (examples, objectives, etc.)")

        # Readability quality (0-20 points)
        if main_content:
            sentences = re.split(r'[.!?]+', main_content)
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0

            if 10 <= avg_sentence_length <= 25:
                quality_scores['readability'] = 20
            elif 5 <= avg_sentence_length <= 35:
                quality_scores['readability'] = 15
            else:
                quality_scores['readability'] = 10
                warnings.append(f"Average sentence length ({avg_sentence_length:.1f} words) may affect readability")

        # Accuracy quality (0-20 points) - basic checks
        accuracy_score = 15  # Base score, would need more sophisticated checks

        # Check for common errors
        error_patterns = [
            r'\bteh\b',  # Common typo
            r'\brecieve\b',  # Common misspelling
            r'\boccured\b',  # Common misspelling
            r'\bseperate\b',  # Common misspelling
        ]

        for pattern in error_patterns:
            if re.search(pattern, main_content, re.IGNORECASE):
                accuracy_score -= 2
                warnings.append("Potential spelling error detected")

        quality_scores['accuracy'] = max(0, accuracy_score)

        # Engagement quality (0-10 points)
        engagement_indicators = ['example', 'practice', 'exercise', 'question', 'think about', 'consider']
        engagement_score = 0

        content_lower = main_content.lower()
        for indicator in engagement_indicators:
            if indicator in content_lower:
                engagement_score += 2

        quality_scores['engagement'] = min(10, engagement_score)

        # Cultural relevance (0-5 points)
        cultural_indicators = ['nigeria', 'africa', 'local', 'cultural', 'traditional', 'community']
        cultural_score = 0

        for field in ['content', 'cultural_notes', 'summary']:
            field_content = content.get(field, '').lower()
            for indicator in cultural_indicators:
                if indicator in field_content:
                    cultural_score += 1
                    break

        quality_scores['cultural_relevance'] = min(5, cultural_score)

        # Calculate total score
        total_score = sum(quality_scores.values())
        max_possible = 100

        return {
            'score': total_score,
            'breakdown': quality_scores,
            'warnings': warnings
        }

    def _validate_subject_specific_rules(self, content: Dict[str, Any]) -> Dict[str, List[str]]:
        """Subject-specific validation rules"""

        errors = []
        warnings = []

        subject = content.get('subject', '').lower()

        if subject == 'mathematics':
            # Check for mathematical expressions
            content_text = content.get('content', '')
            has_math_symbols = any(symbol in content_text for symbol in ['²', '³', '√', 'π', 'θ', 'α', 'β', 'γ'])

            if not has_math_symbols and len(content_text) > 500:
                warnings.append("Mathematics content lacks mathematical symbols or expressions")

            # Check for formulas
            if not content.get('important_formulas') and content.get('content_type') in ['study_guide', 'reference']:
                warnings.append("Mathematics content should include important formulas")

        elif subject == 'physics':
            # Check for units and measurements
            content_text = content.get('content', '')
            physics_units = ['m/s', 'm/s²', 'kg', 'n', 'j', 'w', 'v', 'a', 'ω', 'λ', 'f']

            has_units = any(unit in content_text.lower() for unit in physics_units)
            if not has_units and len(content_text) > 500:
                warnings.append("Physics content should include units of measurement")

        elif subject == 'chemistry':
            # Check for chemical notation
            content_text = content.get('content', '')
            has_chemicals = any(pattern in content_text for pattern in ['H2O', 'CO2', 'NaCl', '→', '⇌'])

            if not has_chemicals and len(content_text) > 500:
                warnings.append("Chemistry content should include chemical formulas or reactions")

        elif subject == 'biology':
            # Check for biological terminology
            content_text = content.get('content', '')
            bio_terms = ['cell', 'dna', 'rna', 'protein', 'organism', 'species', 'evolution']

            has_bio_terms = any(term in content_text.lower() for term in bio_terms)
            if not has_bio_terms and len(content_text) > 500:
                warnings.append("Biology content should include relevant biological terminology")

        return {'errors': errors, 'warnings': warnings}

    def _check_cultural_adaptation(self, content: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check for cultural adaptation and Nigerian context"""

        warnings = []
        recommendations = []

        subject = content.get('subject', '').lower()
        content_text = content.get('content', '').lower()
        cultural_notes = content.get('cultural_notes', '').lower()

        # Check for Nigerian context
        nigerian_indicators = ['nigeria', 'nigerian', 'african', 'local', 'traditional', 'community']

        has_nigerian_context = any(indicator in content_text or indicator in cultural_notes for indicator in nigerian_indicators)

        if not has_nigerian_context:
            warnings.append("Content may benefit from Nigerian cultural context or examples")
            recommendations.append("Consider adding Nigerian examples or cultural references where appropriate")

        # Subject-specific cultural checks
        if subject == 'economics':
            economic_contexts = ['naira', 'cocoa', 'oil', 'agriculture', 'market', 'trade']
            has_local_economics = any(context in content_text for context in economic_contexts)

            if not has_local_economics:
                recommendations.append("Economics content could include Nigerian economic examples (cocoa, oil, agriculture)")

        elif subject == 'geography':
            geography_contexts = ['nigeria', 'lagos', 'abuja', 'rivers', 'plateau', 'savanna', 'rainforest']
            has_local_geography = any(context in content_text for context in geography_contexts)

            if not has_local_geography:
                recommendations.append("Geography content should include Nigerian geographical features and locations")

        elif subject == 'history':
            if 'colonial' in content_text or 'independence' in content_text:
                if 'nigeria' not in content_text and 'nigeria' not in cultural_notes:
                    recommendations.append("Historical content mentioning colonialism should include Nigerian context")

        return {'warnings': warnings, 'recommendations': recommendations}

    def _generate_improvement_recommendations(self, content: Dict[str, Any], validation_result: Dict[str, Any]) -> List[str]:
        """Generate specific improvement recommendations"""

        recommendations = []

        quality_breakdown = validation_result.get('quality_breakdown', {})

        # Structure recommendations
        if quality_breakdown.get('structure', 0) < 15:
            recommendations.append("Add clear section headers (# ## ###) to organize content better")

        # Completeness recommendations
        if quality_breakdown.get('completeness', 0) < 15:
            missing_fields = []
            if not content.get('learning_objectives'):
                missing_fields.append('learning objectives')
            if not content.get('worked_examples'):
                missing_fields.append('worked examples')
            if not content.get('practice_problems'):
                missing_fields.append('practice problems')

            if missing_fields:
                recommendations.append(f"Add {', '.join(missing_fields)} to make content more complete")

        # Readability recommendations
        if quality_breakdown.get('readability', 0) < 15:
            recommendations.append("Break long sentences and paragraphs for better readability")

        # Engagement recommendations
        if quality_breakdown.get('engagement', 0) < 5:
            recommendations.append("Add interactive elements like examples, questions, or practice exercises")

        # Quality score based recommendations
        overall_score = validation_result.get('quality_score', 0)
        if overall_score < 50:
            recommendations.append("Content needs significant improvement - consider rewriting with clear structure and examples")
        elif overall_score < 70:
            recommendations.append("Content is acceptable but could be enhanced with more examples and better organization")
        elif overall_score >= 80:
            recommendations.append("High-quality content - consider using as a template for similar topics")

        return recommendations

    def batch_validate_content(self, content_list: List[Dict[str, Any]], output_file: str = None) -> Dict[str, Any]:
        """Batch validate multiple content items"""

        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"validation_reports/batch_validation_{timestamp}.json"

        os.makedirs('validation_reports', exist_ok=True)

        batch_results = {
            'batch_timestamp': datetime.now().isoformat(),
            'total_items': len(content_list),
            'validation_summary': {
                'valid_items': 0,
                'invalid_items': 0,
                'average_quality_score': 0,
                'quality_score_distribution': {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
            },
            'detailed_results': [],
            'common_issues': [],
            'recommendations': []
        }

        total_quality_score = 0

        for i, content in enumerate(content_list):
            print(f"Validating content {i+1}/{len(content_list)}: {content.get('title', 'Untitled')}")

            validation_result = self.validate_content(content)

            batch_results['detailed_results'].append({
                'content_id': content.get('id', f'item_{i+1}'),
                'title': content.get('title', 'Untitled'),
                'validation_result': validation_result
            })

            if validation_result['is_valid']:
                batch_results['validation_summary']['valid_items'] += 1
            else:
                batch_results['validation_summary']['invalid_items'] += 1

            quality_score = validation_result['quality_score']
            total_quality_score += quality_score

            # Categorize quality
            if quality_score >= 80:
                batch_results['validation_summary']['quality_score_distribution']['excellent'] += 1
            elif quality_score >= 60:
                batch_results['validation_summary']['quality_score_distribution']['good'] += 1
            elif quality_score >= 40:
                batch_results['validation_summary']['quality_score_distribution']['fair'] += 1
            else:
                batch_results['validation_summary']['quality_score_distribution']['poor'] += 1

        # Calculate average
        if content_list:
            batch_results['validation_summary']['average_quality_score'] = total_quality_score / len(content_list)

        # Analyze common issues
        all_errors = []
        all_warnings = []

        for result in batch_results['detailed_results']:
            validation = result['validation_result']
            all_errors.extend(validation['errors'])
            all_warnings.extend(validation['warnings'])

        # Find most common issues
        error_counts = Counter(all_errors)
        warning_counts = Counter(all_warnings)

        batch_results['common_issues'] = {
            'top_errors': error_counts.most_common(5),
            'top_warnings': warning_counts.most_common(5)
        }

        # Generate batch recommendations
        batch_results['recommendations'] = self._generate_batch_recommendations(batch_results)

        # Save results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(batch_results, f, indent=2, ensure_ascii=False)

        print(f"✅ Batch validation completed. Report saved to: {output_file}")
        return batch_results

    def _generate_batch_recommendations(self, batch_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations for the batch"""

        recommendations = []

        summary = batch_results['validation_summary']

        if summary['invalid_items'] > summary['valid_items']:
            recommendations.append("Majority of content items have validation errors - focus on fixing critical issues first")

        avg_score = summary['average_quality_score']
        if avg_score < 50:
            recommendations.append("Overall content quality is low - consider comprehensive review and improvement process")
        elif avg_score < 70:
            recommendations.append("Content quality is acceptable but could be significantly improved")

        # Check quality distribution
        excellent_count = summary['quality_score_distribution']['excellent']
        if excellent_count > 0:
            recommendations.append(f"{excellent_count} items are high-quality - use these as templates for improving others")

        # Common issues recommendations
        common_issues = batch_results['common_issues']
        if common_issues['top_errors']:
            top_error = common_issues['top_errors'][0]
            recommendations.append(f"Address most common error: '{top_error[0]}' (appears {top_error[1]} times)")

        return recommendations

def main():
    """Command-line interface for content validation"""

    validator = ContentValidator()

    parser = argparse.ArgumentParser(description='Content Validation and Quality Assurance')
    parser.add_argument('--validate-file', type=str, help='Validate single content file (JSON)')
    parser.add_argument('--batch-validate', type=str, help='Batch validate content from JSON file')
    parser.add_argument('--validate-content', type=str, help='Validate content from command line (JSON string)')
    parser.add_argument('--strict-mode', action='store_true', help='Use strict validation mode')
    parser.add_argument('--output-report', type=str, help='Output file for validation report')

    args = parser.parse_args()

    if args.validate_file:
        # Validate single file
        if not os.path.exists(args.validate_file):
            print(f"❌ File not found: {args.validate_file}")
            return

        with open(args.validate_file, 'r', encoding='utf-8') as f:
            content = json.load(f)

        result = validator.validate_content(content, strict_mode=args.strict_mode)

        print("📋 Validation Results:")
        print(f"✅ Valid: {result['is_valid']}")
        print(f"📊 Quality Score: {result['quality_score']}/100")

        if result['errors']:
            print(f"❌ Errors ({len(result['errors'])}):")
            for error in result['errors']:
                print(f"  - {error}")

        if result['warnings']:
            print(f"⚠️  Warnings ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"  - {warning}")

        if result['recommendations']:
            print(f"💡 Recommendations ({len(result['recommendations'])}):")
            for rec in result['recommendations']:
                print(f"  - {rec}")

        # Save detailed report if requested
        if args.output_report:
            with open(args.output_report, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"📄 Detailed report saved to: {args.output_report}")

    elif args.batch_validate:
        # Batch validate
        if not os.path.exists(args.batch_validate):
            print(f"❌ File not found: {args.batch_validate}")
            return

        with open(args.batch_validate, 'r', encoding='utf-8') as f:
            content_list = json.load(f)

        if not isinstance(content_list, list):
            print("❌ Batch validation file must contain a list of content items")
            return

        output_file = args.output_report or f"batch_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        results = validator.batch_validate_content(content_list, output_file)

        print("📊 Batch Validation Summary:")
        print(f"📁 Total items: {results['validation_summary']['total_items']}")
        print(f"✅ Valid items: {results['validation_summary']['valid_items']}")
        print(f"❌ Invalid items: {results['validation_summary']['invalid_items']}")
        print(f"📊 Average quality score: {results['validation_summary']['average_quality_score']:.1f}/100")

        quality_dist = results['validation_summary']['quality_score_distribution']
        print("📈 Quality distribution:")
        print(f"  🏆 Excellent (80+): {quality_dist['excellent']}")
        print(f"  ✅ Good (60-79): {quality_dist['good']}")
        print(f"  ⚠️  Fair (40-59): {quality_dist['fair']}")
        print(f"  ❌ Poor (<40): {quality_dist['poor']}")

        if results['recommendations']:
            print("💡 Batch recommendations:")
            for rec in results['recommendations']:
                print(f"  - {rec}")

    elif args.validate_content:
        # Validate from command line
        try:
            content = json.loads(args.validate_content)
            result = validator.validate_content(content, strict_mode=args.strict_mode)

            print("📋 Validation Results:")
            print(f"✅ Valid: {result['is_valid']}")
            print(f"📊 Quality Score: {result['quality_score']}/100")

            if result['errors']:
                print(f"❌ Errors: {result['errors']}")

            if result['warnings']:
                print(f"⚠️  Warnings: {result['warnings']}")

        except json.JSONDecodeError:
            print("❌ Invalid JSON content provided")

    else:
        # Interactive mode
        print("🔍 Content Validation and Quality Assurance")
        print("=" * 50)

        while True:
            print("\nOptions:")
            print("1. Validate single content file")
            print("2. Batch validate content files")
            print("3. Validate content from JSON string")
            print("4. Exit")

            choice = input("\nSelect option (1-4): ").strip()

            if choice == "1":
                file_path = input("Content file path (JSON): ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)

                    result = validator.validate_content(content)
                    print(f"✅ Valid: {result['is_valid']}")
                    print(f"📊 Quality Score: {result['quality_score']}/100")

                    if result['errors']:
                        print("❌ Errors:")
                        for error in result['errors']:
                            print(f"  - {error}")

                    if result['recommendations']:
                        print("💡 Recommendations:")
                        for rec in result['recommendations'][:3]:
                            print(f"  - {rec}")
                else:
                    print("❌ File not found")

            elif choice == "2":
                file_path = input("Batch content file path (JSON array): ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_list = json.load(f)

                    if isinstance(content_list, list):
                        results = validator.batch_validate_content(content_list)
                        print(f"📊 Validated {len(content_list)} items")
                        print(f"✅ Valid: {results['validation_summary']['valid_items']}")
                        print(f"❌ Invalid: {results['validation_summary']['invalid_items']}")
                        print(f"📊 Avg Quality: {results['validation_summary']['average_quality_score']:.1f}/100")
                    else:
                        print("❌ File must contain a JSON array")
                else:
                    print("❌ File not found")

            elif choice == "3":
                json_str = input("Content JSON: ").strip()
                try:
                    content = json.loads(json_str)
                    result = validator.validate_content(content)
                    print(f"✅ Valid: {result['is_valid']}")
                    print(f"📊 Quality Score: {result['quality_score']}/100")
                except json.JSONDecodeError:
                    print("❌ Invalid JSON")

            elif choice == "4":
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid option")

if __name__ == "__main__":
    main()