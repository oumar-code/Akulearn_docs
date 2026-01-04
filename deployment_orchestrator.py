#!/usr/bin/env python3
"""
Deployment Orchestrator
Manages content deployment, database updates, and version control
"""

import json
import logging
import subprocess
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DeploymentOrchestrator:
    """Orchestrates content deployment and versioning"""
    
    def __init__(self, db_path: str = "generated_content/wave3_content_database.json"):
        self.db_path = db_path
        self.deployment_log = []
        self.load_database()
    
    def load_database(self) -> bool:
        """Load existing database"""
        
        try:
            if Path(self.db_path).exists():
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.database = json.load(f)
                
                logger.info(f"✅ Database loaded: {len(self.database.get('lessons', []))} lessons")
                return True
            else:
                # Initialize empty database
                self.database = {
                    "metadata": {
                        "version": "3.0",
                        "created": datetime.now().isoformat(),
                        "total_lessons": 0,
                        "coverage": {}
                    },
                    "lessons": []
                }
                logger.info("📝 Initialized new database")
                return True
        
        except Exception as e:
            logger.error(f"❌ Error loading database: {e}")
            return False
    
    def deploy_batch(self, batch_data: Dict[str, Any], batch_name: str) -> bool:
        """Deploy a batch of lessons to database"""
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 DEPLOYMENT - Batch: {batch_name}")
        logger.info(f"{'='*60}\n")
        
        lessons = batch_data.get("lessons", [])
        logger.info(f"📦 Deploying {len(lessons)} lessons...")
        
        try:
            # Add lessons to database
            added_count = 0
            updated_count = 0
            
            for lesson in lessons:
                lesson_id = lesson.get("id")
                
                # Check if lesson exists
                existing = self._find_lesson(lesson_id)
                
                if existing:
                    # Update existing
                    lesson["updated_at"] = datetime.now().isoformat()
                    updated_count += 1
                    logger.debug(f"  📝 Updated: {lesson.get('title')}")
                else:
                    # Add new
                    lesson["created_at"] = datetime.now().isoformat()
                    lesson["updated_at"] = datetime.now().isoformat()
                    self.database["lessons"].append(lesson)
                    added_count += 1
                    logger.info(f"  ✅ Added: {lesson.get('title')}")
            
            # Update metadata
            self._update_metadata(batch_data)
            
            # Save database
            if self._save_database():
                self.deployment_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "batch": batch_name,
                    "added": added_count,
                    "updated": updated_count,
                    "status": "SUCCESS"
                })
                
                logger.info(f"\n✅ Batch deployed successfully!")
                logger.info(f"   Added: {added_count}, Updated: {updated_count}")
                
                return True
            else:
                return False
        
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            self.deployment_log.append({
                "timestamp": datetime.now().isoformat(),
                "batch": batch_name,
                "status": "FAILED",
                "error": str(e)
            })
            return False
    
    def _find_lesson(self, lesson_id: str) -> Dict[str, Any] | None:
        """Find lesson in database"""
        
        for lesson in self.database.get("lessons", []):
            if lesson.get("id") == lesson_id:
                return lesson
        return None
    
    def _update_metadata(self, batch_data: Dict):
        """Update database metadata"""
        
        metadata = self.database.get("metadata", {})
        
        # Update totals
        metadata["total_lessons"] = len(self.database.get("lessons", []))
        metadata["last_updated"] = datetime.now().isoformat()
        
        # Update coverage stats
        coverage = metadata.get("coverage", {})
        
        for lesson in batch_data.get("lessons", []):
            subject = lesson.get("subject")
            if subject not in coverage:
                coverage[subject] = {"count": 0, "percent": 0}
            
            coverage[subject]["count"] += 1
        
        # Calculate percentages
        total = metadata["total_lessons"]
        for subject in coverage:
            coverage[subject]["percent"] = round(
                (coverage[subject]["count"] / total * 100) if total > 0 else 0, 1
            )
        
        metadata["coverage"] = coverage
        self.database["metadata"] = metadata
    
    def _save_database(self) -> bool:
        """Save database to file"""
        
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Database saved: {self.db_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error saving database: {e}")
            return False
    
    def get_coverage_stats(self) -> Dict[str, Any]:
        """Get current coverage statistics"""
        
        lessons = self.database.get("lessons", [])
        subjects = {}
        
        for lesson in lessons:
            subject = lesson.get("subject")
            if subject not in subjects:
                subjects[subject] = []
            subjects[subject].append(lesson.get("topic"))
        
        stats = {
            "total_lessons": len(lessons),
            "total_subjects": len(subjects),
            "by_subject": {
                subject: len(topics)
                for subject, topics in subjects.items()
            }
        }
        
        # Calculate total expected (WAEC)
        total_expected = sum([12, 12, 10, 10, 5, 2, 1])  # WAEC totals
        coverage_percent = round((len(lessons) / total_expected * 100), 1)
        stats["waec_coverage_percent"] = coverage_percent
        
        return stats
    
    def print_deployment_summary(self):
        """Print deployment summary"""
        
        if not self.deployment_log:
            logger.info("❌ No deployments recorded")
            return
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 DEPLOYMENT SUMMARY")
        logger.info(f"{'='*60}\n")
        
        for log_entry in self.deployment_log:
            timestamp = log_entry.get("timestamp", "UNKNOWN")
            batch = log_entry.get("batch", "UNKNOWN")
            status = log_entry.get("status", "UNKNOWN")
            
            if status == "SUCCESS":
                added = log_entry.get("added", 0)
                updated = log_entry.get("updated", 0)
                logger.info(f"✅ {batch} ({timestamp})")
                logger.info(f"   Added: {added}, Updated: {updated}\n")
            else:
                error = log_entry.get("error", "Unknown error")
                logger.error(f"❌ {batch} ({timestamp}): {error}\n")
        
        # Print coverage
        stats = self.get_coverage_stats()
        logger.info(f"\n{'='*60}")
        logger.info(f"📈 COVERAGE STATISTICS")
        logger.info(f"{'='*60}\n")
        logger.info(f"Total lessons: {stats['total_lessons']}")
        logger.info(f"WAEC coverage: {stats['waec_coverage_percent']}%\n")
        logger.info("By subject:")
        for subject, count in stats["by_subject"].items():
            logger.info(f"  • {subject}: {count} lessons")
        
        logger.info(f"\n{'='*60}\n")
    
    def commit_to_git(self, batch_name: str) -> bool:
        """Commit deployed content to git"""
        
        logger.info(f"\n📝 Committing to Git: {batch_name}")
        
        try:
            # Stage files
            subprocess.run(
                ["git", "add", self.db_path],
                cwd=Path(self.db_path).parent,
                check=True,
                capture_output=True
            )
            
            # Commit
            commit_msg = f"Deploy {batch_name}: content deployment with {len(self.database.get('lessons', []))} lessons"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=Path(self.db_path).parent,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Committed to git: {commit_msg}")
                return True
            else:
                logger.warning(f"⚠️  Git commit may have skipped (no changes or already committed)")
                return True
        
        except Exception as e:
            logger.error(f"❌ Git commit failed: {e}")
            return False
    
    def generate_deployment_report(self, output_path: str = "generated_content/deployment_report.json") -> bool:
        """Generate deployment report"""
        
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "deployment_log": self.deployment_log,
                "current_stats": self.get_coverage_stats(),
                "database_path": self.db_path,
                "total_lessons": len(self.database.get("lessons", []))
            }
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Report saved: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error generating report: {e}")
            return False


def main():
    """Example deployment"""
    
    orchestrator = DeploymentOrchestrator()
    
    # Load generated batch
    try:
        with open("generated_content/batch4_content_complete.json", 'r') as f:
            batch_data = json.load(f)
    except FileNotFoundError:
        logger.error("❌ Batch file not found")
        return
    
    # Deploy
    if orchestrator.deploy_batch(batch_data, "Batch 4"):
        orchestrator.print_deployment_summary()
        orchestrator.generate_deployment_report()
        orchestrator.commit_to_git("Batch 4")


if __name__ == "__main__":
    main()
