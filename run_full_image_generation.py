#!/usr/bin/env python
"""
Complete image generation pipeline for all 83 lessons
Generates SDXL images via Hugging Face and updates database
"""

import json
import time
from datetime import datetime
from pathlib import Path

def main():
    print("\n" + "="*75)
    print(" 🎨 COMPLETE IMAGE GENERATION PIPELINE FOR 83 LESSONS")
    print("="*75)
    
    # Load database
    print("\n📂 Loading database...")
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    lessons = db.get("content", [])
    print(f"✅ Loaded {len(lessons)} lessons")
    
    # Import image generator
    print("📦 Importing image generation client...")
    from stable_image_client import generate_image
    print("✅ Ready to generate SDXL images")
    
    # Setup
    images_dir = Path("generated_images")
    images_dir.mkdir(exist_ok=True)
    
    # Statistics
    total = len(lessons)
    generated = 0
    skipped = 0
    failed = 0
    start = time.time()
    
    print(f"\n{'='*75}")
    print(f" PROCESSING {total} LESSONS")
    print(f" Est. time: {total * 5 // 60} minutes ({total * 5 % 60} seconds)")
    print(f"{'='*75}\n")
    
    # Process each lesson
    for idx, lesson in enumerate(lessons, 1):
        subject = lesson.get("subject", "Unknown")
        title = lesson.get("title", "Untitled")
        
        # Skip if has image
        if "image" in lesson:
            print(f"  [{idx:2d}/{total}] ⏭️  {subject:12} > {title[:42]}")
            skipped += 1
            continue
        
        prompt = f"Educational diagram showing {title} for WAEC {subject}, clear illustrations, classroom suitable, high quality"
        
        print(f"  [{idx:2d}/{total}] 🎨 {subject:12} > {title[:42]}", end=" ", flush=True)
        
        try:
            _, image_path = generate_image(prompt)
            print("✅")
            
            lesson["image"] = {
                "path": image_path,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
            generated += 1
            
            # Pause every 5 images
            if generated % 5 == 0:
                elapsed = time.time() - start
                rate = generated / elapsed
                remaining_imgs = total - idx
                remaining_secs = remaining_imgs / rate if rate > 0 else 0
                print(f"\n  ⏸️  Pause (Generated: {generated}, ETA: {int(remaining_secs/60)}m)\n")
                time.sleep(30)
        
        except Exception as e:
            print(f"❌ {str(e)[:35]}")
            failed += 1
    
    # Save
    print(f"\n{'='*75}")
    print(" 💾 SAVING UPDATED DATABASE")
    print(f"{'='*75}")
    
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - start
    print(f"\n ✅ Generated: {generated} images")
    print(f" ⏭️  Skipped: {skipped} (already had images)")
    print(f" ❌ Failed: {failed}")
    print(f" ⏱️  Total time: {int(elapsed/60)}m {int(elapsed % 60)}s")
    print(f" 📍 Saved to: {images_dir.absolute()}")
    print(f"\n{'='*75}\n")

if __name__ == "__main__":
    main()
