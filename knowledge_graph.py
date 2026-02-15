#!/usr/bin/env python3
"""
In-memory knowledge graph for AkuLearn curricula.
- Nodes: subjects, levels, topics, lessons, concepts
- Edges: prerequisites, relationships, containment, similarity
- No external DB required; JSON-serializable
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict, field
import re


@dataclass
class Node:
    """Graph node representing a concept/topic/lesson."""
    id: str
    type: str  # "subject", "level", "topic", "lesson", "concept"
    name: str
    description: str = ""
    level: Optional[str] = None  # SS1, SS2, SS3, or intermediate/advanced
    curriculum: Optional[str] = None  # WAEC, NERDC
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Edge:
    """Graph edge representing a relationship."""
    source_id: str
    target_id: str
    relationship_type: str  # "contains", "prerequisite", "related_to", "similar_to"
    weight: float = 1.0
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self):
        return asdict(self)


class KnowledgeGraph:
    """In-memory knowledge graph."""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.adj_list: Dict[str, List[str]] = defaultdict(list)  # Fast lookups
        self.reverse_adj: Dict[str, List[str]] = defaultdict(list)
        
    def add_node(self, node: Node):
        """Add a node to the graph."""
        self.nodes[node.id] = node
    
    def add_edge(self, edge: Edge):
        """Add an edge to the graph."""
        self.edges.append(edge)
        self.adj_list[edge.source_id].append(edge.target_id)
        self.reverse_adj[edge.target_id].append(edge.source_id)
    
    def get_neighbors(self, node_id: str, relationship_type: Optional[str] = None) -> List[str]:
        """Get connected nodes."""
        neighbors = self.adj_list.get(node_id, [])
        if relationship_type:
            edges_of_type = [e for e in self.edges 
                           if e.source_id == node_id and e.relationship_type == relationship_type]
            neighbors = [e.target_id for e in edges_of_type]
        return neighbors
    
    def get_prerequisites(self, node_id: str) -> List[str]:
        """Get prerequisite nodes (incoming edges)."""
        prereqs = self.reverse_adj.get(node_id, [])
        return [n for n in prereqs if any(
            e.source_id == n and e.target_id == node_id and e.relationship_type == "prerequisite"
            for e in self.edges
        )]
    
    def get_children(self, node_id: str) -> List[str]:
        """Get contained nodes (e.g., topics within subject)."""
        return [n for n in self.get_neighbors(node_id, "contains")]
    
    def get_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """BFS to find shortest path between nodes."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None
        if start_id == end_id:
            return [start_id]
        
        queue = [(start_id, [start_id])]
        visited = {start_id}
        
        while queue:
            current, path = queue.pop(0)
            for neighbor in self.get_neighbors(current):
                if neighbor == end_id:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_related_concepts(self, node_id: str, depth: int = 2) -> Set[str]:
        """DFS to find all related nodes up to depth."""
        related = set()
        stack = [(node_id, 0)]
        visited = {node_id}
        
        while stack:
            current, d = stack.pop()
            if d < depth:
                for neighbor in self.get_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        related.add(neighbor)
                        stack.append((neighbor, d + 1))
        
        return related
    
    def export_json(self, filepath: Path):
        """Export graph to JSON format."""
        data = {
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "node_types": self._count_types(),
            }
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _count_types(self) -> Dict[str, int]:
        """Count nodes by type."""
        counts = defaultdict(int)
        for node in self.nodes.values():
            counts[node.type] += 1
        return dict(counts)
    
    def stats(self) -> Dict:
        """Return graph statistics."""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": self._count_types(),
            "avg_degree": sum(len(neighbors) for neighbors in self.adj_list.values()) / max(len(self.nodes), 1),
        }


