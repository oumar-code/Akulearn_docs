#!/usr/bin/env python3
"""Direct batch 4 generation test"""

import json
import logging
from pathlib import Path
from datetime import datetime
import sys

# Configure logging to show everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('batch4_debug.log')
    ]
)
logger = logging.getLogger(__name__)

print("="*70)
print("🚀 BATCH 4 GENERATION & DEPLOYMENT - DIRECT TEST")
print("="*70 + "\n")

try:
    print("Step 1: Importing modules...")
    from curriculum_expander import CurriculumExpander
    from deployment_orchestrator import DeploymentOrchestrator
    print("✅ Imports successful\n")
    
    print("Step 2: Initializing curriculum expander...")
    expander = CurriculumExpander()
    batch4_topics = expander.HIGH_PRIORITY_REMAINING
    print(f"✅ Expander initialized with {len(batch4_topics)} topics\n")
    
    print("Step 3: Generating Batch 4 lessons...")
    lessons = expander.expand_next_batch()
    print(f"✅ Generated {len(lessons)} lessons")
    print(f"   Total duration: {expander.generator.total_duration} minutes\n")
    
    print("Step 4: Preparing deployment...")
    batch_data = {
        "metadata": {
            "generatedAt": datetime.now().isoformat(),
            "batch": "Batch 4",
            "count": len(lessons),
            "totalDuration": expander.generator.total_duration
        },
        "lessons": lessons
    }
    print("✅ Batch data prepared\n")
    
    print("Step 5: Initializing orchestrator...")
    orchestrator = DeploymentOrchestrator()
    print("✅ Orchestrator initialized\n")
    
    print("Step 6: Deploying batch...")
    if orchestrator.deploy_batch(batch_data, "Batch 4"):
        print("✅ Deployment successful\n")
        
        print("Step 7: Printing summary...")
        orchestrator.print_deployment_summary()
        
        print("Step 8: Committing to git...")
        if orchestrator.commit_to_git("Batch 4"):
            print("✅ Git commit successful\n")
        
        print("="*70)
        print("✅ BATCH 4 GENERATION COMPLETE!")
        print("="*70)
        exit(0)
    else:
        print("❌ Deployment failed")
        exit(1)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
