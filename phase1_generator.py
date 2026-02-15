#!/usr/bin/env python3
"""Phase 1: Quick Wins - ASCII Diagrams and Truth Tables Generator

Generates:
1. ASCII diagrams for process flows, hierarchies, and structures (36 lessons)
2. Interactive HTML truth tables for logic concepts (10 lessons)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict


CONTENT_PATH = Path("content_data.json")
OUTPUT_DIR = Path("generated_assets")
OUTPUT_DIR.mkdir(exist_ok=True)

(OUTPUT_DIR / "ascii").mkdir(exist_ok=True)
(OUTPUT_DIR / "tables").mkdir(exist_ok=True)


# ============================================================================
# ASCII DIAGRAM GENERATION
# ============================================================================

class ASCIIDiagramGenerator:
    """Generate ASCII diagrams from lesson content."""
    
    DIAGRAM_PATTERNS = {
        "flow": {
            "keywords": ["flow", "process", "step", "sequence", "then", "next"],
            "template": lambda items: "\n".join([
                f"    ┌─────────────────────┐",
                *[f"    │ {item:^19} │" for item in items],
                f"    └─────────────────────┘",
                "\n         ↓\n".join(["" for _ in items[:-1]])
            ])
        },
        "hierarchy": {
            "keywords": ["hierarchy", "structure", "parent", "child", "root", "level", "classification"],
            "template": None  # Custom generation
        },
        "cycle": {
            "keywords": ["cycle", "circular", "loop", "repeat", "feedback"],
            "template": None  # Custom generation
        },
        "comparison": {
            "keywords": ["compare", "versus", "vs", "difference", "similar"],
            "template": None  # Custom generation
        },
    }
    
    @staticmethod
    def extract_structure(text: str) -> List[str]:
        """Extract structure items from lesson text."""
        # Look for numbered lists or bullet points
        patterns = [
            r'\d+\.\s+([^:\n]+)',  # Numbered: 1. Item
            r'[-•]\s+([^:\n]+)',   # Bullets
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s*:',  # Labels with colons
        ]
        
        items = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            items.extend([m.strip()[:15] for m in matches])
        
        return list(dict.fromkeys(items))[:5]  # Dedupe and limit to 5
    
    @staticmethod
    def generate_hierarchy(items: List[str]) -> str:
        """Generate ASCII hierarchy diagram."""
        if len(items) <= 1:
            return "  " + items[0] if items else ""
        
        lines = [items[0]]
        lines.append("  │")
        
        for i, item in enumerate(items[1:]):
            connector = "├─" if i < len(items) - 2 else "└─"
            lines.append(f"  {connector}─ {item}")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_cycle(items: List[str]) -> str:
        """Generate ASCII cycle diagram."""
        if len(items) < 2:
            return items[0] if items else ""
        
        n = min(len(items), 4)
        items = items[:n]
        
        lines = [""]
        if n == 2:
            lines = [
                f"    {items[0]}",
                "      ↙ ↖",
                f"    {items[1]}",
            ]
        elif n == 3:
            lines = [
                f"         {items[0]}",
                "        / \\",
                f"    {items[1]} - {items[2]}",
            ]
        elif n == 4:
            lines = [
                f"      {items[0]} → {items[1]}",
                f"        ↓    ↑",
                f"      {items[3]} ← {items[2]}",
            ]
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_flow(items: List[str]) -> str:
        """Generate ASCII flow diagram."""
        lines = []
        for i, item in enumerate(items):
            lines.append(f"  ┌────────────────┐")
            lines.append(f"  │ {item:^14} │")
            lines.append(f"  └────────────────┘")
            if i < len(items) - 1:
                lines.append(f"         ↓")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_comparison(items: List[str]) -> str:
        """Generate ASCII comparison diagram."""
        if len(items) < 2:
            return items[0] if items else ""
        
        left = items[0]
        right = items[1] if len(items) > 1 else "Other"
        
        return f"""
    ┌─────────────────────────────────┐
    │        {left:^20} │
    └─────────────────────────────────┘
               ⟷ ⟷ ⟷
    ┌─────────────────────────────────┐
    │        {right:^20} │
    └─────────────────────────────────┘
        """
    
    def generate(self, lesson: Dict[str, Any]) -> Tuple[str, str]:
        """Generate ASCII diagram for a lesson."""
        content = lesson.get("content", "")
        title = lesson.get("title", "")
        full_text = f"{title} {content}".lower()
        
        # Detect diagram type
        diagram_type = None
        for dtype, info in self.DIAGRAM_PATTERNS.items():
            if any(kw in full_text for kw in info["keywords"]):
                diagram_type = dtype
                break
        
        if not diagram_type:
            diagram_type = "flow"  # Default
        
        # Extract items
        items = self.extract_structure(content)
        if not items:
            items = [w.strip() for w in re.findall(r'\b[A-Z][a-z]+(?:\s+[a-z]+)?\b', content)[:3]]
        
        if not items:
            return diagram_type, ""
        
        # Generate diagram
        if diagram_type == "hierarchy":
            diagram = self.generate_hierarchy(items)
        elif diagram_type == "cycle":
            diagram = self.generate_cycle(items)
        elif diagram_type == "comparison":
            diagram = self.generate_comparison(items)
        else:  # flow
            diagram = self.generate_flow(items)
        
        return diagram_type, diagram


# ============================================================================
# TRUTH TABLE GENERATION
# ============================================================================

class TruthTableGenerator:
    """Generate HTML truth tables for logic concepts."""
    
    @staticmethod
    def extract_variables(text: str) -> List[str]:
        """Extract logic variables from text."""
        # Look for patterns like P, Q, R or variable names
        variables = []
        
        # Pattern 1: Capital letters used as propositions
        vars1 = re.findall(r'\b([A-P])\s*(?:and|or|not|∧|∨|¬)', text, re.IGNORECASE)
        variables.extend(vars1)
        
        # Pattern 2: Named variables
        vars2 = re.findall(r'\b(proposition|statement|variable)\s+([A-Z])\b', text, re.IGNORECASE)
        variables.extend([v[1] for v in vars2])
        
        # Pattern 3: Standalone variables
        vars3 = re.findall(r'\b([A-P])\b', text)
        variables.extend(vars3)
        
        # Deduplicate and limit
        variables = list(dict.fromkeys(variables))[:3]
        return variables if variables else ['P', 'Q']
    
    @staticmethod
    def generate_truth_table_html(variables: List[str]) -> str:
        """Generate HTML for truth table with given variables."""
        n_vars = len(variables)
        n_rows = 2 ** n_vars
        
        # Generate binary combinations
        rows = []
        for i in range(n_rows):
            row = []
            for j in range(n_vars):
                bit = (i >> (n_vars - 1 - j)) & 1
                row.append(bit)
            rows.append(row)
        
        # Build HTML
        html = f"""<div class="truth-table" style="margin: 20px 0; font-family: monospace;">
  <table style="border-collapse: collapse; border: 1px solid #333;">
    <thead>
      <tr style="background-color: #f0f0f0;">
        {''.join(f'<th style="border: 1px solid #999; padding: 8px; text-align: center; font-weight: bold;">{var}</th>' for var in variables)}
        <th style="border: 1px solid #999; padding: 8px; text-align: center; font-weight: bold;">Result</th>
      </tr>
    </thead>
    <tbody>
