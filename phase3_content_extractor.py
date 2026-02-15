#!/usr/bin/env python3
"""
Phase 3 Content Extractor - Intelligent Diagram Specification

Analyzes lesson content to automatically generate diagram specifications
for Venn diagrams, flowcharts, timelines, circuits, and chemistry diagrams.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class DiagramSpec:
    """Specification for a diagram to generate."""
    lesson_id: str
    diagram_type: str
    title: str
    subject: str
    data: Dict[str, Any]


class ContentExtractor:
    """Extract diagram specifications from lesson content."""
    
    def __init__(self, lessons_file: str = "content_data.json"):
        """Initialize with lessons data."""
        self.lessons_file = Path(lessons_file)
        self.lessons = self._load_lessons()
        
    def _load_lessons(self) -> List[Dict[str, Any]]:
        """Load lessons from JSON file."""
        with self.lessons_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "content" in data:
            return data["content"]
        return data if isinstance(data, list) else []
    
    # ==================== VENN DIAGRAMS ====================
    
    def extract_venn_specs(self, lesson: Dict[str, Any]) -> List[DiagramSpec]:
        """Extract Venn diagram specs from lesson."""
        specs = []
        lesson_id = lesson.get("id", "")
        subject = lesson.get("subject", "Unknown")
        content = lesson.get("content", "").lower()
        title = lesson.get("title", "")
        
        # Look for set theory keywords
        set_keywords = ["set", "union", "intersection", "venn", "subset"]
        if not any(kw in content for kw in set_keywords):
            return specs
        
        # Check for specific set operations
        if "union" in content or "∪" in content:
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="venn_2",
                title=f"{subject}: Set Union",
                subject=subject,
                data={
                    "set_a_label": "A",
                    "set_b_label": "B",
                    "only_a": 5,
                    "both": 3,
                    "only_b": 4,
                    "title": "A ∪ B (Union)"
                }
            ))
        
        if "intersection" in content or "∩" in content:
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="venn_2",
                title=f"{subject}: Set Intersection",
                subject=subject,
                data={
                    "set_a_label": "A",
                    "set_b_label": "B",
                    "only_a": 4,
                    "both": 6,
                    "only_b": 3,
                    "title": "A ∩ B (Intersection)"
                }
            ))
        
        # Three-set diagrams for complex topics
        if ("three" in content or "three-set" in content) and "set" in content:
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="venn_3",
                title=f"{subject}: Three Sets",
                subject=subject,
                data={
                    "set_a_label": "A",
                    "set_b_label": "B",
                    "set_c_label": "C",
                    "title": "A, B, C Relationships"
                }
            ))
        
        return specs
    
    # ==================== FLOWCHARTS ====================
    
    def extract_flowchart_specs(self, lesson: Dict[str, Any]) -> List[DiagramSpec]:
        """Extract flowchart specs from lesson."""
        specs = []
        lesson_id = lesson.get("id", "")
        subject = lesson.get("subject", "Unknown")
        content = lesson.get("content", "").lower()
        
        # Look for process/algorithm keywords
        flowchart_keywords = ["algorithm", "process", "step", "procedure", "method"]
        if not any(kw in content for kw in flowchart_keywords):
            return specs
        
        # Generic process flowchart
        if "algorithm" in content or "procedure" in content:
            steps = [
                {"type": "start", "text": "Start"},
                {"type": "process", "text": "Input Data"},
                {"type": "process", "text": "Process"},
                {"type": "decision", "text": "Valid?"},
                {"type": "process", "text": "Output"},
                {"type": "end", "text": "End"}
            ]
            
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="flowchart",
                title=f"{subject}: Process Flow",
                subject=subject,
                data={
                    "steps": steps,
                    "title": "Process Algorithm"
                }
            ))
        
        return specs
    
    # ==================== TIMELINES ====================
    
    def extract_timeline_specs(self, lesson: Dict[str, Any]) -> List[DiagramSpec]:
        """Extract timeline specs from lesson."""
        specs = []
        lesson_id = lesson.get("id", "")
        subject = lesson.get("subject", "Unknown")
        content = lesson.get("content", "")
        
        # Look for year patterns (4-digit years)
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, content)
        
        if len(years) >= 2:
            # Extract unique years
            unique_years = sorted(list(set([''.join(y) if isinstance(y, tuple) else y for y in years])))[:6]
            
            events = []
            for year in unique_years:
                # Try to find context around the year
                context_match = re.search(rf'{year}[:\-\s]+([^\.]+)', content)
                if context_match:
                    event_text = context_match.group(1).strip()[:50]
                else:
                    event_text = "Event"
                
                events.append({
                    "year": year,
                    "event": event_text
                })
            
            if events:
                specs.append(DiagramSpec(
                    lesson_id=lesson_id,
                    diagram_type="timeline",
                    title=f"{subject}: Timeline",
                    subject=subject,
                    data={
                        "events": events,
                        "title": f"Historical Timeline"
                    }
                ))
        
        return specs
    
    # ==================== CIRCUITS ====================
    
    def extract_circuit_specs(self, lesson: Dict[str, Any]) -> List[DiagramSpec]:
        """Extract circuit diagram specs from lesson."""
        specs = []
        lesson_id = lesson.get("id", "")
        subject = lesson.get("subject", "Unknown")
        content = lesson.get("content", "").lower()
        
        # Electrical circuits
        if any(kw in content for kw in ["circuit", "resistor", "voltage", "current"]):
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="circuit_electrical",
                title=f"{subject}: Electrical Circuit",
                subject=subject,
                data={
                    "components": [
                        {"type": "battery", "label": "V", "value": "12V"},
                        {"type": "resistor", "label": "R1", "value": "100Ω"},
                        {"type": "resistor", "label": "R2", "value": "200Ω"}
                    ],
                    "connections": "series",
                    "title": "Simple Series Circuit"
                }
            ))
        
        # Logic circuits
        if any(kw in content for kw in ["logic gate", "and", "or", "not gate", "truth table"]):
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="circuit_logic",
                title=f"{subject}: Logic Circuit",
                subject=subject,
                data={
                    "gates": [
                        {"type": "AND", "inputs": ["A", "B"], "output": "Q1"},
                        {"type": "OR", "inputs": ["Q1", "C"], "output": "Y"}
                    ],
                    "title": "Logic Gate Circuit"
                }
            ))
        
        return specs
    
    # ==================== CHEMISTRY ====================
    
    def extract_chemistry_specs(self, lesson: Dict[str, Any]) -> List[DiagramSpec]:
        """Extract chemistry diagram specs from lesson."""
        specs = []
        lesson_id = lesson.get("id", "")
        subject = lesson.get("subject", "Unknown")
        content = lesson.get("content", "").lower()
        
        # Molecular structures
        if any(kw in content for kw in ["molecule", "molecular", "structure", "compound"]):
            # Common molecules
            molecules = {
                "water": {"formula": "H2O", "atoms": [("H", 2), ("O", 1)]},
                "methane": {"formula": "CH4", "atoms": [("C", 1), ("H", 4)]},
                "co2": {"formula": "CO2", "atoms": [("C", 1), ("O", 2)]},
            }
            
            for mol_name, mol_data in molecules.items():
                if mol_name in content or mol_data["formula"].lower() in content:
                    specs.append(DiagramSpec(
                        lesson_id=lesson_id,
                        diagram_type="chemistry_molecular",
                        title=f"{subject}: {mol_data['formula']}",
                        subject=subject,
                        data={
                            "formula": mol_data["formula"],
                            "atoms": mol_data["atoms"],
                            "title": f"{mol_data['formula']} Structure"
                        }
                    ))
                    break
        
        # Chemical reactions
        if any(kw in content for kw in ["reaction", "equation", "reactant", "product"]):
            specs.append(DiagramSpec(
                lesson_id=lesson_id,
                diagram_type="chemistry_reaction",
                title=f"{subject}: Chemical Reaction",
                subject=subject,
                data={
                    "reactants": ["A", "B"],
                    "products": ["C"],
                    "title": "Chemical Reaction"
                }
            ))
        
        return specs
    
    # ==================== MAIN EXTRACTION ====================
    
    def extract_all_specs(self, max_per_type: int = 3) -> List[DiagramSpec]:
        """Extract all diagram specs from all lessons."""
        all_specs = []
        
        print(f"Extracting diagram specs from {len(self.lessons)} lessons...")
        
        for lesson in self.lessons:
            lesson_id = lesson.get("id", "")
            specs = []
            
            # Extract each type
            specs.extend(self.extract_venn_specs(lesson))
            specs.extend(self.extract_flowchart_specs(lesson))
            specs.extend(self.extract_timeline_specs(lesson))
            specs.extend(self.extract_circuit_specs(lesson))
            specs.extend(self.extract_chemistry_specs(lesson))
            
            # Limit per lesson
            if specs:
                all_specs.extend(specs[:max_per_type])
                print(f"  {lesson_id}: {len(specs[:max_per_type])} diagrams")
        
        print(f"\n✓ Extracted {len(all_specs)} diagram specifications")
        return all_specs
    
    def save_specs(self, specs: List[DiagramSpec], output_file: str = "phase3_diagram_specs.json"):
        """Save specs to JSON file."""
        specs_dict = [asdict(spec) for spec in specs]
        
        output_path = Path(output_file)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(specs_dict, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Specs saved to: {output_file}")
        
        # Print summary
        type_counts = {}
        for spec in specs:
            type_counts[spec.diagram_type] = type_counts.get(spec.diagram_type, 0) + 1
        
        print("\nDiagram Type Summary:")
        for dtype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {dtype}: {count}")


def main():
    """Main execution."""
    print("="*70)
    print("PHASE 3 CONTENT EXTRACTOR - INTELLIGENT DIAGRAM SPECS")
    print("="*70 + "\n")
    
    extractor = ContentExtractor()
    specs = extractor.extract_all_specs(max_per_type=2)
    extractor.save_specs(specs)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
