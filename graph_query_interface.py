#!/usr/bin/env python3
"""
Interactive query interface for the knowledge graph.
Supports searching, traversal, and relationship queries.
"""

import json
from pathlib import Path
from typing import Dict, List
from knowledge_graph import KnowledgeGraph, Node, CurriculumGraphBuilder


class GraphQueryInterface:
    """Query interface for knowledge graph."""
    
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph
    
    def search_by_name(self, name: str, node_type: str = None) -> list:
        """Search nodes by name (substring match)."""
        results = []
        name_lower = name.lower()
        for node_id, node in self.graph.nodes.items():
            if name_lower in node.name.lower():
                if node_type is None or node.type == node_type:
                    results.append(node)
        return results
    
    def search_by_subject(self, subject: str) -> list:
        """Find all topics and lessons in a subject."""
        results = []
        subject_lower = subject.lower()
        for node in self.graph.nodes.values():
            if node.metadata.get("subject", "").lower() == subject_lower:
                results.append(node)
        return results
    
    def search_by_curriculum(self, curriculum: str) -> list:
        """Find all content from a curriculum."""
        results = []
        for node in self.graph.nodes.values():
            if node.curriculum and node.curriculum.lower() == curriculum.lower():
                results.append(node)
        return results
    
    def get_subject_topics(self, subject: str) -> Dict:
        """Get all topics organized by level for a subject."""
        organized = {}
        for node in self.graph.nodes.values():
            if (node.type == "topic" and 
                node.metadata.get("subject", "").lower() == subject.lower()):
                level = node.level or "general"
                if level not in organized:
                    organized[level] = []
                organized[level].append(node.name)
        return organized
    
    def get_subject_coverage(self) -> Dict:
        """Get topic and lesson counts per subject."""
        coverage = {}
        for node in self.graph.nodes.values():
            subj = node.metadata.get("subject")
            if subj:
                if subj not in coverage:
                    coverage[subj] = {"topics": 0, "lessons": 0}
                if node.type == "topic":
                    coverage[subj]["topics"] += 1
                elif node.type == "lesson":
                    coverage[subj]["lessons"] += 1
        return coverage
    
    def find_path(self, start_name: str, end_name: str) -> list:
        """Find learning path between two concepts."""
        start_nodes = self.search_by_name(start_name)
        end_nodes = self.search_by_name(end_name)
        
        if not start_nodes or not end_nodes:
            return []
        
        # Try all combinations (prefer first match)
        for start in start_nodes:
            for end in end_nodes:
                path = self.graph.get_path(start.id, end.id)
                if path:
                    return [self.graph.nodes[nid].name for nid in path]
        
        return []
    
    def get_curriculum_map(self, curriculum: str = "WAEC") -> Dict:
        """Generate hierarchical curriculum structure."""
        structure = {}
        
        # Group by level, then subject, then topic
        for node in self.graph.nodes.values():
            if node.curriculum != curriculum:
                continue
            
            if node.type == "subject":
                if node.name not in structure:
                    structure[node.name] = {"topics": {}, "lessons": []}
            elif node.type == "topic":
                subj = node.metadata.get("subject")
                if subj and subj in structure:
                    topic_key = node.name
                    if topic_key not in structure[subj]["topics"]:
                        structure[subj]["topics"][topic_key] = []
            elif node.type == "lesson":
                subj = node.metadata.get("subject")
                topic = node.metadata.get("topic")
                if subj and subj in structure and topic:
                    if topic not in structure[subj]["topics"]:
                        structure[subj]["topics"][topic] = []
                    structure[subj]["topics"][topic].append({
                        "name": node.name,
                        "difficulty": node.metadata.get("difficulty")
                    })
        
        return structure
    
    def get_learning_sequence(self, subject: str, curriculum: str = "WAEC") -> List[str]:
        """Get recommended learning sequence for a subject."""
        topics = [n for n in self.graph.nodes.values() 
                 if (n.type == "topic" and 
                     n.curriculum == curriculum and 
                     n.metadata.get("subject", "").lower() == subject.lower())]
        return sorted([t.name for t in topics])
    
    def export_curriculum_summary(self, filepath: Path):
        """Export full curriculum structure as JSON."""
        summary = {
            "waec": self.get_curriculum_map("WAEC"),
            "nerdc": self.get_curriculum_map("NERDC"),
            "coverage": self.get_subject_coverage(),
            "graph_stats": self.graph.stats(),
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)


def main():
    print("\n=== Building Knowledge Graph ===\n")
    builder = CurriculumGraphBuilder()
    graph = builder.build()
    
    query = GraphQueryInterface(graph)
    
    print("\n=== Query Examples ===\n")
    
    # Subject coverage
    print("Subject Coverage:")
    for subj, counts in query.get_subject_coverage().items():
        print(f"  {subj}: {counts['topics']} topics, {counts['lessons']} lessons")
    
    # WAEC structure
    print("\nWAEC Mathematics Topics:")
    math_topics = query.get_subject_topics("Mathematics")
    for level, topics in sorted(math_topics.items()):
        print(f"  {level}: {len(topics)} topics")
        for t in topics[:3]:  # Show first 3
            print(f"    - {t}")
        if len(topics) > 3:
            print(f"    ... and {len(topics) - 3} more")
    
    # Learning sequence
    print("\nNERDC Physics Learning Sequence:")
    seq = query.get_learning_sequence("Physics", "NERDC")
    for i, topic in enumerate(seq[:5], 1):
        print(f"  {i}. {topic}")
    if len(seq) > 5:
        print(f"  ... and {len(seq) - 5} more")
    
    # Export summary
    summary_path = Path(__file__).parent / "curriculum_summary.json"
    query.export_curriculum_summary(summary_path)
    print(f"\nExported curriculum summary to {summary_path}")


if __name__ == "__main__":
    main()
