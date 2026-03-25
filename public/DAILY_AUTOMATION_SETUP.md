# Daily Content Generation Setup Guide

## Quick Start (5 minutes)

### Step 1: Install Schedule Library
```bash
pip install schedule
```

### Step 2: Run First Generation
```bash
python content_generator_scheduled.py --run-once
```
This generates all templates immediately and shows a progress report.

### Step 3: Set Up Daily Automation

#### Option A: Windows Task Scheduler (Recommended)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Akudemy Daily Content Generation"
4. Trigger: Daily at 9:55 AM
5. Action: Start program
   - Program: `C:\Users\hp\Documents\Akulearn_docs\myenv\Scripts\python.exe`
   - Arguments: `content_generator_scheduled.py --run-once`
   - Start in: `C:\Users\hp\Documents\Akulearn_docs\public`

#### Option B: Linux/Mac Cron Job
```bash
# Edit crontab
crontab -e

# Add this line (runs every day at 10 AM)
0 10 * * * cd /path/to/Akulearn_docs/public && python content_generator_scheduled.py --run-once >> content_generation.log 2>&1
```

#### Option C: Manual (Development)
```bash
# Terminal 1: Start daily scheduler
python content_generator_scheduled.py --start-daily

# Terminal 2: Check progress
python content_generator_scheduled.py --report
```

---

## What Gets Generated Daily

### At 10:00 AM
- **Study Guide Templates** (12 new templates)
- File: `{subject}_{topic}_guide.json`
- Status: Ready for expert review

### At 2:00 PM
- **Practice Questions** (120 new questions)
- Files: `{subject}_{topic}_questions.json`
- Organized by: Subject → Topic → Difficulty level

### At 6:00 PM
- **Mock Exams** (1 new full mock)
- File: `mock_exam_{number}.json`
- Format: 180 questions, 4 sections

---

## Monitoring Progress

### View Logs
```bash
# Display real-time logs
cat content_generation.log

# Last 20 lines
tail -20 content_generation.log

# Search for errors
grep "ERROR" content_generation.log
```

### View Dashboard
Open in browser:
```
file:///C:/Users/hp/Documents/Akulearn_docs/public/CONTENT_DASHBOARD.html
```

Updates every hour automatically.

### Check Statistics
```bash
python content_generator_scheduled.py --report
```

Output:
```
╔════════════════════════════════════════════════════════════════╗
║        CONTENT GENERATION PROGRESS REPORT                     ║
║        Generated: 2026-01-30T10:00:00                         ║
╚════════════════════════════════════════════════════════════════╝

📊 STATISTICS
─────────────────────────────────────────────────────────────────
Study Guides:        12
Practice Questions:  120
Mock Exams:          1
─────────────────────────────────────────────────────────────────

📈 PROGRESS
─────────────────────────────────────────────────────────────────
Guides (Target: 50)      [12/50] 24%
Questions (Target: 2000) [120/2000] 6%
Mocks (Target: 10)       [1/10] 10%
```

---

## Output File Structure

```
generated_content/
├── chemistry_atomic_structure_guide.json
├── chemistry_atomic_structure_questions.json
├── english_grammar_guide.json
├── english_grammar_questions.json
├── mathematics_trigonometry_guide.json
├── mathematics_trigonometry_questions.json
├── biology_cell_biology_guide.json
├── biology_cell_biology_questions.json
├── mock_exam_001.json
├── mock_exam_002.json
├── mock_exam_003.json
├── generation_stats.json           # Statistics updated daily
└── content_generation.log          # Activity log
```

---

## Daily Workflow

### Morning (Before 10 AM)
- ✅ Guides generated at 10:00 AM
- ✅ Assigned to subject matter experts
- ✅ Expert review begins

### Afternoon (2 PM)
- ✅ Questions generated
- ✅ Automatically reviewed by quality checklist
- ✅ Questions added to question bank

### Evening (6 PM)
- ✅ New mock exam created
- ✅ Questions populated
- ✅ Ready for student testing

### Night (After 6 PM)
- ✅ Review expert feedback
- ✅ Update checklist findings
- ✅ Prepare for next day

---

## Troubleshooting

### Issue: Script not running at scheduled time
**Solution**: Check Windows Task Scheduler / Cron job
```bash
# Windows: Check scheduled tasks
tasklist /svc | findstr python

# Linux: Check cron jobs
crontab -l
```

### Issue: "Schedule module not found"
**Solution**: Install the schedule library
```bash
pip install schedule
```

### Issue: Permission denied on generated files
**Solution**: Ensure output directory is writable
```bash
chmod 755 generated_content/
```

### Issue: Disk space full
**Solution**: Archive old generated files
```bash
# Archive files older than 30 days
find generated_content/ -name "*.json" -mtime +30 -exec zip archive_old.zip {} \;
```

---

## Customization

### Change Schedule Times
Edit `content_generator_scheduled.py`:
```python
DAILY_SCHEDULE = {
    "10:00": "generate_study_guides",  # Change to your preferred time
    "14:00": "generate_questions",
    "18:00": "generate_mocks"
}
```

### Change Number of Items Generated
Edit `content_generator_scheduled.py`:
```python
# In generate_questions() method:
for i in range(10):  # Change 10 to desired number of questions per topic
    ...
```

### Add More Subjects/Topics
Edit `content_generator_scheduled.py`:
```python
SUBJECTS = {
    "Chemistry": ["Atomic Structure", "Bonding", "Stoichiometry", "YOUR_TOPIC"],
    "Biology": ["Cell Biology", "Genetics", "Ecology", "YOUR_TOPIC"],
    "English": ["Grammar", "Vocabulary", "Literature", "YOUR_TOPIC"],
    "Mathematics": ["Trigonometry", "Statistics", "Calculus", "YOUR_TOPIC"]
}
```

---

## Next Steps

1. **Set Up Automation** (Today)
   - Install schedule library
   - Configure Task Scheduler / Cron
   - Verify first run works

2. **Generate Content** (Daily at scheduled times)
   - Guides at 10 AM
   - Questions at 2 PM
   - Mocks at 6 PM

3. **Expert Review** (Daily)
   - Use EXPERT_REVIEW_CHECKLIST.md
   - Score each guide (target: 28+/35)
   - Approve or request revisions

4. **Deploy** (Weekly)
   - Archive approved content
   - Deploy to CONTENT_DASHBOARD.html
   - Track student engagement

5. **Iterate** (Weekly)
   - Analyze student feedback
   - Update generation templates
   - Improve content quality

---

## Support

**Questions?**
- Email: content@akudemy.com
- Check: `/public/CONTENT_DASHBOARD.html`
- Review: `content_generation.log`

**File Structure Questions?**
- See: `generated_content/` directory

**Quality Standards?**
- See: `EXPERT_REVIEW_CHECKLIST.md`

---

**Setup Date**: January 30, 2026
**Maintenance**: Check daily, review weekly
**Success Target**: 50 guides + 2,000 questions + 10 mocks by March 31, 2026
