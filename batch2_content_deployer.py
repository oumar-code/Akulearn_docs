#!/usr/bin/env python3
"""
Deploy Batch 2 Content to Wave 3 Platform
Takes batch2_content.json and imports all lessons into wave3_content_database.json
"""

import json
from pathlib import Path
from datetime import datetime

def deploy_batch2():
    print("\n" + "=" * 70)
    print("BATCH 2 DEPLOYMENT TO WAVE 3 PLATFORM")
    print("=" * 70)
    
    # Load batch 2 content
    print("\n📥 Loading batch 2 content...")
    with open("generated_content/batch2_content.json") as f:
        batch2 = json.load(f)
    
    batch2_items = batch2.get("content", [])
    print(f"   Found {len(batch2_items)} lessons")
    
    # Load existing database
    print("\n📂 Loading existing Wave 3 database...")
    with open("wave3_content_database.json") as f:
        database = json.load(f)
    
    existing_count = database["metadata"]["total_items"]
    print(f"   Existing items: {existing_count}")
    
    # Transform and merge batch 2 items
    print("\n🔄 Transforming and merging batch 2 content...")
    
    added_items = 0
    added_by_subject = {}
    
    for item in batch2_items:
        # Transform to Wave 3 schema
        wave3_item = {
            "id": item.get("id"),
            "title": item.get("title"),
            "subject": item.get("subject"),
            "topic": item.get("topic"),
            "difficulty": item.get("difficulty"),
            "exam_weight": item.get("exam_weight", "high"),
            "read_time_minutes": item.get("read_time_minutes", item.get("estimated_read_time", 25)),
            "content": item.get("content", item.get("content_summary", "")),
            "summary": item.get("content_summary", ""),
            "learning_objectives": item.get("learning_objectives", []),
            "prerequisites": item.get("prerequisites", []),
            "diagrams": item.get("diagrams", []),
            "tags": item.get("tags", []),
            "nigerian_context": item.get("nigerian_context", ""),
            "views": 0,
            "likes": 0,
            "ratings": 0,
            "created_at": datetime.now().isoformat(),
            "status": "published"
        }
        
        # Add to database
        database["content_items"].append(wave3_item)
        added_items += 1
        
        subject = item.get("subject")
        added_by_subject[subject] = added_by_subject.get(subject, 0) + 1
        
        print(f"   ✓ {wave3_item['title']}")
    
    # Update metadata
    new_total = existing_count + added_items
    database["metadata"]["total_items"] = new_total
    database["metadata"]["last_updated"] = datetime.now().isoformat()
    
    # Save updated database
    print("\n💾 Saving updated database...")
    with open("wave3_content_database.json", "w") as f:
        json.dump(database, f, indent=2)
    
    print(f"   ✅ Database saved: wave3_content_database.json")
    
    # Print summary
    print("\n" + "=" * 70)
    print("DEPLOYMENT STATISTICS")
    print("=" * 70)
    print(f"\n📊 Total items in database: {new_total}")
    print(f"   - Existing items: {existing_count}")
    print(f"   - New batch 2 items: {added_items}")
    
    print(f"\n📚 New items by subject:")
    for subject, count in sorted(added_by_subject.items()):
        print(f"   - {subject}: {count}")
    
    print(f"\n✅ BATCH 2 DEPLOYMENT COMPLETE")
    print("=" * 70)
    
    print("\nNext steps:")
    print("1. Start Wave 3 API server: python wave3_advanced_platform.py")
    print("2. Access API docs: http://localhost:8000/api/docs")
    print("3. Test content endpoints: http://localhost:8000/api/v3/content")
    print("4. View in dashboards: student_dashboard_enhanced.html")

if __name__ == "__main__":
    deploy_batch2()
