#!/usr/bin/env python3
"""
Content Validation and Quality Assurance Script
Validates the quality and integrity of educational content in the Akulearn platform.
"""

import json
import re
from collections import defaultdict

def validate_content_structure():
    """
    Validate the structure and quality of content items.
    """
    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: content_data.json not found")
        return False

    content_items = data.get('content', [])
    print(f"🔍 Validating {len(content_items)} content items...")

    validation_results = {
        'total_items': len(content_items),
        'valid_items': 0,
        'invalid_items': 0,
        'issues': defaultdict(int),
        'subject_breakdown': defaultdict(int),
        'level_breakdown': defaultdict(int)
    }

    required_fields = [
        'id', 'title', 'subject', 'level', 'curriculum_framework',
        'learning_objectives', 'content', 'learning_options',
        'practice_problems', 'exam_preparation'
    ]

    for item in content_items:
        is_valid = True
        issues = []

        # Check required fields
        for field in required_fields:
            if field not in item:
                issues.append(f"Missing required field: {field}")
                is_valid = False

        # Validate ID format
        if 'id' in item:
            id_pattern = r'nerdc-[a-z-]+-ss[1-3]-[a-z0-9-]+\d{8}-\d{6}'
            if not re.match(id_pattern, item['id']):
                issues.append("Invalid ID format")
                is_valid = False

        # Validate subject
        if 'subject' in item:
            valid_subjects = [
                'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English Language',
                'Further Mathematics', 'Geography', 'Economics', 'Computer Science'
            ]
            if item['subject'] not in valid_subjects:
                issues.append(f"Invalid subject: {item['subject']}")
                is_valid = False

        # Validate level
        if 'level' in item:
            if item['level'] not in ['SS1', 'SS2', 'SS3']:
                issues.append(f"Invalid level: {item['level']}")
                is_valid = False

        # Validate learning objectives
        if 'learning_objectives' in item:
            if not isinstance(item['learning_objectives'], list) or len(item['learning_objectives']) < 2:
                issues.append("Insufficient learning objectives")
                is_valid = False

        # Validate learning options
        if 'learning_options' in item:
            required_options = ['visual', 'kinesthetic', 'auditory', 'reading_writing']
            for option in required_options:
                if option not in item['learning_options']:
                    issues.append(f"Missing learning option: {option}")
                    is_valid = False

        # Validate practice problems
        if 'practice_problems' in item:
            required_levels = ['basic', 'intermediate', 'advanced']
            for level in required_levels:
                if level not in item['practice_problems']:
                    issues.append(f"Missing practice problems level: {level}")
                    is_valid = False

        # Check content length
        if 'content' in item:
            if len(item['content']) < 500:
                issues.append("Content too short (minimum 500 characters)")
                is_valid = False

        # Check for NERDC alignment
        if 'curriculum_framework' in item:
            if 'NERDC' not in item['curriculum_framework']:
                issues.append("Not aligned with NERDC curriculum")
                is_valid = False

        # Update validation results
        if is_valid:
            validation_results['valid_items'] += 1
        else:
            validation_results['invalid_items'] += 1
            for issue in issues:
                validation_results['issues'][issue] += 1

        # Update breakdowns
        if 'subject' in item:
            validation_results['subject_breakdown'][item['subject']] += 1
        if 'level' in item:
            validation_results['level_breakdown'][item['level']] += 1

    return validation_results

