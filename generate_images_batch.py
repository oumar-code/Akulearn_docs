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
    print(" COMPLETE IMAGE GENERATION PIPELINE FOR 83 LESSONS")
    print("="*75)
    
    # Load database
    print("\n[1/3] Loading database...")
    with open("wave3_content_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    lessons = db.get("content", [])
    print("[OK] Loaded %d lessons" % len(lessons))
    
    # Import image generator
    print("\n[2/3] Importing image generation client...")
    try:
        from stable_image_client import generate_image
        print("[OK] Ready to generate SDXL images")
    except ImportError as e:
        print("[ERROR] Failed to import: %s" % e)
        return
    
    # Setup
    images_dir = Path("generated_images")
    images_dir.mkdir(exist_ok=True)
    
    # Statistics
    total = len(lessons)
    generated = 0
    skipped = 0
    failed = 0
    start = time.time()
    
    print("\n" + "="*75)
    print(" PROCESSING %d LESSONS" % total)
    print(" Estimated time: %d minutes" % (total * 5 // 60))
    print("="*75 + "\n")
    
    # Process each lesson
    for idx, lesson in enumerate(lessons, 1):
        subject = lesson.get("subject", "Unknown")
        title = lesson.get("title", "Untitled")[:42]
        
        # Skip if has image
        if "image" in lesson:
            print("  [%2d/%d] SKIP  %s > %s" % (idx, total, subject.ljust(12), title))
            skipped += 1
            continue
        
        prompt = "Educational diagram showing %s for WAEC %s, clear illustrations, classroom suitable, high quality" % (title, subject)
        
        print("  [%2d/%d] GEN   %s > %s" % (idx, total, subject.ljust(12), title), end=" ", flush=True)
        
        try:
            _, image_path = generate_image(prompt)
            print("[OK]")
            
            lesson["image"] = {
                "path": image_path,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
            generated += 1
            
            # Pause every 5 images
            if generated % 5 == 0:
                elapsed = time.time() - start
                rate = generated / elapsed if elapsed > 0 else 1
                remaining_imgs = total - idx
                remaining_secs = remaining_imgs / rate if rate > 0 else 0
                print("\n  PAUSE: Generated %d/%d, ETA: %dm\n" % (generated, total, int(remaining_secs/60)))
                time.sleep(30)
        
        except Exception as e:
            print("[FAIL] %s" % str(e)[:35])
            failed += 1
    
    # Save
    print("\n" + "="*75)
    print(" SAVING UPDATED DATABASE")
    print("="*75)
    
    with open("wave3_content_database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - start
    print("\n [OK] Generated: %d images" % generated)
    print(" [SKIP] Skipped: %d (already had images)" % skipped)
    print(" [FAIL] Failed: %d" % failed)
    print(" [TIME] Total: %dm %ds" % (int(elapsed/60), int(elapsed % 60)))
    print(" [PATH] Saved to: %s\n" % images_dir.absolute())
    print("="*75 + "\n")

if __name__ == "__main__":
    main()
