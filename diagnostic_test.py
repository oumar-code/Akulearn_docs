#!/usr/bin/env python3
"""Diagnostic script to test batch generation"""

import sys
import traceback

print("🔍 Diagnostic Test for Batch 4 Generation\n")

# Test 1: Import checks
print("Test 1: Checking imports...")
try:
    from curriculum_expander import CurriculumExpander
    print("  ✅ curriculum_expander imported")
except Exception as e:
    print(f"  ❌ curriculum_expander error: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from deployment_orchestrator import DeploymentOrchestrator
    print("  ✅ deployment_orchestrator imported")
except Exception as e:
    print(f"  ❌ deployment_orchestrator error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Initialize components
print("\nTest 2: Initializing components...")
try:
    expander = CurriculumExpander()
    print("  ✅ CurriculumExpander initialized")
except Exception as e:
    print(f"  ❌ CurriculumExpander error: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    orchestrator = DeploymentOrchestrator()
    print("  ✅ DeploymentOrchestrator initialized")
except Exception as e:
    print(f"  ❌ DeploymentOrchestrator error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Get batch 4 topics
print("\nTest 3: Getting Batch 4 topics...")
try:
    topics = expander.HIGH_PRIORITY_REMAINING
    print(f"  ✅ {len(topics)} Batch 4 topics found")
    for i, (subject, topic, difficulty) in enumerate(topics, 1):
        print(f"     {i}. {subject} - {topic}")
except Exception as e:
    print(f"  ❌ Error getting topics: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 4: Generate single lesson
print("\nTest 4: Generating sample lesson...")
try:
    gen = expander.generator
    test_topics = [topics[0]]  # Just first topic
    lessons = gen.generate_batch(topics=test_topics)
    print(f"  ✅ Generated {len(lessons)} lesson")
    if lessons:
        print(f"     Title: {lessons[0].get('title')}")
        print(f"     Duration: {lessons[0].get('duration_minutes')} min")
except Exception as e:
    print(f"  ❌ Generation error: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All diagnostic tests passed!")
print("\nYou can now run: python run_batch4_generation.py")
