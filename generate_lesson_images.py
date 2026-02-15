"""
Generate SDXL images for all lessons in the database
Uses Hugging Face Inference API with stable_image_client
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

def build_image_prompt(subject: str, title: str) -> str:
    """Build an image prompt for a lesson topic"""
    return (
        f"Educational diagram showing {title} for WAEC {subject}, "
        f"clear science illustrations, classroom, readable labels, "
        f"high contrast, professional quality"
    )

def generate_lesson_images(batch_size: int = 5, skip_existing: bool = True):
    """Generate images for lessons in the database"""
    
    print("\n" + "="*70)
    print("🎨 GENERATING IMAGES FOR LESSONS")
    print("="*70)
    
    # Load database
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    lessons = db.get("content", [])
    print(f"\n📚 Found {len(lessons)} lessons")
    print(f"⚙️  Batch size: {batch_size} images")
    print(f"⏭️  Skip existing: {skip_existing}\n")
    
    # Import after confirming packages available
    try:
        from stable_image_client import generate_image
    except ImportError:
        print("❌ Error: stable_image_client not found. Please ensure it exists.")
        return 0, 0, 0
    
    images_dir = Path("generated_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    generated = 0
    skipped = 0
    failed = 0
    
    for idx, lesson in enumerate(lessons, 1):
        subject = lesson.get("subject", "Unknown")
        title = lesson.get("title", "Untitled")
        lesson_id = lesson.get("id", f"lesson_{idx}")
        
        # Skip if image already exists and skip_existing is True
        if skip_existing and "image" in lesson:
            print(f"[{idx}/{len(lessons)}] ⏭️  {subject} > {title} (already has image)")
            skipped += 1
            continue
        
        # Generate prompt
        prompt = build_image_prompt(subject, title)
        
        # Generate image
        print(f"[{idx}/{len(lessons)}] 🎨 {subject} > {title}...", end=" ", flush=True)
        
        try:
            _, image_path = generate_image(
                prompt,
                output_path=None,  # Will auto-generate filename
            )
            
            # Update lesson metadata with image
            lesson["image"] = {
                "path": image_path,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
            
            print(f"✅")
            generated += 1
            
            # Rate limiting: pause between batches
            if generated % batch_size == 0:
                print(f"\n⏸️  Pausing 30s after {batch_size} images...\n")
                time.sleep(30)
        
        except Exception as exc:
            print(f"❌ {str(exc)[:50]}")
            failed += 1
    
    # Save updated database
    print("\n" + "="*70)
    print("💾 SAVING UPDATED DATABASE")
    print("="*70)
    
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    db_size_mb = os.path.getsize("wave3_content_database.json") / (1024 * 1024)
    
    print(f"\n✅ Generated: {generated} images")
    print(f"⏭️  Skipped: {skipped} (existing)")
    print(f"❌ Failed: {failed}")
    print(f"📊 Database size: {db_size_mb:.2f} MB")
    print(f"💾 Saved to: wave3_content_database.json\n")
    
    return generated, skipped, failed

def main():
    """Main execution"""
    try:
        generated, skipped, failed = generate_lesson_images(batch_size=5, skip_existing=True)
        
        print("="*70)
        print("🎉 IMAGE GENERATION COMPLETE")
        print("="*70)
        print(f"Total processed: {generated + skipped + failed}")
        print(f"Timestamp: {datetime.now().isoformat()}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