def check_content_quality():
    """
    Perform quality checks on content.
    """
    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: content_data.json not found")
        return False

    content_items = data.get('content', [])
    quality_metrics = {
        'total_content_length': 0,
        'average_objectives': 0,
        'learning_options_completeness': 0,
        'practice_problems_count': 0,
        'has_real_applications': 0,
        'has_career_connections': 0,
        'has_waec_prep': 0
    }

    for item in content_items:
        # Content length
        if 'content' in item:
            quality_metrics['total_content_length'] += len(item['content'])

        # Learning objectives count
        if 'learning_objectives' in item:
            quality_metrics['average_objectives'] += len(item['learning_objectives'])

        # Learning options completeness
        if 'learning_options' in item:
            options = item['learning_options']
            if all(key in options for key in ['visual', 'kinesthetic', 'auditory', 'reading_writing']):
                quality_metrics['learning_options_completeness'] += 1

        # Practice problems count
        if 'practice_problems' in item:
            for level in ['basic', 'intermediate', 'advanced']:
                if level in item['practice_problems']:
                    quality_metrics['practice_problems_count'] += len(item['practice_problems'][level])

        # Real applications
        if 'real_applications' in item or 'Real-Life Applications' in item.get('content', ''):
            quality_metrics['has_real_applications'] += 1

        # Career connections
        if 'career_connections' in item:
            quality_metrics['has_career_connections'] += 1

        # WAEC preparation
        if 'exam_preparation' in item and 'waec' in str(item['exam_preparation']).lower():
            quality_metrics['has_waec_prep'] += 1

    # Calculate averages
    total_items = len(content_items)
    if total_items > 0:
        quality_metrics['average_content_length'] = quality_metrics['total_content_length'] / total_items
        quality_metrics['average_objectives'] = quality_metrics['average_objectives'] / total_items
        quality_metrics['learning_options_percentage'] = (quality_metrics['learning_options_completeness'] / total_items) * 100
        quality_metrics['real_applications_percentage'] = (quality_metrics['has_real_applications'] / total_items) * 100
        quality_metrics['career_connections_percentage'] = (quality_metrics['has_career_connections'] / total_items) * 100
        quality_metrics['waec_prep_percentage'] = (quality_metrics['has_waec_prep'] / total_items) * 100

    return quality_metrics

def generate_validation_report():
    """
    Generate a comprehensive validation and quality report.
    """
    print("🔍 AKULEARN CONTENT VALIDATION & QUALITY REPORT")
    print("=" * 60)

    # Structure validation
    print("\n📋 STRUCTURE VALIDATION:")
    validation_results = validate_content_structure()

    if validation_results:
        print(f"Total Items: {validation_results['total_items']}")
        print(f"Valid Items: {validation_results['valid_items']}")
        print(f"Invalid Items: {validation_results['invalid_items']}")
        print(f"Validation Rate: {(validation_results['valid_items'] / validation_results['total_items'] * 100):.1f}%")
        if validation_results['issues']:
            print("\nIssues Found:")
            for issue, count in sorted(validation_results['issues'].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {issue}: {count} items")

        print("\nSubject Breakdown:")
        for subject, count in sorted(validation_results['subject_breakdown'].items()):
            print(f"  {subject}: {count} items")

        print("\nLevel Breakdown:")
        for level, count in sorted(validation_results['level_breakdown'].items()):
            print(f"  {level}: {count} items")

    # Quality metrics
    print("\n📊 QUALITY METRICS:")
    quality_metrics = check_content_quality()

    if quality_metrics:
        print(f"Average Content Length: {quality_metrics.get('average_content_length', 0):.0f} characters")
        print(f"Average Learning Objectives: {quality_metrics.get('average_objectives', 0):.1f}")
        print(f"Learning Options Completeness: {quality_metrics.get('learning_options_percentage', 0):.1f}%")
        print(f"Real Applications Coverage: {quality_metrics.get('real_applications_percentage', 0):.1f}%")
        print(f"Career Connections Coverage: {quality_metrics.get('career_connections_percentage', 0):.1f}%")
        print(f"WAEC Preparation Coverage: {quality_metrics.get('waec_prep_percentage', 0):.1f}%")
        print(f"Total Practice Problems: {quality_metrics.get('practice_problems_count', 0)}")
    print("\n✅ Validation Complete!")

if __name__ == '__main__':
    generate_validation_report()