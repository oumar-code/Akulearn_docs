"""
Generate high-quality images for WAEC and NERDC lessons using Gemini API.
Uses free tier with enhanced prompt engineering for better results.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, List

def build_image_prompt(subject: str, title: str, level: str = "SS2") -> str:
    """
    Build an optimized image prompt for Gemini.
    Focuses on clarity, educational value, and high quality.
    """
    # Educational context for better results
    context = f"A professional educational diagram for {subject} at {level} level, "
    
    quality_directives = (
        "clean visual, clear labels, professional style, "
        "high contrast, suitable for student learning, realistic, "
        "scientifically accurate if applicable, well-organized, "
        "bright colors, readable text, centered composition"
    )
    
    prompt = f"{context}showing {title}. {quality_directives}"
    return prompt


def generate_waec_images(
    db_path: str = "wave3_content_database.json",
    skip_existing: bool = True,
    batch_size: int = 10,
    regenerate_existing: bool = False,
) -> Tuple[int, int, int]:
    """
    Generate images for all WAEC lessons.
    
    Returns: (generated, skipped, failed)
    """
    print("\n" + "="*80)
    print("GEMINI IMAGE GENERATION - WAEC LESSONS")
    print("="*80)
    
    # Load database
    if not Path(db_path).exists():
        print(f"ERROR: {db_path} not found")
        return 0, 0, 0
    
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    lessons = db.get("content", [])
    print(f"\n📚 Total WAEC lessons: {len(lessons)}")
    
    # Import Gemini client
    try:
        from gemini_image_client import generate_image, GeminiImageClientError
    except ImportError:
        print("ERROR: gemini_image_client module not found")
        return 0, 0, 0
    
    images_dir = Path("generated_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    generated = 0
    skipped = 0
    failed = 0
    
    print(f"\n⚙️  Configuration:")
    print(f"   Skip existing: {skip_existing}")
    print(f"   Regenerate existing: {regenerate_existing}")
    print(f"   Batch size: {batch_size}")
    print(f"\nStarting generation...\n")
    
    start_time = time.time()
    batch_start = 0
    
    for idx, lesson in enumerate(lessons, 1):
        subject = lesson.get("subject", "Unknown").title()
        title = lesson.get("title", "Untitled")
        level = lesson.get("level", "SS2")
        lesson_id = lesson.get("id", f"waec_{idx}")
        
        # Determine output path
        safe_subject = subject.replace(" ", "_").replace("/", "_")
        safe_title = title[:40].replace(" ", "_").replace("/", "_")
        output_path = images_dir / f"waec_{idx}_{safe_subject}_{safe_title}.png"
        
        # Skip logic
        should_skip = False
        if output_path.exists() and not regenerate_existing:
            if skip_existing:
                should_skip = True
                print(f"[{idx:2d}/{len(lessons)}] ⏭️  {subject:20s} > {title[:45]:45s} (exists)")
                skipped += 1
                continue
        
        # Generate image
        prompt = build_image_prompt(subject, title, level)
        
        try:
            print(f"[{idx:2d}/{len(lessons)}] 🎨 {subject:20s} > {title[:45]:45s}...", end=" ", flush=True)
            
            img_bytes, saved_path = generate_image(prompt, output_path=str(output_path))
            
            # Update lesson metadata
            lesson["image"] = str(saved_path)
            lesson["image_generated_at"] = datetime.now().isoformat()
            lesson["image_generator"] = "gemini"
            
            print(f"✓ ({len(img_bytes) // 1024}KB)")
            generated += 1
            
        except GeminiImageClientError as e:
            print(f"✗ FAILED")
            print(f"     Error: {str(e)[:80]}")
            failed += 1
        except Exception as e:
            print(f"✗ FAILED")
            print(f"     Error: {str(e)[:80]}")
            failed += 1
        
        # Batch pause (be nice to free tier)
        if idx % batch_size == 0:
            elapsed = time.time() - batch_start
            print(f"\n   [Batch {idx // batch_size} complete | {elapsed:.1f}s elapsed | Rate: {batch_size / elapsed:.1f} img/s]")
            print(f"   Pausing 2 seconds before next batch...\n")
            time.sleep(2)
            batch_start = time.time()
    
    # Save updated database
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("WAEC GENERATION COMPLETE")
    print("="*80)
    print(f"✓ Generated: {generated}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"✗ Failed:    {failed}")
    print(f"📊 Total: {generated + skipped + failed}/{len(lessons)}")
    print(f"⏱️  Time: {total_time:.1f}s ({total_time/len(lessons):.1f}s per image)")
    print("="*80)
    
    return generated, skipped, failed


def generate_nerdc_images(
    db_path: str = "connected_stack/backend/content_data.json",
    skip_existing: bool = True,
    batch_size: int = 10,
    limit: int = None,
    regenerate_existing: bool = False,
) -> Tuple[int, int, int]:
    """
    Generate images for NERDC lessons.
    
    Returns: (generated, skipped, failed)
    """
    print("\n" + "="*80)
    print("GEMINI IMAGE GENERATION - NERDC LESSONS")
    print("="*80)
    
    # Load database
    if not Path(db_path).exists():
        print(f"ERROR: {db_path} not found")
        return 0, 0, 0
    
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    lessons = db.get("content", [])
    if limit:
        lessons = lessons[:limit]
    
    print(f"\n📚 Total NERDC lessons: {len(lessons)}")
    if limit:
        print(f"⚠️  Limited to: {limit}")
    
    # Import Gemini client
    try:
        from gemini_image_client import generate_image, GeminiImageClientError
    except ImportError:
        print("ERROR: gemini_image_client module not found")
        return 0, 0, 0
    
    images_dir = Path("generated_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    generated = 0
    skipped = 0
    failed = 0
    
    print(f"\n⚙️  Configuration:")
    print(f"   Skip existing: {skip_existing}")
    print(f"   Regenerate existing: {regenerate_existing}")
    print(f"   Batch size: {batch_size}")
    print(f"\nStarting generation...\n")
    
    start_time = time.time()
    batch_start = 0
    
    for idx, lesson in enumerate(lessons, 1):
        subject = lesson.get("subject", "Unknown").title()
        title = lesson.get("title", "Untitled")
        level = lesson.get("level", "SS2").upper()
        
        # Determine output path
        safe_subject = subject.replace(" ", "_").replace("/", "_")
        safe_title = title[:40].replace(" ", "_").replace("/", "_")
        output_path = images_dir / f"nerdc_{level}_{idx}_{safe_subject}_{safe_title}.png"
        
        # Skip logic
        if output_path.exists() and not regenerate_existing:
            if skip_existing:
                print(f"[{idx:2d}/{len(lessons)}] ⏭️  {level} > {subject:20s} > {title[:40]:40s} (exists)")
                skipped += 1
                continue
        
        # Generate image
        prompt = build_image_prompt(subject, title, level)
        
        try:
            print(f"[{idx:2d}/{len(lessons)}] 🎨 {level} > {subject:20s} > {title[:40]:40s}...", end=" ", flush=True)
            
            img_bytes, saved_path = generate_image(prompt, output_path=str(output_path))
            
            # Update lesson metadata
            lesson["image"] = str(saved_path)
            lesson["image_generated_at"] = datetime.now().isoformat()
            lesson["image_generator"] = "gemini"
            
            print(f"✓ ({len(img_bytes) // 1024}KB)")
            generated += 1
            
        except GeminiImageClientError as e:
            print(f"✗ FAILED")
            print(f"     Error: {str(e)[:80]}")
            failed += 1
        except Exception as e:
            print(f"✗ FAILED")
            print(f"     Error: {str(e)[:80]}")
            failed += 1
        
        # Batch pause
        if idx % batch_size == 0:
            elapsed = time.time() - batch_start
            print(f"\n   [Batch {idx // batch_size} complete | {elapsed:.1f}s elapsed | Rate: {batch_size / elapsed:.1f} img/s]")
            print(f"   Pausing 2 seconds before next batch...\n")
            time.sleep(2)
            batch_start = time.time()
    
    # Save updated database (read and merge in case of concurrent changes)
    with open(db_path, "r", encoding="utf-8") as f:
        current_db = json.load(f)
    
    # Update content
    current_db["content"] = db.get("content", [])
    
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(current_db, f, indent=2, ensure_ascii=False)
    
    total_time = time.time() - start_time
    
    print("\n" + "="*80)
    print("NERDC GENERATION COMPLETE")
    print("="*80)
    print(f"✓ Generated: {generated}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"✗ Failed:    {failed}")
    print(f"📊 Total: {generated + skipped + failed}/{len(lessons)}")
    print(f"⏱️  Time: {total_time:.1f}s ({total_time/len(lessons):.1f}s per image)")
    print("="*80)
    
    return generated, skipped, failed


def main():
    """Main entry point for image generation."""
    print("\n" + "="*80)
    print("GEMINI API IMAGE GENERATION FOR AKULEARN")
    print("="*80)
    
    import argparse
    parser = argparse.ArgumentParser(description="Generate images using Gemini API")
    parser.add_argument("--waec-only", action="store_true", help="Generate only WAEC images")
    parser.add_argument("--nerdc-only", action="store_true", help="Generate only NERDC images")
    parser.add_argument("--regenerate", action="store_true", help="Regenerate existing images")
    parser.add_argument("--limit-nerdc", type=int, help="Limit NERDC generation to N images")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for pausing (default: 10)")
    
    args = parser.parse_args()
    
    total_gen = 0
    total_skip = 0
    total_fail = 0
    
    # WAEC images
    if not args.nerdc_only:
        print("\n" + "-"*80)
        print("PHASE 1: WAEC IMAGES")
        print("-"*80)
        gen, skip, fail = generate_waec_images(
            skip_existing=not args.regenerate,
            batch_size=args.batch_size,
            regenerate_existing=args.regenerate
        )
        total_gen += gen
        total_skip += skip
        total_fail += fail
    
    # NERDC images
    if not args.waec_only:
        print("\n" + "-"*80)
        print("PHASE 2: NERDC IMAGES")
        print("-"*80)
        gen, skip, fail = generate_nerdc_images(
            skip_existing=not args.regenerate,
            batch_size=args.batch_size,
            limit=args.limit_nerdc,
            regenerate_existing=args.regenerate
        )
        total_gen += gen
        total_skip += skip
        total_fail += fail
    
    # Summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    print(f"✓ Total Generated: {total_gen}")
    print(f"⏭️  Total Skipped:  {total_skip}")
    print(f"✗ Total Failed:    {total_fail}")
    print(f"📊 Grand Total: {total_gen + total_skip + total_fail}")
    print("="*80)
    
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
