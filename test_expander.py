#!/usr/bin/env python3
"""Quick test of curriculum expander"""

import sys
import os

sys.path.insert(0, os.getcwd())

# Try importing
try:
    print("Importing curriculum_expander...")
    from curriculum_expander import CurriculumExpander
    print("✅ Import successful")
    
    # Create instance
    print("\nCreating CurriculumExpander instance...")
    expander = CurriculumExpander()
    print("✅ Instance created")
    
    # Get stats
    print("\nGetting coverage stats...")
    stats = expander._get_current_stats()
    print(f"Coverage stats: {stats}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
