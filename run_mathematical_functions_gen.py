#!/usr/bin/env python3
"""
Run mathematical functions generator directly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'backend' / 'generators'))

from mathematical_functions import MathematicalFunctionsModelGenerator

if __name__ == '__main__':
    generator = MathematicalFunctionsModelGenerator()
    models = generator.generate_all_models()
    
    print("\n✅ Generated 6 Mathematical Functions models:")
    for model_name, model_path in models.items():
        file_size = Path(model_path).stat().st_size / 1024
        print(f"  - {model_name}.glb: {file_size:.2f} KB")
    
    # Calculate total
    total_size = sum(Path(path).stat().st_size for path in models.values()) / 1024
    print(f"\nTotal: {total_size:.2f} KB")
