import json

# Load and verify the complete questions file
with open('generated_assets/questions/phase4_questions_complete.json', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
print(f"✓ Total questions: {len(questions)}")
print(f"✓ First question ID: {questions[0]['id']}")
print(f"✓ Last question ID: {questions[-1]['id']}")
print(f"\n✓ Question types distribution:")
types = {}
for q in questions:
    types[q['question_type']] = types.get(q['question_type'], 0) + 1
for t, count in types.items():
    print(f"  - {t}: {count}")

print(f"\n✓ Sample question:")
print(f"  ID: {questions[0]['id']}")
print(f"  Subject: {questions[0]['subject']}")
print(f"  Type: {questions[0]['question_type']}")
print(f"  Question: {questions[0]['question_text'][:80]}...")
