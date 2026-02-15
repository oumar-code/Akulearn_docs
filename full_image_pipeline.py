"""
Complete image generation pipeline for all lessons
Generates SDXL images and updates the database with metadata
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

def log(msg, level="info", end="\n"):
    """Simple logging"""
    symbols = {"info": "ℹ️", "ok": "✅", "warn": "⚠️", "err": "❌", "wait": "⏳"}
    print(f"{symbols.get(level, '→')} {msg}", end=end, flush=True)

def main():
    log("="*70, "info")
    log("COMPLETE IMAGE GENERATION PIPELINE", "info")
    log("="*70, "info")
    
    # Load database
    log("Loading database...", "info")
    try:
        with open("wave3_content_database.json", "r", encoding="utf-8") as f:
            db = json.load(f)
        lessons = db.get("content", [])
        log(f"Loaded {len(lessons)} lessons", "ok")
    except Exception as e:
        log(f"Failed to load database: {e}", "err")
        return
    
    # Import image generator
    log("Importing image generator...", "info")
    try:
        from stable_image_client import generate_image
        log("stable_image_client ready", "ok")
    except ImportError as e:
        log(f"Failed to import: {e}", "err")
        return
    
    # Setup output
    images_dir = Path("generated_images")
    images_dir.mkdir(exist_ok=True)
    
    # Statistics
    total_lessons = len(lessons)
    generated = 0
    skipped = 0
    failed = 0
    start_time = time.time()
    
    log(f"\n{'='*70}", "info")
    log(f"Generating images for {total_lessons} lessons", "info")
    log(f"This will take approximately {total_lessons * 5 // 60} minutes", "wait")
    log(f"{'='*70}\n", "info")
    
    # Main loop
    for idx, lesson in enumerate(lessons, 1):
        subject = lesson.get("subject", "Unknown")
        title = lesson.get("title", "Untitled")
        
        # Check if already has image
        if "image" in lesson:
            log(f"[{idx:2d}/{total_lessons}] {subject:12} > {title[:40]:40} [SKIPPED - exists]", "warn")
            skipped += 1
            continue
        
        # Build prompt
        prompt = f"Educational diagram of {title} for WAEC {subject} curriculum, clear labels, classroom suitable"
        
        # Generate
        log(f"[{idx:2d}/{total_lessons}] {subject:12} > {title[:40]:40} ", "info", end="")
        sys.stdout.flush()
        
        try:
            _, image_path = generate_image(prompt)
            log(f"[OK]", "ok")
            
            # Update lesson
            lesson["image"] = {
                "path": image_path,
                "prompt": prompt,
                "generated_at": datetime.now().isoformat()
            }
            generated += 1
            
            # Rate limiting
            if generated % 5 == 0:
                elapsed = time.time() - start_time
                avg_time = elapsed / generated
                remaining = (total_lessons - idx) * avg_time
                log(f"  ⏸️  Pausing... (Remaining: ~{int(remaining/60)}m)", "wait")
                time.sleep(30)
        
        except Exception as e:
            log(f"[FAIL: {str(e)[:30]}]", "err")
            failed += 1
    
    # Save
    log(f"\n{'='*70}", "info")
    log("Saving database with image metadata...", "info")
    try:
        with open("wave3_content_database.json", "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        log(f"Database saved successfully", "ok")
    except Exception as e:
        log(f"Failed to save: {e}", "err")
        return
    
    # Report
    elapsed = time.time() - start_time
    log(f"{'='*70}", "info")
    log(f"GENERATION COMPLETE", "ok")
    log(f"  Generated: {generated} new images", "ok")
    log(f"  Skipped: {skipped} (already had images)", "warn")
    log(f"  Failed: {failed}", "err" if failed > 0 else "ok")
    log(f"  Total time: {int(elapsed/60)}m {int(elapsed%60)}s", "info")
    log(f"  Stored in: {images_dir.absolute()}", "ok")
    log(f"{'='*70}", "info")

if __name__ == "__main__":
    main()
