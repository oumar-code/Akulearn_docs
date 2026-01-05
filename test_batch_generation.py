#!/usr/bin/env python3
"""Test curriculum expansion script"""

from curriculum_expander import CurriculumExpander
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    expander = CurriculumExpander()
    print("\n✅ CurriculumExpander initialized successfully\n")
    
    # Get stats
    stats = expander._get_current_stats()
    print("📊 Coverage Stats:")
    for subject, stat in stats['by_subject'].items():
        print(f"  {subject}: {stat['covered']}/{stat['total']} ({stat['percentage']:.1f}%)")
    
    # Get expansion plan
    plan = expander.get_expansion_plan()
    print(f"\n📈 Expansion Plan:")
    print(f"  Total phases: {len(plan['phases'])}")
    for i, phase in enumerate(plan['phases'], 1):
        coverage = phase.get('coverage_improvement', 'Unknown')
        target = phase.get('target_topics', '?')
        print(f"  Phase {i}: +{target} topics → {coverage}")
    
    # Get high priority topics for batch 4
    topics = expander.HIGH_PRIORITY_REMAINING
    print(f"\n🎯 Batch 4 Topics ({len(topics)} total):")
    for subject, topic, difficulty in topics:
        print(f"  • {subject} - {topic} ({difficulty})")
    
    # Generate batch
    print(f"\n🚀 Generating Batch 4 lessons...")
    lessons = expander.expand_next_batch()
    print(f"✅ Generated {len(lessons)} lessons")
    print(f"   Total duration: {expander.generator.total_duration} minutes")
    
    if lessons:
        print(f"\n📚 Sample Lesson:")
        sample = lessons[0]
        print(f"  ID: {sample.get('id')}")
        print(f"  Title: {sample.get('title')}")
        print(f"  Subject: {sample.get('subject')}")
        print(f"  Duration: {sample.get('duration_minutes')} min")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

