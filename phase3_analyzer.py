#!/usr/bin/env python3
"""
Phase 3 Content Analyzer - Specialized Diagrams

Analyzes curriculum to identify opportunities for:
1. Chemistry diagrams (molecular structures, reactions)
2. Circuit diagrams (electrical circuits, logic gates)
3. Venn diagrams (set theory, logic)
4. Flowcharts (processes, algorithms)
5. Biology diagrams (cells, body systems)
6. Geography diagrams (maps, climate zones)
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict


class Phase3Analyzer:
    """Analyze content for specialized diagram opportunities."""
    
    # Keywords for diagram type identification
    DIAGRAM_KEYWORDS = {
        "chemistry_molecular": [
            "molecule", "molecular", "compound", "chemical formula", "structure",
            "hydrocarbon", "benzene", "organic", "functional group", "isomer",
            "alkane", "alkene", "alcohol", "acid", "ester", "polymer"
        ],
        "chemistry_reaction": [
            "reaction", "equation", "synthesis", "decomposition", "oxidation",
            "reduction", "combustion", "neutralization", "catalyst", "products",
            "reactants", "chemical change", "equilibrium"
        ],
        "circuit_electrical": [
            "circuit", "resistor", "capacitor", "current", "voltage", "ohm",
            "series circuit", "parallel circuit", "battery", "switch", "conductor",
            "insulator", "electrical", "electricity", "power"
        ],
        "circuit_logic": [
            "logic gate", "and gate", "or gate", "not gate", "truth table",
            "boolean", "digital", "binary", "logic circuit", "xor", "nand"
        ],
        "venn_diagram": [
            "set", "union", "intersection", "subset", "venn diagram",
            "element", "universal set", "complement", "disjoint", "overlap"
        ],
        "flowchart": [
            "process", "algorithm", "flowchart", "step", "procedure",
            "decision", "loop", "sequence", "workflow", "diagram"
        ],
        "biology_cell": [
            "cell", "nucleus", "membrane", "mitochondria", "chloroplast",
            "organelle", "cytoplasm", "ribosome", "cellular", "plant cell",
            "animal cell", "prokaryote", "eukaryote"
        ],
        "biology_system": [
            "digestive system", "circulatory system", "respiratory system",
            "nervous system", "skeletal system", "organ", "tissue", "anatomy",
            "physiology", "heart", "lung", "kidney", "liver"
        ],
        "geography_map": [
            "map", "latitude", "longitude", "scale", "legend", "compass",
            "coordinates", "region", "location", "topography", "relief"
        ],
        "timeline": [
            "timeline", "chronology", "sequence", "history", "era", "period",
            "before", "after", "event", "date", "century", "decade"
        ],
        "tree_diagram": [
            "hierarchy", "classification", "taxonomy", "family tree",
            "organizational", "tree structure", "branching", "phylogenetic"
        ],
        "graph_network": [
            "network", "graph theory", "node", "edge", "vertex", "path",
            "connected", "cycle", "tree", "directed graph"
        ]
    }
    
    def __init__(self, lessons_file: str = "content_data.json"):
        """Initialize analyzer with lessons data."""
        self.lessons_file = Path(lessons_file)
        self.lessons = self._load_lessons()
        self.results = defaultdict(list)
        
    def _load_lessons(self) -> List[Dict[str, Any]]:
        """Load lessons from JSON file."""
        if not self.lessons_file.exists():
            raise FileNotFoundError(f"Lessons file not found: {self.lessons_file}")
        
        with self.lessons_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Handle multiple formats
        if isinstance(data, dict):
            if "lessons" in data:
                return data["lessons"]
            elif "content" in data:
                return data["content"]
        return data if isinstance(data, list) else []
    
    def analyze_lesson(self, lesson: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyze a single lesson for diagram opportunities."""
        content = " ".join([
            lesson.get("title", ""),
            lesson.get("content", ""),
            " ".join(lesson.get("learning_objectives", [])),
            " ".join(lesson.get("key_concepts", []))
        ]).lower()
        
        matches = {}
        
        for diagram_type, keywords in self.DIAGRAM_KEYWORDS.items():
            matched = [kw for kw in keywords if kw.lower() in content]
            if matched:
                matches[diagram_type] = matched
        
        return matches
    
    def analyze_all(self) -> Dict[str, Any]:
        """Analyze all lessons for diagram opportunities."""
        print(f"Analyzing {len(self.lessons)} lessons for Phase 3 diagrams...")
        
        for lesson in self.lessons:
            lesson_id = lesson.get("id", "unknown")
            subject = lesson.get("subject", "Unknown")
            title = lesson.get("title", "Untitled")
            
            matches = self.analyze_lesson(lesson)
            
            if matches:
                for diagram_type, keywords in matches.items():
                    self.results[diagram_type].append({
                        "lesson_id": lesson_id,
                        "title": title,
                        "subject": subject,
                        "matched_keywords": keywords[:5],  # Top 5 matches
                        "keyword_count": len(keywords)
                    })
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        total_lessons = len(self.lessons)
        lessons_with_diagrams = len(set(
            item["lesson_id"] 
            for items in self.results.values() 
            for item in items
        ))
        
        # Calculate statistics
        diagram_stats = {}
        for diagram_type, items in self.results.items():
            diagram_stats[diagram_type] = {
                "count": len(items),
                "lessons": items,
                "subjects": list(set(item["subject"] for item in items))
            }
        
        # Subject breakdown
        subject_breakdown = defaultdict(lambda: defaultdict(int))
        for diagram_type, items in self.results.items():
            for item in items:
                subject_breakdown[item["subject"]][diagram_type] += 1
        
        report = {
            "summary": {
                "total_lessons_analyzed": total_lessons,
                "lessons_with_diagram_opportunities": lessons_with_diagrams,
                "coverage_percentage": round(lessons_with_diagrams / total_lessons * 100, 1),
                "diagram_types_identified": len(self.results),
                "total_diagram_opportunities": sum(len(items) for items in self.results.values())
            },
            "by_diagram_type": diagram_stats,
            "by_subject": dict(subject_breakdown),
            "priority_recommendations": self._get_priority_recommendations()
        }
        
        return report
    
    def _get_priority_recommendations(self) -> List[Dict[str, Any]]:
        """Get priority recommendations for diagram generation."""
        priorities = []
        
        # Priority 1: High-value diagrams with many matches
        for diagram_type, items in sorted(
            self.results.items(),
            key=lambda x: len(x[1]),
            reverse=True
        ):
            if len(items) >= 5:  # At least 5 lessons
                priorities.append({
                    "priority": "HIGH",
                    "diagram_type": diagram_type,
                    "lesson_count": len(items),
                    "reason": f"High demand - {len(items)} lessons benefit",
                    "subjects": list(set(item["subject"] for item in items))
                })
        
        # Priority 2: Subject-specific critical diagrams
        critical_types = ["chemistry_molecular", "circuit_electrical", "biology_cell"]
        for diagram_type in critical_types:
            if diagram_type in self.results and diagram_type not in [p["diagram_type"] for p in priorities]:
                items = self.results[diagram_type]
                priorities.append({
                    "priority": "MEDIUM",
                    "diagram_type": diagram_type,
                    "lesson_count": len(items),
                    "reason": "Critical for subject understanding",
                    "subjects": list(set(item["subject"] for item in items))
                })
        
        return priorities
    
    def save_report(self, output_file: str = "phase3_analysis_report.json"):
        """Save analysis report to file."""
        report = self.analyze_all()
        
        output_path = Path(output_file)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Report saved to: {output_file}")
        return report
    
    def print_summary(self):
        """Print analysis summary to console."""
        report = self.analyze_all()
        summary = report["summary"]
        
        print("\n" + "="*70)
        print("PHASE 3 ANALYSIS SUMMARY - SPECIALIZED DIAGRAMS")
        print("="*70)
        
        print(f"\n📊 OVERALL STATISTICS")
        print(f"  Total lessons analyzed: {summary['total_lessons_analyzed']}")
        print(f"  Lessons with diagram opportunities: {summary['lessons_with_diagram_opportunities']}")
        print(f"  Coverage: {summary['coverage_percentage']}%")
        print(f"  Diagram types identified: {summary['diagram_types_identified']}")
        print(f"  Total opportunities: {summary['total_diagram_opportunities']}")
        
        print(f"\n🎯 BY DIAGRAM TYPE")
        for diagram_type, stats in sorted(
            report["by_diagram_type"].items(),
            key=lambda x: x[1]["count"],
            reverse=True
        ):
            print(f"  {diagram_type.replace('_', ' ').title()}: {stats['count']} lessons")
            print(f"    Subjects: {', '.join(stats['subjects'])}")
        
        print(f"\n📚 BY SUBJECT")
        for subject, types in sorted(report["by_subject"].items()):
            total = sum(types.values())
            print(f"  {subject}: {total} diagram opportunities")
            for dtype, count in sorted(types.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"    - {dtype.replace('_', ' ')}: {count}")
        
        print(f"\n⭐ PRIORITY RECOMMENDATIONS")
        for i, rec in enumerate(report["priority_recommendations"][:5], 1):
            print(f"  {i}. [{rec['priority']}] {rec['diagram_type'].replace('_', ' ').title()}")
            print(f"     Lessons: {rec['lesson_count']} | Reason: {rec['reason']}")
            print(f"     Subjects: {', '.join(rec['subjects'])}")
        
        print("\n" + "="*70)


def main():
    """Main execution function."""
    try:
        analyzer = Phase3Analyzer()
        analyzer.print_summary()
        report = analyzer.save_report()
        
        print(f"\n✅ Phase 3 analysis complete!")
        print(f"   Found {report['summary']['total_diagram_opportunities']} diagram opportunities")
        print(f"   across {report['summary']['diagram_types_identified']} diagram types")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
