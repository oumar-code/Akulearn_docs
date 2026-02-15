import json
import os

# Verify Physics L2 JSON exists
json_path = 'content/ai_generated/textbooks/Physics/SS1/lesson_02_motion.json'
print(f'JSON exists: {os.path.exists(json_path)}')

# Load and check title
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        lesson = json.load(f)
    title = lesson['metadata']['lesson_title']
    print(f'Lesson title: {title}')
    print('Physics L2 JSON is valid')
