#!/usr/bin/env python3
"""
Final completion script to:
1. Generate missing WAEC topics
2. Generate missing NERDC topics
3. Run coverage analyses
4. Report final statistics
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}\n")
    try:
        result = subprocess.run([sys.executable, script_name], capture_output=False)
        if result.returncode != 0:
            print(f"⚠️  {script_name} exited with code {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("AKULEARN CURRICULUM COMPLETION - FINAL PASS")
    print("="*80)
    
    steps = [
        ("generate_waec_missing_topics.py", "STEP 1: Generate missing WAEC topics"),
        ("generate_nerdc_missing_topics.py", "STEP 2: Generate missing NERDC topics"),
        ("analyze_waec_coverage.py", "STEP 3: Analyze final WAEC coverage"),
        ("analyze_nerdc_coverage.py", "STEP 4: Analyze final NERDC coverage"),
    ]
    
    success_count = 0
    for script, desc in steps:
        if Path(script).exists():
            if run_script(script, desc):
                success_count += 1
        else:
            print(f"⚠️  {script} not found, skipping")
    
    print(f"\n{'='*80}")
    print(f"COMPLETION STATUS: {success_count}/{len(steps)} steps completed")
    print(f"{'='*80}\n")
    
    print("Next steps:")
    print("  1. Review coverage reports above")
    print("  2. Run: git add . && git commit -m 'Complete WAEC and NERDC content coverage'")
    print("  3. Run: git push origin docs-copilot-refactor")
    print("  4. When HF credits reset, run: python process_image_queue.py")

if __name__ == "__main__":
    main()
