import json

def check_content_stats():
    try:
        with open('content_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)

        total_items = len(data['content'])
        print(f'📊 Total Content Items: {total_items}')

        subjects = {}
        levels = {}
        for item in data['content']:
            subj = item.get('subject', 'Unknown')
            level = item.get('level', 'Unknown')
            subjects[subj] = subjects.get(subj, 0) + 1
            if level != 'Unknown':
                levels[level] = levels.get(level, 0) + 1

        print('\n📚 By Subject:')
        for subj, count in sorted(subjects.items()):
            print(f'  {subj}: {count} items')

        print('\n🏫 By Level:')
        for level, count in sorted(levels.items()):
            print(f'  {level}: {count} items')

        # Check for NERDC content
        nerdc_items = [item for item in data['content'] if 'nerdc' in item.get('curriculum_framework', '').lower() or 'nerdc' in item.get('id', '').lower()]
        print(f'\n🎓 NERDC Curriculum Content: {len(nerdc_items)} items')

        # Check for learning options
        with_learning_options = [item for item in data['content'] if 'learning_options' in item or 'learning_tips' in item.get('content', '').lower()]
        print(f'📖 Content with Learning Options: {len(with_learning_options)} items')

        # Show recent additions
        print('\n🔄 Recent NERDC Content:')
        for item in nerdc_items[-5:]:  # Show last 5
            print(f'  • {item.get("title", "Unknown")} ({item.get("subject", "Unknown")})')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    check_content_stats()