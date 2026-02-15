#!/usr/bin/env python3
"""
Wave 3 Content Importer
Imports educational content from CSV files into the platform database
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class ContentImporter:
    """Import content from CSV files into Wave 3 platform"""
    
    def __init__(self, csv_directory: str = "content_templates", 
                 output_file: str = "wave3_content_database.json"):
        self.csv_directory = csv_directory
        self.output_file = output_file
        self.content_items = []
        self.stats = {
            "total_imported": 0,
            "by_subject": {},
            "by_type": {},
            "by_difficulty": {},
            "errors": []
        }
    
    def find_latest_csv_files(self) -> List[str]:
        """Find all CSV files in the content templates directory"""
        csv_files = []
        
        if not os.path.exists(self.csv_directory):
            print(f"❌ Directory not found: {self.csv_directory}")
            return csv_files
        
        # Get all CSV files
        all_files = [f for f in os.listdir(self.csv_directory) if f.endswith('.csv')]
        
        # Group by subject to get latest timestamp
        subject_files = {}
        for filename in all_files:
            # Extract subject name (e.g., content_template_mathematics_20251223_082243.csv)
            parts = filename.replace('content_template_', '').replace('.csv', '').split('_')
            if len(parts) >= 2:
                subject = parts[0]
                timestamp = '_'.join(parts[1:])
                
                if subject not in subject_files or timestamp > subject_files[subject][1]:
                    subject_files[subject] = (filename, timestamp)
        
        # Return latest file for each subject
        csv_files = [os.path.join(self.csv_directory, data[0]) 
                     for data in subject_files.values()]
        
        return sorted(csv_files)
    
    def import_csv_file(self, csv_file: str) -> int:
        """Import content from a single CSV file"""
        count = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        content_item = self.process_content_row(row)
                        if content_item:
                            self.content_items.append(content_item)
                            count += 1
                            
                            # Update stats
                            subject = content_item.get('subject', 'Unknown')
                            content_type = content_item.get('content_type', 'Unknown')
                            difficulty = content_item.get('difficulty', 'Unknown')
                            
                            self.stats['by_subject'][subject] = self.stats['by_subject'].get(subject, 0) + 1
                            self.stats['by_type'][content_type] = self.stats['by_type'].get(content_type, 0) + 1
                            self.stats['by_difficulty'][difficulty] = self.stats['by_difficulty'].get(difficulty, 0) + 1
                    
                    except Exception as e:
                        error_msg = f"Error processing row in {csv_file}: {str(e)}"
                        self.stats['errors'].append(error_msg)
                        print(f"⚠️  {error_msg}")
        
        except Exception as e:
            error_msg = f"Error reading {csv_file}: {str(e)}"
            self.stats['errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        return count
    
    def process_content_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Process a single content row from CSV"""
        # Generate unique ID
        content_id = self.generate_content_id(
            row.get('subject', ''),
            row.get('topic', ''),
            row.get('subtopic', '')
        )
        
        # Split comma-separated fields
        learning_objectives = [obj.strip() for obj in row.get('learning_objectives', '').split(',') if obj.strip()]
        key_concepts = [concept.strip() for concept in row.get('key_concepts', '').split(',') if concept.strip()]
        tags = [tag.strip() for tag in row.get('tags', '').split(',') if tag.strip()]
        prerequisites = [prereq.strip() for prereq in row.get('prerequisites', '').split(',') if prereq.strip()]
        
        # Create content item
        content_item = {
            "id": content_id,
            "title": row.get('title', 'Untitled'),
            "subject": row.get('subject', 'General'),
            "topic": row.get('topic', ''),
            "subtopic": row.get('subtopic', ''),
            "content_type": row.get('content_type', 'study_guide'),
            "difficulty": row.get('difficulty', 'intermediate'),
            "exam_board": row.get('exam_board', 'WAEC'),
            "content": row.get('content', ''),
            "summary": row.get('summary', ''),
            "learning_objectives": learning_objectives,
            "key_concepts": key_concepts,
            "worked_examples": row.get('worked_examples', ''),
            "important_formulas": row.get('important_formulas', ''),
            "common_mistakes": row.get('common_mistakes', ''),
            "practice_problems": row.get('practice_problems', ''),
            "exam_tips": row.get('exam_tips', ''),
            "estimated_read_time": int(row.get('estimated_read_time', 15)),
            "prerequisites": prerequisites,
            "related_questions": [],  # Will be populated later
            "tags": tags,
            "author": row.get('author', 'Akulearn Content Team'),
            "references": row.get('references', ''),
            "multimedia_links": row.get('multimedia_links', ''),
            "cultural_notes": row.get('cultural_notes', ''),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "published",
            "views": 0,
            "likes": 0,
            "completion_rate": 0.0
        }
        
        return content_item
    
    def generate_content_id(self, subject: str, topic: str, subtopic: str) -> str:
        """Generate unique content ID"""
        # Create slug from subject, topic, subtopic
        parts = [subject, topic, subtopic]
        slug = '_'.join([p.lower().replace(' ', '_') for p in parts if p])
        
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        return f"{slug}_{timestamp}"
    
    def save_to_database(self) -> bool:
        """Save imported content to JSON database"""
        try:
            database = {
                "metadata": {
                    "version": "3.0.0",
                    "generated_at": datetime.now().isoformat(),
                    "total_items": len(self.content_items),
                    "statistics": self.stats
                },
                "content": self.content_items,
                "subjects": list(self.stats['by_subject'].keys()),
                "content_types": list(self.stats['by_type'].keys())
            }
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Content database saved to: {self.output_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error saving database: {str(e)}")
            return False
    
    def import_all(self) -> Dict[str, Any]:
        """Import all content from CSV files"""
        print("="*70)
        print("Wave 3 Content Importer")
        print("="*70)
        print()
        
        # Find CSV files
        csv_files = self.find_latest_csv_files()
        
        if not csv_files:
            print("❌ No CSV files found to import")
            return self.stats
        
        print(f"📁 Found {len(csv_files)} CSV files to import:")
        for csv_file in csv_files:
            print(f"   • {os.path.basename(csv_file)}")
        print()
        
        # Import each file
        print("📥 Importing content...")
        print()
        
        for csv_file in csv_files:
            filename = os.path.basename(csv_file)
            count = self.import_csv_file(csv_file)
            
            if count > 0:
                print(f"✅ {filename}: {count} items imported")
            else:
                print(f"⚠️  {filename}: No items imported")
        
        print()
        
        # Update total stats
        self.stats['total_imported'] = len(self.content_items)
        
        # Save to database
        print("💾 Saving to database...")
        success = self.save_to_database()
        
        # Print summary
        print()
        print("="*70)
        print("Import Summary")
        print("="*70)
        print(f"Total Items Imported: {self.stats['total_imported']}")
        print()
        
        if self.stats['by_subject']:
            print("By Subject:")
            for subject, count in sorted(self.stats['by_subject'].items()):
                print(f"   • {subject}: {count} items")
        print()
        
        if self.stats['by_type']:
            print("By Content Type:")
            for content_type, count in sorted(self.stats['by_type'].items()):
                print(f"   • {content_type}: {count} items")
        print()
        
        if self.stats['by_difficulty']:
            print("By Difficulty:")
            for difficulty, count in sorted(self.stats['by_difficulty'].items()):
                print(f"   • {difficulty}: {count} items")
        print()
        
        if self.stats['errors']:
            print(f"⚠️  Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more errors")
        print()
        
        if success:
            print("✅ Import completed successfully!")
            print(f"📊 Database file: {self.output_file}")
            print(f"🚀 Ready to integrate with Wave 3 API")
        else:
            print("❌ Import completed with errors")
        
        print("="*70)
        
        return self.stats
    
    def verify_import(self) -> bool:
        """Verify the imported content database"""
        if not os.path.exists(self.output_file):
            print(f"❌ Database file not found: {self.output_file}")
            return False
        
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                database = json.load(f)
            
            total_items = database['metadata']['total_items']
            content_count = len(database['content'])
            
            print()
            print("="*70)
            print("Content Database Verification")
            print("="*70)
            print(f"✅ Database file exists: {self.output_file}")
            print(f"✅ Metadata present: {len(database['metadata'])} fields")
            print(f"✅ Content items: {content_count}")
            print(f"✅ Subjects: {len(database['subjects'])}")
            print(f"✅ Content types: {len(database['content_types'])}")
            
            if total_items == content_count:
                print(f"✅ Item count matches: {total_items}")
            else:
                print(f"⚠️  Item count mismatch: metadata={total_items}, actual={content_count}")
            
            # Sample content item
            if content_count > 0:
                sample = database['content'][0]
                print()
                print("Sample Content Item:")
                print(f"   • ID: {sample['id']}")
                print(f"   • Title: {sample['title']}")
                print(f"   • Subject: {sample['subject']}")
                print(f"   • Topic: {sample['topic']}")
                print(f"   • Type: {sample['content_type']}")
                print(f"   • Difficulty: {sample['difficulty']}")
            
            print("="*70)
            print()
            
            return True
        
        except Exception as e:
            print(f"❌ Verification failed: {str(e)}")
            return False


def main():
    """Main execution"""
    # Create importer
    importer = ContentImporter()
    
    # Import all content
    stats = importer.import_all()
    
    # Verify import
    importer.verify_import()
    
    # Return stats for programmatic use
    return stats


if __name__ == "__main__":
    main()
