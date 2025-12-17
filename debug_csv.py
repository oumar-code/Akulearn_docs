import csv

with open('sample_content.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for i, row in enumerate(reader):
        if i < 3:  # Check first few rows
            print(f'Row {i+2}:')
            for key, value in row.items():
                if value is None:
                    print(f'  {key}: None')
                else:
                    print(f'  {key}: "{value[:50]}..."' if len(str(value)) > 50 else f'  {key}: "{value}"')
            print()