class CurriculumGraphBuilder:
    """Build knowledge graph from curriculum databases."""
    
    def __init__(self):
        self.graph = KnowledgeGraph()
        self.root = Path(__file__).parent
    
    def load_waec(self):
        """Load WAEC curriculum into graph."""
        db_path = self.root / "wave3_content_database.json"
        if not db_path.exists():
            print(f"WAEC database not found: {db_path}")
            return
        
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        # Add WAEC subject nodes
        subjects_seen = set()
        for item in db.get("content", []):
            subj = item.get("subject", "Unknown")
            if subj not in subjects_seen:
                subjects_seen.add(subj)
                node = Node(
                    id=f"waec_subj_{subj.lower().replace(' ', '_')}",
                    type="subject",
                    name=subj,
                    curriculum="WAEC"
                )
                self.graph.add_node(node)
        
        # Add topic and lesson nodes
        for item in db.get("content", []):
            subj = item.get("subject", "Unknown")
            topic = item.get("topic", "Unknown")
            lesson_id = item.get("id", f"waec_lesson_{len(self.graph.nodes)}")
            
            # Topic node
            topic_id = f"waec_topic_{subj.lower().replace(' ', '_')}_{topic.lower().replace(' ', '_')}"
            if topic_id not in self.graph.nodes:
                topic_node = Node(
                    id=topic_id,
                    type="topic",
                    name=topic,
                    curriculum="WAEC",
                    metadata={"subject": subj}
                )
                self.graph.add_node(topic_node)
                
                # Edge: subject contains topic
                subj_id = f"waec_subj_{subj.lower().replace(' ', '_')}"
                edge = Edge(subj_id, topic_id, "contains")
                self.graph.add_edge(edge)
            
            # Lesson node
            lesson_node = Node(
                id=lesson_id,
                type="lesson",
                name=item.get("title", topic),
                description=item.get("content", "")[:200],  # First 200 chars
                curriculum="WAEC",
                metadata={
                    "subject": subj,
                    "topic": topic,
                    "difficulty": item.get("difficulty", "intermediate")
                }
            )
            self.graph.add_node(lesson_node)
            
            # Edge: topic contains lesson
            edge = Edge(topic_id, lesson_id, "contains")
            self.graph.add_edge(edge)
        
        print(f"Loaded WAEC: {len([n for n in self.graph.nodes.values() if n.curriculum == 'WAEC'])} nodes")
    
    def load_nerdc(self):
        """Load NERDC curriculum into graph."""
        db_path = self.root / "connected_stack" / "backend" / "content_data.json"
        if not db_path.exists():
            print(f"NERDC database not found: {db_path}")
            return
        
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        
        # Add NERDC level nodes (SS1, SS2, SS3)
        for level in ["SS1", "SS2", "SS3"]:
            node = Node(
                id=f"nerdc_level_{level.lower()}",
                type="level",
                name=level,
                curriculum="NERDC"
            )
            self.graph.add_node(node)
        
        # Add subject nodes and organize by level
        subjects_by_level = defaultdict(set)
        for item in db.get("content", []):
            subj = item.get("subject", "Unknown")
            level = item.get("level", "SS1")
            subjects_by_level[level].add(subj)
        
        for level, subjects in subjects_by_level.items():
            for subj in subjects:
                subj_id = f"nerdc_{level.lower()}_subj_{subj.lower().replace(' ', '_')}"
                if subj_id not in self.graph.nodes:
                    node = Node(
                        id=subj_id,
                        type="subject",
                        name=subj,
                        level=level,
                        curriculum="NERDC"
                    )
                    self.graph.add_node(node)
                    
                    # Edge: level contains subject
                    level_id = f"nerdc_level_{level.lower()}"
                    edge = Edge(level_id, subj_id, "contains")
                    self.graph.add_edge(edge)
        
        # Add topic and lesson nodes
        for item in db.get("content", []):
            subj = item.get("subject", "Unknown")
            level = item.get("level", "SS1")
            topic = item.get("topic", "Unknown")
            lesson_id = item.get("id", f"nerdc_lesson_{len(self.graph.nodes)}")
            
            # Topic node
            topic_id = f"nerdc_{level.lower()}_topic_{subj.lower().replace(' ', '_')}_{topic.lower().replace(' ', '_')}"
            if topic_id not in self.graph.nodes:
                topic_node = Node(
                    id=topic_id,
                    type="topic",
                    name=topic,
                    level=level,
                    curriculum="NERDC",
                    metadata={"subject": subj}
                )
                self.graph.add_node(topic_node)
                
                # Edge: subject contains topic
                subj_id = f"nerdc_{level.lower()}_subj_{subj.lower().replace(' ', '_')}"
                edge = Edge(subj_id, topic_id, "contains")
                self.graph.add_edge(edge)
            
            # Lesson node
            lesson_node = Node(
                id=lesson_id,
                type="lesson",
                name=item.get("title", topic),
                description=item.get("content", "")[:200],
                level=level,
                curriculum="NERDC",
                metadata={
                    "subject": subj,
                    "topic": topic,
                    "difficulty": item.get("difficulty", "intermediate")
                }
            )
            self.graph.add_node(lesson_node)
            
            # Edge: topic contains lesson
            edge = Edge(topic_id, lesson_id, "contains")
            self.graph.add_edge(edge)
        
        print(f"Loaded NERDC: {len([n for n in self.graph.nodes.values() if n.curriculum == 'NERDC'])} nodes")
    
    def add_cross_subject_relationships(self):
        """Add relationships between related topics across curricula."""
        # Get all topic nodes
        topics = [n for n in self.graph.nodes.values() if n.type == "topic"]
        
        # Simple heuristic: topics with similar names are related
        for i, topic1 in enumerate(topics):
            for topic2 in topics[i+1:]:
                # Skip if from same curriculum and subject
                if (topic1.curriculum == topic2.curriculum and 
                    topic1.metadata.get("subject") == topic2.metadata.get("subject")):
                    continue
                
                # Check name similarity
                sim = self._name_similarity(topic1.name, topic2.name)
                if sim > 0.6:  # High similarity threshold
                    edge = Edge(
                        topic1.id, 
                        topic2.id, 
                        "related_to",
                        weight=sim
                    )
                    self.graph.add_edge(edge)
    
    def add_prerequisite_chains(self):
        """Add prerequisite relationships within levels."""
        # Assume natural order within a level's topics
        by_subject_level = defaultdict(list)
        for node in self.graph.nodes.values():
            if node.type == "topic":
                key = (node.curriculum, node.level, node.metadata.get("subject"))
                by_subject_level[key].append(node)
        
        for topics in by_subject_level.values():
            # Sort by name for consistent ordering
            topics_sorted = sorted(topics, key=lambda x: x.name)
            # Add chain: each topic leads to next
            for i in range(len(topics_sorted) - 1):
                edge = Edge(
                    topics_sorted[i].id,
                    topics_sorted[i+1].id,
                    "prerequisite",
                    weight=0.5
                )
                self.graph.add_edge(edge)
    
    @staticmethod
    def _name_similarity(name1: str, name2: str) -> float:
        """Simple token-based similarity score."""
        tokens1 = set(re.findall(r'\w+', name1.lower()))
        tokens2 = set(re.findall(r'\w+', name2.lower()))
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union if union > 0 else 0.0
    
    def build(self) -> KnowledgeGraph:
        """Build complete graph."""
        print("\n=== Building Knowledge Graph ===\n")
        self.load_waec()
        self.load_nerdc()
        self.add_cross_subject_relationships()
        self.add_prerequisite_chains()
        print(f"\nGraph built: {self.graph.stats()}\n")
        return self.graph


def main():
    builder = CurriculumGraphBuilder()
    graph = builder.build()
    
    # Export
    output_path = Path(__file__).parent / "knowledge_graph.json"
    graph.export_json(output_path)
    print(f"Exported to {output_path}")
    
    # Display stats
    stats = graph.stats()
    print(f"\nGraph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
