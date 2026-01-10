#!/bin/bash
# Commit and push final curriculum updates

cd /c/Users/hp/Documents/Akulearn_docs

echo "Staging updated content files..."
git add wave3_content_database.json
git add connected_stack/backend/content_data.json
git add generate_waec_missing_topics.py
git add generate_nerdc_missing_topics.py
git add analyze_waec_coverage.py
git add analyze_nerdc_coverage.py
git add nerdc_curriculum_map.json
git add complete_curriculum_coverage.py
git add coverage_report.py
git add analyze_waec_coverage.py

echo "Committing changes..."
git commit -m "Complete WAEC and NERDC curriculum coverage

- Generated all missing WAEC topics for 100% coverage
- Generated all missing NERDC topics across SS1-SS3
- Added nerdc_curriculum_map.json for NERDC tracking
- Added coverage analysis scripts for both frameworks
- Updated content databases with complete curriculum"

echo "Pushing to remote..."
git push origin docs-copilot-refactor

echo "✅ Commit and push complete"
