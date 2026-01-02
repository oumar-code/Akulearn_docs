#!/usr/bin/env python3
"""
Pilot Content Deployer
Imports pilot lessons from JSON into Wave 3 content database
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class PilotContentDeployer:
    """Deploy pilot content to Wave 3 platform"""
    
    def __init__(self, 
                 pilot_file: str = "generated_content/pilot_content.json",
                 database_file: str = "wave3_content_database.json"):
        self.pilot_file = pilot_file
        self.database_file = database_file
        self.stats = {
            "total_imported": 0,
            "by_subject": {},
            "by_difficulty": {},
            "existing_items": 0,
            "new_items": 0
        }
    
    def load_existing_database(self) -> Dict[str, Any]:
        """Load existing content database"""
        if os.path.exists(self.database_file):
            try:
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading database: {e}")
                return self._create_empty_database()
        else:
            print("📝 Creating new database...")
            return self._create_empty_database()
    
    def _create_empty_database(self) -> Dict[str, Any]:
        """Create empty database structure"""
        return {
            "metadata": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "total_items": 0
            },
            "content": []
        }
    
    def load_pilot_content(self) -> List[Dict[str, Any]]:
        """Load pilot content from JSON"""
        try:
            with open(self.pilot_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("content", [])
        except FileNotFoundError:
            print(f"❌ Pilot content file not found: {self.pilot_file}")
            return []
        except Exception as e:
            print(f"❌ Error loading pilot content: {e}")
            return []
    
    def transform_pilot_item(self, pilot_item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform pilot content format to Wave 3 database format"""
        # Map pilot content structure to Wave 3 expected structure
        transformed = {
            "id": pilot_item.get("id"),
            "title": pilot_item.get("title"),
            "subject": pilot_item.get("subject"),
            "topic": pilot_item.get("topic"),
            "subtopic": pilot_item.get("subtopic", ""),
            "content_type": pilot_item.get("content_type", "study_guide"),
            "difficulty": pilot_item.get("difficulty", "intermediate"),
            "exam_board": pilot_item.get("exam_board", "WAEC"),
            
            # Content sections
            "content": pilot_item.get("content", ""),
            "summary": self._extract_summary(pilot_item.get("content", "")),
            
            # Educational metadata
            "learning_objectives": pilot_item.get("learning_objectives", []),
            "prerequisites": pilot_item.get("prerequisites", []),
            "estimated_read_time": pilot_item.get("estimated_read_time", 20),
            
            # Examples and practice
            "worked_examples": pilot_item.get("worked_examples", []),
            "practice_problems": pilot_item.get("practice_problems", []),
            
            # Media
            "diagrams": pilot_item.get("diagrams", []),
            "videos": [],
            "interactive_elements": [],
            
            # Context
            "nigerian_context": pilot_item.get("nigerian_context", ""),
            "real_world_applications": [],
            
            # Engagement metrics (initialize)
            "views": 0,
            "likes": 0,
            "completion_rate": 0.0,
            "average_rating": 0.0,
            "total_ratings": 0,
            
            # Timestamps
            "created_at": pilot_item.get("created_at", datetime.now().isoformat()),
            "updated_at": datetime.now().isoformat(),
            "status": pilot_item.get("status", "published"),
            
            # Tags
            "tags": self._generate_tags(pilot_item),
            
            # Source
            "source": "pilot_content_generator",
            "version": "1.0"
        }
        
        return transformed
    
    def _extract_summary(self, content: str, max_length: int = 200) -> str:
        """Extract a summary from the content"""
        if not content:
            return ""
        
        # Take first paragraph or first max_length characters
        lines = content.split('\n')
        summary = ""
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                summary = line
                break
        
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
        
        return summary
    
    def _generate_tags(self, pilot_item: Dict[str, Any]) -> List[str]:
        """Generate tags for the content"""
        tags = []
        
        # Subject tag
        subject = pilot_item.get("subject", "")
        if subject:
            tags.append(subject.lower())
        
        # Topic tag
        topic = pilot_item.get("topic", "")
        if topic:
            tags.append(topic.lower().replace(" ", "_"))
        
        # Difficulty tag
        difficulty = pilot_item.get("difficulty", "")
        if difficulty:
            tags.append(difficulty)
        
        # Exam board tag
        exam_board = pilot_item.get("exam_board", "")
        if exam_board:
            tags.append(exam_board.lower())
        
        # Special tags
        if pilot_item.get("diagrams"):
            tags.append("with_diagrams")
        
        if pilot_item.get("worked_examples"):
            tags.append("worked_examples")
        
        if pilot_item.get("practice_problems"):
            tags.append("practice_problems")
        
        if "nigerian" in pilot_item.get("nigerian_context", "").lower():
            tags.append("nigerian_context")
        
        return tags
    
    def merge_content(self, existing_db: Dict[str, Any], 
                      pilot_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge pilot content with existing database"""
        existing_ids = {item["id"] for item in existing_db.get("content", [])}
        
        # Transform and add pilot items
        for pilot_item in pilot_items:
            transformed = self.transform_pilot_item(pilot_item)
            
            if transformed["id"] in existing_ids:
                print(f"  ⚠️  Skipping duplicate: {transformed['title']}")
                continue
            
            existing_db["content"].append(transformed)
            self.stats["new_items"] += 1
            
            # Update stats
            subject = transformed["subject"]
            difficulty = transformed["difficulty"]
            
            self.stats["by_subject"][subject] = self.stats["by_subject"].get(subject, 0) + 1
            self.stats["by_difficulty"][difficulty] = self.stats["by_difficulty"].get(difficulty, 0) + 1
        
        # Update metadata
        existing_db["metadata"]["total_items"] = len(existing_db["content"])
        existing_db["metadata"]["last_updated"] = datetime.now().isoformat()
        
        return existing_db
    
    def save_database(self, database: Dict[str, Any]):
        """Save updated database"""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Database saved: {self.database_file}")
        except Exception as e:
            print(f"❌ Error saving database: {e}")
            raise
    
    def deploy(self):
        """Deploy pilot content to Wave 3 platform"""
        print("=" * 70)
        print("PILOT CONTENT DEPLOYMENT TO WAVE 3 PLATFORM")
        print("=" * 70)
        print()
        
        # Load pilot content
        print("📥 Loading pilot content...")
        pilot_items = self.load_pilot_content()
        if not pilot_items:
            print("❌ No pilot content to import")
            return
        print(f"   Found {len(pilot_items)} pilot lessons")
        print()
        
        # Load existing database
        print("📂 Loading existing database...")
        existing_db = self.load_existing_database()
        self.stats["existing_items"] = len(existing_db.get("content", []))
        print(f"   Existing items: {self.stats['existing_items']}")
        print()
        
        # Merge content
        print("🔄 Merging pilot content with existing database...")
        updated_db = self.merge_content(existing_db, pilot_items)
        print()
        
        # Save database
        print("💾 Saving updated database...")
        self.save_database(updated_db)
        print()
        
        # Print statistics
        self.print_statistics()
        
        print()
        print("=" * 70)
        print("DEPLOYMENT COMPLETE")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Start Wave 3 API server: python wave3_advanced_platform.py")
        print("2. Access API docs: http://localhost:8000/api/docs")
        print("3. Test content endpoints: http://localhost:8000/api/v3/content")
        print("4. View in dashboards: student_dashboard_enhanced.html")
        print()
    
    def print_statistics(self):
        """Print import statistics"""
        print("=" * 70)
        print("DEPLOYMENT STATISTICS")
        print("=" * 70)
        print()
        print(f"📊 Total items in database: {self.stats['existing_items'] + self.stats['new_items']}")
        print(f"   - Existing items: {self.stats['existing_items']}")
        print(f"   - New pilot items: {self.stats['new_items']}")
        print()
        
        if self.stats["by_subject"]:
            print("📚 New items by subject:")
            for subject, count in sorted(self.stats["by_subject"].items()):
                print(f"   - {subject}: {count}")
            print()
        
        if self.stats["by_difficulty"]:
            print("📈 New items by difficulty:")
            for difficulty, count in sorted(self.stats["by_difficulty"].items()):
                print(f"   - {difficulty.capitalize()}: {count}")
            print()


def main():
    """Main deployment"""
    deployer = PilotContentDeployer()
    deployer.deploy()


if __name__ == "__main__":
    main()
