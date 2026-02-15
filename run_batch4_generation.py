#!/usr/bin/env python3
"""
Batch 4 Complete Generation & Deployment Script
Run this to generate and deploy Batch 4 content
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# Import our modules
from curriculum_expander import CurriculumExpander
from deployment_orchestrator import DeploymentOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_and_deploy_batch_4():
    """
    Complete workflow: Generate Batch 4 → Validate → Deploy
    """
    
    logger.info("\n" + "="*70)
    logger.info("🚀 BATCH 4 GENERATION & DEPLOYMENT WORKFLOW")
    logger.info("="*70 + "\n")
    
    # Step 1: Initialize curriculum expander
    logger.info("📊 Step 1: Initializing Curriculum Expander...")
    expander = CurriculumExpander()
    logger.info("✅ Curriculum expander initialized\n")
    
    # Step 2: Get Batch 4 topics
    logger.info("📋 Step 2: Preparing Batch 4 Topics...")
    batch4_topics = expander.HIGH_PRIORITY_REMAINING
    logger.info(f"✅ {len(batch4_topics)} topics ready for generation")
    for subject, topic, difficulty in batch4_topics:
        logger.info(f"   • {subject} - {topic} ({difficulty})")
    logger.info()
    
    # Step 3: Generate content
    logger.info("🎨 Step 3: Generating Batch 4 Content...")
    lessons = expander.expand_next_batch()
    logger.info(f"✅ Generated {len(lessons)} lessons")
    logger.info(f"   Total duration: {expander.generator.total_duration} minutes\n")
    
    # Step 4: Display sample lesson
    if lessons:
        logger.info("📚 Sample Generated Lesson:")
        sample = lessons[0]
        logger.info(f"   ID: {sample.get('id')}")
        logger.info(f"   Title: {sample.get('title')}")
        logger.info(f"   Subject: {sample.get('subject')}")
        logger.info(f"   Difficulty: {sample.get('difficulty')}")
        logger.info(f"   Duration: {sample.get('duration_minutes')} min")
        logger.info(f"   Objectives: {len(sample.get('learningObjectives', []))}")
        logger.info(f"   Sections: {len(sample.get('sections', []))}")
        logger.info(f"   Assessment questions: {len(sample.get('assessment', {}).get('questions', []))}\n")
    
    # Step 5: Deploy to database
    logger.info("🚀 Step 4: Deploying to Database...")
    
    # Prepare batch data
    batch_data = {
        "metadata": {
            "generatedAt": datetime.now().isoformat(),
            "batch": "Batch 4",
            "count": len(lessons),
            "totalDuration": expander.generator.total_duration
        },
        "lessons": lessons
    }
    
    # Initialize orchestrator
    orchestrator = DeploymentOrchestrator()
    
    # Deploy
    if orchestrator.deploy_batch(batch_data, "Batch 4"):
        logger.info("✅ Batch 4 deployed successfully\n")
        
        # Step 6: Print summary
        logger.info("📊 Step 5: Deployment Summary...")
        orchestrator.print_deployment_summary()
        
        # Step 7: Git commit
        logger.info("📝 Step 6: Committing to Git...")
        if orchestrator.commit_to_git("Batch 4"):
            logger.info("✅ Changes committed to git\n")
        
        # Final summary
        logger.info("="*70)
        logger.info("✅ BATCH 4 GENERATION & DEPLOYMENT COMPLETE!")
        logger.info("="*70)
        logger.info(f"\n📈 Coverage Update:")
        stats = orchestrator.get_coverage_stats()
        logger.info(f"   Total lessons: {stats['total_lessons']}")
        logger.info(f"   WAEC coverage: {stats['waec_coverage_percent']}%")
        logger.info(f"   By subject: {stats['by_subject']}")
        logger.info("\n🎯 Next steps:")
        logger.info("   1. Review generated content in generated_content/batch4_content_complete.json")
        logger.info("   2. Validate against WAEC standards")
        logger.info("   3. Check coverage improvement in wave3_content_database.json")
        logger.info("   4. Plan and execute Batch 5 (Phase 2)\n")
        
        return True
    else:
        logger.error("❌ Batch 4 deployment failed\n")
        return False


if __name__ == "__main__":
    try:
        success = generate_and_deploy_batch_4()
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
