"""
Batch image generator for lessons with progress tracking
Generates images for first N lessons as a test run
"""

import json
import time
from datetime import datetime
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("🎨 BATCH IMAGE GENERATOR - TEST RUN")
    print("="*70)
    
    # Load database
    print("\n📂 Loading database...")
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    lessons = db.get("content", [])
    total = len(lessons)
    print(f"✅ Found {total} lessons")
    
    # Import image generator
    print("📦 Loading image generator...")
    try:
        from stable_image_client import generate_image
        print("✅ stable_image_client imported")
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        return
    
    # Create output directory
    images_dir = Path("generated_images")
    images_dir.mkdir(exist_ok=True)
    print(f"✅ Output directory: {images_dir}")
    
    # Generate for first 5 lessons as test
    test_count = min(5, total)
    print(f"\n🚀 Generating images for first {test_count} lessons...\n")
    
    generated = 0
    for idx in range(test_count):
        lesson = lessons[idx]
        subject = lesson.get("subject", "Unknown")
        title = lesson.get("title", "Untitled")
        
        # Skip if already has image
        if "image" in lesson:
            print(f"[{idx+1}/{test_count}] ⏭️  {subject} > {title}")
            continue
        
        prompt = f"Educational diagram showing {title} for WAEC {subject}, clear illustrations, classroom setting"
        
        print(f"[{idx+1}/{test_count}] 🎨 Generating {subject}...", end="", flush=True)
        
        try:
            _, image_path = generate_image(prompt)
            print(f" ✅ {image_path}")
            
            lesson["image"] = {
                "path": image_path,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
            generated += 1
            
            # Wait between images
            if idx < test_count - 1:
                print(f"   ⏸️  Waiting 10s before next...")
                time.sleep(10)
        
        except Exception as e:
            print(f" ❌ {str(e)[:40]}")
    
    # Save database
    print(f"\n💾 Saving database with {generated} new images...")
    with open("wave3_content_database.json", "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print("✅ Database saved")
    
    print(f"\n{'='*70}")
    print(f"✅ Generated {generated} images")
    print(f"📊 Test complete. Ready for full batch generation")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
