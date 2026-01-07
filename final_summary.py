#!/usr/bin/env python3
"""
Final curriculum completion summary - run after all generators finish
"""

import json
from pathlib import Path

def main():
    print("\n" + "="*80)
    print("AKULEARN CURRICULUM - FINAL COMPLETION SUMMARY")
    print("="*80)
    
    # Load databases
    waec_db = json.load(open("wave3_content_database.json", encoding="utf-8"))
    nerdc_db = json.load(open("connected_stack/backend/content_data.json", encoding="utf-8"))
    
    waec_count = len(waec_db.get("content", []))
    nerdc_count = len(nerdc_db.get("content", []))
    
    print(f"\n📊 DATABASE TOTALS:")
    print(f"  WAEC Database: {waec_count} items")
    print(f"  NERDC Database: {nerdc_count} items")
    print(f"  Combined Total: {waec_count + nerdc_count} items\n")
    
    # WAEC subjects
    waec_by_subject = {}
    for item in waec_db.get("content", []):
        subj = item.get("subject", "Unknown")
        waec_by_subject[subj] = waec_by_subject.get(subj, 0) + 1
    
    print("WAEC Content by Subject:")
    for subj in sorted(waec_by_subject.keys()):
        print(f"  {subj}: {waec_by_subject[subj]} items")
    
    # NERDC subjects
    nerdc_by_subject = {}
    for item in nerdc_db.get("content", []):
        subj = item.get("subject", "Unknown")
        nerdc_by_subject[subj] = nerdc_by_subject.get(subj, 0) + 1
    
    print("\nNERDC Content by Subject:")
    for subj in sorted(nerdc_by_subject.keys()):
        print(f"  {subj}: {nerdc_by_subject[subj]} items")
    
    # Coverage estimates
    print("\n" + "="*80)
    print("COVERAGE ESTIMATES:")
    print("="*80)
    print("\nWAEC Curriculum (44 total topics):")
    print(f"  Mathematics (15): {waec_by_subject.get('Mathematics', 0)} items → {round(100*waec_by_subject.get('Mathematics',0)/15,1)}%")
    print(f"  Physics (11): {waec_by_subject.get('Physics', 0)} items → {round(100*waec_by_subject.get('Physics',0)/11,1)}%")
    print(f"  Chemistry (5): {waec_by_subject.get('Chemistry', 0)} items → {round(100*waec_by_subject.get('Chemistry',0)/5,1)}%")
    print(f"  Biology (8): {waec_by_subject.get('Biology', 0)} items → {round(100*waec_by_subject.get('Biology',0)/8,1)}%")
    print(f"  English Language (5): {waec_by_subject.get('English Language', 0)} items → {round(100*waec_by_subject.get('English Language',0)/5,1)}%")
    
    print("\nNERDC Curriculum (~168 total topics):")
    for subj in ["Mathematics", "Physics", "Chemistry", "Biology", "English Language", 
                 "Further Mathematics", "Geography", "Economics", "Computer Science"]:
        count = nerdc_by_subject.get(subj, 0)
        print(f"  {subj}: {count} items")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("\n1. Run coverage analysis:")
    print("   python analyze_waec_coverage.py")
    print("   python analyze_nerdc_coverage.py")
    print("\n2. Commit and push:")
    print("   git add wave3_content_database.json connected_stack/backend/content_data.json")
    print("   git commit -m 'Complete curriculum content generation'")
    print("   git push origin docs-copilot-refactor")
    print("\n3. Generate images (when credits reset):")
    print("   python queue_nerdc_images.py")
    print("   python process_image_queue.py")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