"""
        
        for i, row in enumerate(rows):
            html += f'      <tr style="background-color: {"#fff" if i % 2 == 0 else "#f9f9f9"}">\n'
            for bit in row:
                html += f'        <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">{bit}</td>\n'
            html += f'        <td style="border: 1px solid #ccc; padding: 8px; text-align: center; background-color: #ffffcc;">?</td>\n'
            html += f'      </tr>\n'
        
        html += """    </tbody>
  </table>
  <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
    <em>Fill in the Result column based on the logical operation</em>
  </p>
</div>"""
        
        return html
    
    def generate(self, lesson: Dict[str, Any]) -> Tuple[bool, str]:
        """Generate truth table for a lesson if applicable."""
        content = lesson.get("content", "")
        title = lesson.get("title", "")
        full_text = f"{title} {content}".lower()
        
        # Check if this is a logic lesson
        logic_keywords = ["logic", "truth table", "proposition", "boolean", "and", "or", "not"]
        is_logic = any(kw in full_text for kw in logic_keywords)
        
        if not is_logic:
            return False, ""
        
        # Extract variables and generate table
        variables = self.extract_variables(content)
        html = self.generate_truth_table_html(variables)
        
        return True, html


# ============================================================================
# MAIN GENERATION ORCHESTRATOR
# ============================================================================

def generate_phase1():
    """Generate Phase 1 assets for all applicable lessons."""
    
    # Load content
    with CONTENT_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    lessons = data.get("content", [])
    
    ascii_gen = ASCIIDiagramGenerator()
    table_gen = TruthTableGenerator()
    
    results = {
        "ascii_diagrams": [],
        "truth_tables": [],
        "generated_at": Path(__file__).stem,
        "total_lessons": len(lessons),
    }
    
    print("\n" + "="*70)
    print("PHASE 1: QUICK WINS ASSET GENERATION")
    print("="*70 + "\n")
    
    # Process each lesson
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        
        lesson_id = lesson.get("id", "unknown")
        title = lesson.get("title", "Untitled")
        subject = lesson.get("subject", "Unknown")
        
        # Generate ASCII diagram
        diagram_type, diagram = ascii_gen.generate(lesson)
        if diagram:
            diagram_path = OUTPUT_DIR / "ascii" / f"{lesson_id}.txt"
            with diagram_path.open("w", encoding="utf-8") as f:
                f.write(diagram)
            
            results["ascii_diagrams"].append({
                "lesson_id": lesson_id,
                "title": title,
                "subject": subject,
                "type": diagram_type,
                "path": str(diagram_path),
            })
            print(f"✓ ASCII ({diagram_type:12}): {subject:20} - {title[:45]}")
        
        # Generate truth table
        is_table, html = table_gen.generate(lesson)
        if is_table:
            table_path = OUTPUT_DIR / "tables" / f"{lesson_id}.html"
            with table_path.open("w", encoding="utf-8") as f:
                f.write(html)
            
            results["truth_tables"].append({
                "lesson_id": lesson_id,
                "title": title,
                "subject": subject,
                "path": str(table_path),
            })
            print(f"✓ Table (logic)    : {subject:20} - {title[:45]}")
    
    # Save summary
    summary_path = OUTPUT_DIR / "phase1_manifest.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "="*70)
    print(f"ASCII Diagrams Generated: {len(results['ascii_diagrams'])}")
    print(f"Truth Tables Generated  : {len(results['truth_tables'])}")
    print(f"Total Phase 1 Assets    : {len(results['ascii_diagrams']) + len(results['truth_tables'])}")
    print("="*70)
    print(f"\n📄 Manifest saved to: {summary_path}\n")
    
    # Summary by subject
    by_subject = defaultdict(lambda: {"ascii": 0, "table": 0})
    for item in results["ascii_diagrams"]:
        by_subject[item["subject"]]["ascii"] += 1
    for item in results["truth_tables"]:
        by_subject[item["subject"]]["table"] += 1
    
    print("Summary by Subject:")
    for subject, counts in sorted(by_subject.items()):
        print(f"  {subject:25} ASCII: {counts['ascii']:2}  Tables: {counts['table']:2}")
    
    print()


if __name__ == "__main__":
    generate_phase1()
