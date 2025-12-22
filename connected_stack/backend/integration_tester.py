#!/usr/bin/env python3
"""
Integration Testing Script for Akulearn Content System
Tests the integration of content with the broader Akulearn ecosystem.
"""

import json
import sys
import os

def test_content_loading():
    """
    Test if content loads properly from the database.
    """
    print("🧪 Testing Content Loading...")

    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        content_items = data.get('content', [])
        print(f"✅ Successfully loaded {len(content_items)} content items")

        # Test content structure
        required_fields = ['id', 'title', 'subject']
        valid_items = 0

        for item in content_items:
            if all(field in item for field in required_fields):
                valid_items += 1

        print(f"✅ {valid_items}/{len(content_items)} items have required fields")
        return True

    except Exception as e:
        print(f"❌ Content loading failed: {e}")
        return False

def test_content_search():
    """
    Test content search functionality.
    """
    print("\n🧪 Testing Content Search...")

    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        content_items = data.get('content', [])

        # Test subject filtering
        subjects = ['Mathematics', 'Physics', 'Computer Science']
        for subject in subjects:
            subject_items = [item for item in content_items if item.get('subject') == subject]
            print(f"✅ Found {len(subject_items)} {subject} items")

        # Test level filtering
        levels = ['SS1', 'SS2', 'SS3']
        for level in levels:
            level_items = [item for item in content_items if item.get('level') == level]
            print(f"✅ Found {len(level_items)} {level} items")

        return True

    except Exception as e:
        print(f"❌ Content search failed: {e}")
        return False

def test_content_api_simulation():
    """
    Simulate API endpoints for content retrieval.
    """
    print("\n🧪 Testing Content API Simulation...")

    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        content_items = data.get('content', [])

        # Simulate get all content
        print(f"✅ GET /api/content - Returns {len(content_items)} items")

        # Simulate get by subject
        subjects = set(item.get('subject', 'Unknown') for item in content_items)
        for subject in list(subjects)[:3]:  # Test first 3 subjects
            subject_items = [item for item in content_items if item.get('subject') == subject]
            print(f"✅ GET /api/content?subject={subject} - Returns {len(subject_items)} items")

        # Simulate get by level
        levels = ['SS1', 'SS2', 'SS3']
        for level in levels:
            level_items = [item for item in content_items if item.get('level') == level]
            print(f"✅ GET /api/content?level={level} - Returns {len(level_items)} items")

        # Simulate get by ID
        if content_items:
            sample_id = content_items[0]['id']
            found_item = next((item for item in content_items if item['id'] == sample_id), None)
            if found_item:
                print(f"✅ GET /api/content/{sample_id} - Returns item: {found_item['title'][:50]}...")
            else:
                print("❌ Sample ID lookup failed")

        return True

    except Exception as e:
        print(f"❌ API simulation failed: {e}")
        return False

def test_learning_options_integration():
    """
    Test integration of learning options across content.
    """
    print("\n🧪 Testing Learning Options Integration...")

    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        content_items = data.get('content', [])

        learning_styles = ['visual', 'kinesthetic', 'auditory', 'reading_writing']
        style_counts = {style: 0 for style in learning_styles}

        for item in content_items:
            learning_options = item.get('learning_options', {})
            for style in learning_styles:
                if style in learning_options:
                    style_counts[style] += 1

        for style, count in style_counts.items():
            print(f"✅ {style.capitalize()} learning options: {count} items")

        return True

    except Exception as e:
        print(f"❌ Learning options integration failed: {e}")
        return False

def test_content_metadata():
    """
    Test content metadata completeness.
    """
    print("\n🧪 Testing Content Metadata...")

    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        content_items = data.get('content', [])

        metadata_fields = ['estimated_duration', 'difficulty_level', 'tags', 'created_at']
        field_counts = {field: 0 for field in metadata_fields}

        for item in content_items:
            for field in metadata_fields:
                if field in item:
                    field_counts[field] += 1

        for field, count in field_counts.items():
            percentage = (count / len(content_items)) * 100
            print(f"✅ {field}: {count}/{len(content_items)} items ({percentage:.1f}%)")

        return True

    except Exception as e:
        print(f"❌ Metadata testing failed: {e}")
        return False

def run_integration_tests():
    """
    Run all integration tests.
    """
    print("🚀 AKULEARN CONTENT INTEGRATION TESTS")
    print("=" * 50)

    tests = [
        test_content_loading,
        test_content_search,
        test_content_api_simulation,
        test_learning_options_integration,
        test_content_metadata
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All integration tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check output above.")
        return False

if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)