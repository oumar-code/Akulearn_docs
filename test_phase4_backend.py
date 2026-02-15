#!/usr/bin/env python3
"""Test Phase 4 Backend Integration

Tests:
1. Phase4AssetLoader initialization
2. Question retrieval (by ID, subject, type, difficulty)
3. Answer validation for all question types
4. Statistics and analytics
5. API endpoint imports
6. Quiz generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_phase4_loader_import():
    """Test 1: Import Phase4AssetLoader"""
    print("Test 1: Import Phase4AssetLoader")
    try:
        from src.backend.phase4_asset_loader import Phase4AssetLoader, initialize_phase4_loader
        print("  ✅ Phase4AssetLoader imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_loader_initialization():
    """Test 2: Initialize Phase4AssetLoader"""
    print("\nTest 2: Initialize Phase4AssetLoader")
    try:
        from src.backend.phase4_asset_loader import initialize_phase4_loader
        loader = initialize_phase4_loader("generated_assets")
        stats = loader.get_phase4_stats()
        print(f"  ✅ Loader initialized: {stats['total_questions']} questions loaded")
        return True, loader
    except Exception as e:
        print(f"  ❌ Initialization failed: {e}")
        return False, None

def test_question_retrieval(loader):
    """Test 3: Question retrieval methods"""
    print("\nTest 3: Question Retrieval")
    
    tests_passed = 0
    
    # Test get_question_by_id
    try:
        question = loader.get_question_by_id("mathematics_number_bases_multiple_choice_1")
        if question:
            print(f"  ✅ Get by ID: {question.question_id}")
            tests_passed += 1
        else:
            print("  ❌ Get by ID returned None")
    except Exception as e:
        print(f"  ❌ Get by ID failed: {e}")
    
    # Test get_questions_by_subject
    try:
        questions = loader.get_questions_by_subject("Mathematics", limit=5)
        if questions:
            print(f"  ✅ Get by subject: {len(questions)} questions")
            tests_passed += 1
        else:
            print("  ❌ Get by subject returned empty list")
    except Exception as e:
        print(f"  ❌ Get by subject failed: {e}")
    
    # Test get_questions_by_type
    try:
        questions = loader.get_questions_by_type("multiple_choice", limit=5)
        if questions:
            print(f"  ✅ Get by type: {len(questions)} questions")
            tests_passed += 1
        else:
            print("  ❌ Get by type returned empty list")
    except Exception as e:
        print(f"  ❌ Get by type failed: {e}")
    
    # Test get_questions_by_difficulty
    try:
        questions = loader.get_questions_by_difficulty("easy", limit=5)
        if questions:
            print(f"  ✅ Get by difficulty: {len(questions)} questions")
            tests_passed += 1
        else:
            print("  ❌ Get by difficulty returned empty list")
    except Exception as e:
        print(f"  ❌ Get by difficulty failed: {e}")
    
    # Test get_random_questions
    try:
        questions = loader.get_random_questions(count=5, subject="Mathematics")
        if questions:
            print(f"  ✅ Get random questions: {len(questions)} questions")
            tests_passed += 1
        else:
            print("  ❌ Get random questions returned empty list")
    except Exception as e:
        print(f"  ❌ Get random questions failed: {e}")
    
    return tests_passed == 5

def test_answer_validation(loader):
    """Test 4: Answer validation for all question types"""
    print("\nTest 4: Answer Validation")
    
    tests_passed = 0
    
    # Test multiple choice validation (correct)
    try:
        result = loader.validate_answer("mathematics_number_bases_multiple_choice_1", 1)
        if result.get("valid") and result.get("correct"):
            print(f"  ✅ MCQ validation (correct): {result.get('points_earned')} points")
            tests_passed += 1
        else:
            print(f"  ❌ MCQ validation (correct) failed: {result}")
    except Exception as e:
        print(f"  ❌ MCQ validation failed: {e}")
    
    # Test multiple choice validation (incorrect)
    try:
        result = loader.validate_answer("mathematics_number_bases_multiple_choice_1", 0)
        if result.get("valid") and not result.get("correct"):
            print(f"  ✅ MCQ validation (incorrect): 0 points")
            tests_passed += 1
        else:
            print(f"  ❌ MCQ validation (incorrect) failed: {result}")
    except Exception as e:
        print(f"  ❌ MCQ validation failed: {e}")
    
    # Test true/false validation
    try:
        result = loader.validate_answer("mathematics_number_bases_true_false_1", False)
        if result.get("valid"):
            print(f"  ✅ True/False validation: {result.get('correct')}")
            tests_passed += 1
        else:
            print(f"  ❌ True/False validation failed: {result}")
    except Exception as e:
        print(f"  ❌ True/False validation failed: {e}")
    
    # Test fill-in-blank validation
    try:
        result = loader.validate_answer("mathematics_number_bases_fill_blank_1", "base conversion")
        if result.get("valid"):
            print(f"  ✅ Fill-blank validation: {result.get('correct')}")
            tests_passed += 1
        else:
            print(f"  ❌ Fill-blank validation failed: {result}")
    except Exception as e:
        print(f"  ❌ Fill-blank validation failed: {e}")
    
    # Test matching validation
    try:
        # Get a matching question first
        questions = loader.get_questions_by_type("matching", limit=1)
        if questions:
            q_id = questions[0].question_id
            # Submit correct pairs
            correct_pairs = questions[0].question_data.get("correct_pairs", {})
            result = loader.validate_answer(q_id, correct_pairs)
            if result.get("valid"):
                print(f"  ✅ Matching validation: {result.get('correct_count')}/{result.get('total_pairs')} pairs")
                tests_passed += 1
            else:
                print(f"  ❌ Matching validation failed: {result}")
        else:
            print("  ⚠️  No matching questions available")
    except Exception as e:
        print(f"  ❌ Matching validation failed: {e}")
    
    return tests_passed >= 4

def test_statistics(loader):
    """Test 5: Statistics and analytics"""
    print("\nTest 5: Statistics and Analytics")
    
    tests_passed = 0
    
    # Test get_phase4_stats
    try:
        stats = loader.get_phase4_stats()
        if stats.get("total_questions", 0) > 0:
            print(f"  ✅ Phase 4 stats: {stats['total_questions']} questions")
            print(f"     - Question types: {stats['question_types']}")
            print(f"     - Subjects: {stats['subjects']}")
            print(f"     - Total points: {stats['total_points']}")
            print(f"     - Total time: {stats['total_time_minutes']} minutes")
            tests_passed += 1
        else:
            print(f"  ❌ Phase 4 stats failed: {stats}")
    except Exception as e:
        print(f"  ❌ Phase 4 stats failed: {e}")
    
    # Test get_subject_stats
    try:
        stats = loader.get_subject_stats("Mathematics")
        if stats.get("total_questions", 0) > 0:
            print(f"  ✅ Subject stats: {stats['total_questions']} Mathematics questions")
            tests_passed += 1
        else:
            print(f"  ❌ Subject stats failed: {stats}")
    except Exception as e:
        print(f"  ❌ Subject stats failed: {e}")
    
    return tests_passed == 2

def test_api_import():
    """Test 6: Import API router"""
    print("\nTest 6: Import API Router")
    try:
        from src.backend.api.assets_v4 import router
        print(f"  ✅ API router imported: {len(router.routes)} endpoints")
        
        # List endpoint paths
        print("     Endpoints:")
        for route in router.routes[:10]:  # Show first 10
            if hasattr(route, 'path'):
                print(f"       - {route.methods} {route.path}")
        
        return True
    except Exception as e:
        print(f"  ❌ API import failed: {e}")
        return False

def test_app_integration():
    """Test 7: Main app integration"""
    print("\nTest 7: Main App Integration")
    try:
        from src.backend.api.learning import app
        
        # Check if phase4 router is included
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        phase4_routes = [r for r in routes if '/phase4' in r]
        
        if phase4_routes:
            print(f"  ✅ Phase 4 router mounted: {len(phase4_routes)} endpoints")
            print(f"     Sample endpoints:")
            for route in phase4_routes[:5]:
                print(f"       - {route}")
            return True
        else:
            print("  ❌ Phase 4 router not found in app")
            return False
    except Exception as e:
        print(f"  ❌ App integration failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("PHASE 4 BACKEND INTEGRATION TESTS")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(test_phase4_loader_import())
    
    # Test 2: Initialization
    success, loader = test_loader_initialization()
    results.append(success)
    
    if loader:
        # Test 3: Question retrieval
        results.append(test_question_retrieval(loader))
        
        # Test 4: Answer validation
        results.append(test_answer_validation(loader))
        
        # Test 5: Statistics
        results.append(test_statistics(loader))
    else:
        print("\n⚠️  Skipping tests 3-5 due to loader initialization failure")
        results.extend([False, False, False])
    
    # Test 6: API import
    results.append(test_api_import())
    
    # Test 7: App integration
    results.append(test_app_integration())
    
    # Summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print()
    
    if passed == total:
        print("✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
