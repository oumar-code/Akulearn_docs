"""
Batch 5 Content Generator - Phase 2 Core Completion
Uses MCP-enhanced generation with Brave Search + Wikipedia
"""

import json
import os
from datetime import datetime
from enhanced_content_generator import EnhancedContentGenerator

# Batch 5 topics from expansion plan (10 topics)
BATCH_5_TOPICS = [
    ("Mathematics", "Calculus - Differentiation", "Intermediate"),
    ("Mathematics", "Calculus - Integration", "Intermediate"),
    ("Mathematics", "Complex Numbers", "Intermediate"),
    ("Mathematics", "Trigonometric Functions", "Intermediate"),
    ("Mathematics", "Permutation and Combination", "Intermediate"),
    ("Mathematics", "Probability and Statistics", "Intermediate"),
    ("Physics", "Mechanics - Forces and Motion", "Intermediate"),
    ("Physics", "Work, Energy and Power", "Intermediate"),
    ("Chemistry", "Periodic Table", "Intermediate"),
    ("Chemistry", "States of Matter", "Intermediate"),
]

def generate_batch5():
    """Generate Batch 5 content with MCP enhancement"""
    
    print("\n" + "="*70)
    print("🎓 BATCH 5 GENERATION - MCP-Enhanced with Brave Search + Wikipedia")
    print("="*70)
    print(f"Topics: {len(BATCH_5_TOPICS)}")
    print(f"Expected duration: ~250 minutes")
    print(f"Research sources: Brave Search + Wikipedia")
    print("="*70 + "\n")
    
    # Initialize generator with MCP enabled
    print("Initializing MCP-enhanced generator...")
    generator = EnhancedContentGenerator(use_mcp=True)
    print("✅ Generator ready (Brave Search + Wikipedia)\n")
    
    generated_lessons = []
    successful = 0
    failed = 0
    
    # Generate each topic
    for idx, (subject, topic, difficulty) in enumerate(BATCH_5_TOPICS, 1):
        try:
            print(f"[{idx}/{len(BATCH_5_TOPICS)}] Generating: {subject} > {topic} ({difficulty})...")
            
            # Generate with MCP research
            lesson = generator.generate(
                subject=subject,
                topic=topic,
                difficulty=difficulty,
                use_mcp=True,  # Enable research-backed generation
                include_nigerian_context=True,
                exam_board="WAEC"
            )
            
            if lesson:
                generated_lessons.append(lesson)
                successful += 1
                print(f"    ✅ Generated successfully (with Brave + Wikipedia research)")
            else:
                failed += 1
                print(f"    ⚠️ Failed to generate")
                
        except Exception as e:
            failed += 1
            print(f"    ❌ Error: {str(e)[:100]}")
    
    # Save results
    output_file = "generated_content/batch5_content.json"
    os.makedirs("generated_content", exist_ok=True)
    
    result = {
        "metadata": {
            "batch": 5,
            "generated_at": datetime.now().isoformat(),
            "total_generated": successful,
            "total_failed": failed,
            "mcp_enabled": True,
            "research_sources": ["Brave Search", "Wikipedia"],
            "expected_duration_minutes": 250,
        },
        "lessons": generated_lessons
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "="*70)
    print(f"✅ BATCH 5 GENERATION COMPLETE")
    print("="*70)
    print(f"Generated: {successful}/{len(BATCH_5_TOPICS)} lessons")
    print(f"Failed: {failed}")
    print(f"Output: {output_file}")
    print(f"Size: {os.path.getsize(output_file) / 1024:.1f} KB")
    print("="*70 + "\n")
    
    return generated_lessons, output_file

def merge_batch5_to_main():
    """Merge Batch 5 into main database"""
    
    print("\n" + "="*70)
    print("📦 MERGING BATCH 5 INTO MAIN DATABASE")
    print("="*70)
    
    # Load Batch 5
    with open("generated_content/batch5_content.json", "r", encoding="utf-8") as f:
        batch5_data = json.load(f)
    
    # Load main database
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        main_db = json.load(f)
    
    # Current stats
    current_count = len(main_db["content"])
    batch5_lessons = batch5_data.get("lessons", [])
    new_count = current_count + len(batch5_lessons)
    
    print(f"Current database: {current_count} lessons")
    print(f"Batch 5 lessons: {len(batch5_lessons)} lessons")
    print(f"After merge: {new_count} lessons")
    
    # Add lessons
    main_db["content"].extend(batch5_lessons)
    
    # Update metadata
    main_db["metadata"]["last_updated"] = datetime.now().isoformat()
    main_db["metadata"]["total_items"] = new_count
    
    # Update statistics
    subjects = {}
    for lesson in main_db["content"]:
        subject = lesson.get("subject", "Unknown")
        subjects[subject] = subjects.get(subject, 0) + 1
    main_db["metadata"]["statistics"]["by_subject"] = subjects
    
    # Save merged database
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(main_db, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Merge complete!")
    print(f"   Total: {current_count} → {new_count} lessons")
    print(f"   By subject: {subjects}")
    print("="*70 + "\n")
    
    return new_count, subjects

if __name__ == "__main__":
    # Step 1: Generate Batch 5
    lessons, output_file = generate_batch5()
    
    if lessons:
        # Step 2: Merge into main database
        total, subjects = merge_batch5_to_main()
        
        print("\n🎉 BATCH 5 WORKFLOW COMPLETE!")
        print(f"✅ Database now has {total} total lessons")
        print(f"📊 Coverage: {total}/{52} WAEC topics ({total*100/52:.1f}%)")
    else:
        print("\n❌ No lessons generated - skipping merge")
