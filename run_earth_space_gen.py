#!/usr/bin/env python3
"""Quick runner for Earth and Space generator - avoids full package import"""
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Direct import, avoid __init__ circular deps
from src.backend.generators.earth_space import EarthSpaceGenerator

gen = EarthSpaceGenerator()
models = gen.generate_all_models()
print(f"📋 Manifest created: earth_space_manifest.json")

# Display sizes
print(f"\n✅ Generated {len(models)} Earth and Space models:")
for m in models:
    print(f"  - {m['name']}.glb: {m['size_kb']} KB")

total_kb = sum(m['size_kb'] for m in models)
print(f"\nTotal: {total_kb:.2f} KB")
