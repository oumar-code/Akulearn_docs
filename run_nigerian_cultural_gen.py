"""
Runner script for Nigerian Cultural Models Generator
Generates all 6 Nigerian cultural and historical 3D models
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.backend.generators.nigerian_cultural import NigerianCulturalModelsGenerator

if __name__ == "__main__":
    generator = NigerianCulturalModelsGenerator()
    
    print("\n" + "="*60)
    print("Nigerian Cultural and Historical 3D Models Generator")
    print("="*60 + "\n")
    
    # Generate all models
    model_paths = generator.generate_all_models()
    
    # Print summary
    print("\n" + "="*60)
    print(f"✅ Generated {len(model_paths)} Nigerian Cultural models:")
    
    total_size = 0
    for path in model_paths:
        file_size = Path(path).stat().st_size / 1024
        total_size += file_size
        print(f"  - {Path(path).name}: {file_size:.2f} KB")
    
    print(f"\nTotal: {total_size:.2f} KB")
    print("="*60 + "\n")
