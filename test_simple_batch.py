#!/usr/bin/env python3
import sys
print("Starting Batch 4 generation...", flush=True)
sys.stdout.flush()

from curriculum_expander import CurriculumExpander
print("1. Expander imported", flush=True)
sys.stdout.flush()

expander = CurriculumExpander()
print("2. Expander initialized", flush=True)
sys.stdout.flush()

lessons = expander.expand_next_batch()
print(f"3. Generated {len(lessons)} lessons", flush=True)
sys.stdout.flush()

from deployment_orchestrator import DeploymentOrchestrator
print("4. Orchestrator imported", flush=True)
sys.stdout.flush()

orchestrator = DeploymentOrchestrator()
print("5. Orchestrator initialized", flush=True)
sys.stdout.flush()

from datetime import datetime
batch_data = {
    "metadata": {
        "generatedAt": datetime.now().isoformat(),
        "batch": "Batch 4",
        "count": len(lessons)
    },
    "lessons": lessons
}

print("6. Deploying...", flush=True)
sys.stdout.flush()

if orchestrator.deploy_batch(batch_data, "Batch 4"):
    print("7. Deployment successful", flush=True)
    sys.stdout.flush()
else:
    print("7. Deployment failed", flush=True)
    sys.stdout.flush()
