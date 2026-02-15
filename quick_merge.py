import json

# Load databases
main = json.load(open('wave3_content_database.json', 'r'))
batch4 = json.load(open('generated_content/wave3_content_database.json', 'r'))

print(f"Before: {main['metadata']['total_items']} lessons")
print(f"Batch 4: {len(batch4['lessons'])} new lessons")

# Add new lessons
main['content'].extend(batch4['lessons'])

# Update count
main['metadata']['total_items'] = len(main['content'])
main['metadata']['statistics']['total_imported'] = len(main['content'])

# Save
json.dump(main, open('wave3_content_database.json', 'w'), indent=2)

print(f"After: {main['metadata']['total_items']} lessons")
print("✅ Merge complete!")
