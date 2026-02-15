"""
Wave 3 Knowledge Graph Generator
Generate interactive network graphs showing lesson relationships and learning pathways
"""

import json
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import numpy as np


@dataclass
class GraphNode:
    """Node in the knowledge graph"""
    id: str
    label: str
    type: str  # 'lesson', 'topic', 'skill'
    subject: str
    difficulty: str  # 'beginner', 'intermediate', 'advanced', 'expert'
    metadata: Dict
    x: Optional[float] = None
    y: Optional[float] = None


@dataclass
class GraphEdge:
    """Edge in the knowledge graph"""
    source: str
    target: str
    type: str  # 'prerequisite', 'related', 'follows', 'similar'
    weight: float = 1.0
    metadata: Dict = None


@dataclass
class LearningPath:
    """Sequential learning pathway"""
    id: str
    name: str
    description: str
    nodes: List[str]
    difficulty: str
    estimated_hours: int
    subject: str


class KnowledgeGraphGenerator:
    """
    Generate knowledge graphs and learning pathways from lesson data
    """
    
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
        self.reverse_adjacency: Dict[str, List[str]] = defaultdict(list)
        self.learning_paths: Dict[str, LearningPath] = {}
        
    def add_lesson(
        self,
        lesson_id: str,
        title: str,
        subject: str,
        difficulty: str,
        topics: List[str],
        prerequisites: List[str] = None,
        metadata: Dict = None
    ):
        """Add a lesson node to the graph"""
        node = GraphNode(
            id=lesson_id,
            label=title,
            type='lesson',
            subject=subject,
            difficulty=difficulty,
            metadata=metadata or {}
        )
        self.nodes[lesson_id] = node
        
        # Add prerequisite edges
        if prerequisites:
            for prereq_id in prerequisites:
                self.add_edge(prereq_id, lesson_id, 'prerequisite', weight=1.0)
        
        # Add topic connections
        for topic in topics:
            topic_id = f"topic_{subject}_{topic}"
            if topic_id not in self.nodes:
                self.nodes[topic_id] = GraphNode(
                    id=topic_id,
                    label=topic,
                    type='topic',
                    subject=subject,
                    difficulty='intermediate',
                    metadata={'topic_name': topic}
                )
            self.add_edge(topic_id, lesson_id, 'contains', weight=0.5)
    
    def add_edge(
        self,
        source: str,
        target: str,
        edge_type: str,
        weight: float = 1.0,
        metadata: Dict = None
    ):
        """Add an edge between two nodes"""
        edge = GraphEdge(
            source=source,
            target=target,
            type=edge_type,
            weight=weight,
            metadata=metadata or {}
        )
        self.edges.append(edge)
        self.adjacency_list[source].append(target)
        self.reverse_adjacency[target].append(source)
    
    def find_related_lessons(
        self,
        lesson_id: str,
        similarity_threshold: float = 0.3
    ) -> List[Tuple[str, float]]:
        """
        Find lessons related to the given lesson based on:
        - Shared topics
        - Similar difficulty
        - Same subject
        """
        if lesson_id not in self.nodes:
            return []
        
        source_node = self.nodes[lesson_id]
        related = []
        
        for node_id, node in self.nodes.items():
            if node_id == lesson_id or node.type != 'lesson':
                continue
            
            # Calculate similarity score
            similarity = 0.0
            
            # Same subject bonus
            if node.subject == source_node.subject:
                similarity += 0.4
            
            # Similar difficulty
            difficulty_map = {'beginner': 0, 'intermediate': 1, 'advanced': 2, 'expert': 3}
            diff_distance = abs(
                difficulty_map.get(node.difficulty, 1) - 
                difficulty_map.get(source_node.difficulty, 1)
            )
            similarity += (1 - diff_distance / 3) * 0.3
            
            # Shared topics (check through topic nodes)
            source_topics = set()
            target_topics = set()
            
            for edge in self.edges:
                if edge.target == lesson_id and edge.type == 'contains':
                    source_topics.add(edge.source)
                if edge.target == node_id and edge.type == 'contains':
                    target_topics.add(edge.source)
            
            shared_topics = len(source_topics & target_topics)
            if source_topics or target_topics:
                topic_similarity = shared_topics / len(source_topics | target_topics)
                similarity += topic_similarity * 0.3
            
            if similarity >= similarity_threshold:
                related.append((node_id, similarity))
        
        # Sort by similarity
        related.sort(key=lambda x: x[1], reverse=True)
        return related
    
    def generate_learning_path(
        self,
        start_lesson: str,
        end_lesson: str,
        path_name: str = "Custom Path"
    ) -> Optional[LearningPath]:
        """
        Generate optimal learning path from start to end lesson
        Uses BFS with prerequisite awareness
        """
        if start_lesson not in self.nodes or end_lesson not in self.nodes:
            return None
        
        # BFS to find path
        queue = deque([(start_lesson, [start_lesson])])
        visited = {start_lesson}
        
        while queue:
            current, path = queue.popleft()
            
            if current == end_lesson:
                # Found path
                start_node = self.nodes[start_lesson]
                path_obj = LearningPath(
                    id=f"path_{start_lesson}_{end_lesson}",
                    name=path_name,
                    description=f"Learning path from {self.nodes[start_lesson].label} to {self.nodes[end_lesson].label}",
                    nodes=path,
                    difficulty=start_node.difficulty,
                    estimated_hours=len(path) * 2,  # Assume 2 hours per lesson
                    subject=start_node.subject
                )
                self.learning_paths[path_obj.id] = path_obj
                return path_obj
            
            # Explore neighbors (following prerequisite chain)
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited and self.nodes[neighbor].type == 'lesson':
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def get_prerequisite_chain(self, lesson_id: str) -> List[str]:
        """Get all prerequisites for a lesson in order"""
        if lesson_id not in self.nodes:
            return []
        
        prerequisites = []
        visited = set()
        
        def dfs(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)
            
            # Get prerequisites
            for source in self.reverse_adjacency.get(node_id, []):
                edge = next((e for e in self.edges if e.source == source and e.target == node_id), None)
                if edge and edge.type == 'prerequisite':
                    dfs(source)
                    if source not in prerequisites:
                        prerequisites.append(source)
        
        dfs(lesson_id)
        return prerequisites
    
    def get_learning_sequence(self, subject: str, difficulty: str = None) -> List[str]:
        """
        Get optimal learning sequence for a subject
        Orders lessons by prerequisites (topological sort)
        """
        # Filter nodes by subject and difficulty
        relevant_nodes = [
            node_id for node_id, node in self.nodes.items()
            if node.type == 'lesson' and node.subject == subject and
            (difficulty is None or node.difficulty == difficulty)
        ]
        
        # Topological sort
        in_degree = defaultdict(int)
        for node_id in relevant_nodes:
            for edge in self.edges:
                if edge.target == node_id and edge.source in relevant_nodes:
                    in_degree[node_id] += 1
        
        queue = deque([n for n in relevant_nodes if in_degree[n] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor in relevant_nodes:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
        
        return result
    
    def calculate_positions(self, layout: str = "force"):
        """
        Calculate node positions for visualization
        
        Layouts:
        - force: Force-directed layout
        - hierarchical: Prerequisite hierarchy
        - circular: Circular layout by subject
        """
        if layout == "force":
            self._force_directed_layout()
        elif layout == "hierarchical":
            self._hierarchical_layout()
        elif layout == "circular":
            self._circular_layout()
    
    def _force_directed_layout(self, iterations: int = 100):
        """Force-directed graph layout (Fruchterman-Reingold)"""
        # Initialize random positions
        for node in self.nodes.values():
            node.x = np.random.uniform(0, 1000)
            node.y = np.random.uniform(0, 1000)
        
        # Parameters
        width, height = 1000, 800
        area = width * height
        k = np.sqrt(area / len(self.nodes))  # Optimal distance
        
        for iteration in range(iterations):
            # Calculate repulsive forces
            forces = {node_id: np.array([0.0, 0.0]) for node_id in self.nodes}
            
            for v in self.nodes.values():
                for u in self.nodes.values():
                    if v.id != u.id:
                        delta = np.array([v.x - u.x, v.y - u.y])
                        distance = np.linalg.norm(delta)
                        if distance > 0:
                            # Repulsive force
                            force = (k * k / distance) * (delta / distance)
                            forces[v.id] += force
            
            # Calculate attractive forces (edges)
            for edge in self.edges:
                if edge.source in self.nodes and edge.target in self.nodes:
                    source = self.nodes[edge.source]
                    target = self.nodes[edge.target]
                    delta = np.array([target.x - source.x, target.y - source.y])
                    distance = np.linalg.norm(delta)
                    if distance > 0:
                        # Attractive force
                        force = (distance * distance / k) * (delta / distance) * edge.weight
                        forces[source.id] += force
                        forces[target.id] -= force
            
            # Apply forces with cooling
            temperature = width / 10 * (1 - iteration / iterations)
            for node_id, force in forces.items():
                node = self.nodes[node_id]
                displacement = force / np.linalg.norm(force) * min(np.linalg.norm(force), temperature) if np.linalg.norm(force) > 0 else force
                node.x += displacement[0]
                node.y += displacement[1]
                
                # Keep within bounds
                node.x = max(50, min(width - 50, node.x))
                node.y = max(50, min(height - 50, node.y))
    
    def _hierarchical_layout(self):
        """Hierarchical layout based on prerequisites"""
        # Assign levels (topological sort)
        levels = {}
        in_degree = defaultdict(int)
        
        for edge in self.edges:
            if edge.type == 'prerequisite':
                in_degree[edge.target] += 1
        
        queue = deque([node_id for node_id in self.nodes if in_degree[node_id] == 0])
        level = 0
        
        while queue:
            level_size = len(queue)
            for _ in range(level_size):
                node_id = queue.popleft()
                levels[node_id] = level
                
                for neighbor in self.adjacency_list.get(node_id, []):
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
            level += 1
        
        # Assign positions
        level_counts = defaultdict(int)
        level_positions = defaultdict(int)
        
        for node_id, lvl in levels.items():
            level_counts[lvl] += 1
        
        for node_id, lvl in levels.items():
            node = self.nodes[node_id]
            node.y = lvl * 150 + 50
            width_spacing = 1000 / (level_counts[lvl] + 1)
            level_positions[lvl] += 1
            node.x = level_positions[lvl] * width_spacing
    
    def _circular_layout(self):
        """Circular layout grouped by subject"""
        subjects = defaultdict(list)
        for node_id, node in self.nodes.items():
            if node.type == 'lesson':
                subjects[node.subject].append(node_id)
        
        num_subjects = len(subjects)
        center_x, center_y = 500, 400
        subject_radius = 300
        
        for i, (subject, node_ids) in enumerate(subjects.items()):
            # Position subject nodes in circle
            angle = 2 * np.pi * i / num_subjects
            subject_x = center_x + subject_radius * np.cos(angle)
            subject_y = center_y + subject_radius * np.sin(angle)
            
            # Position lessons around subject center
            for j, node_id in enumerate(node_ids):
                node = self.nodes[node_id]
                node_angle = 2 * np.pi * j / len(node_ids)
                node.x = subject_x + 150 * np.cos(node_angle)
                node.y = subject_y + 150 * np.sin(node_angle)
    
    def export_for_visualization(
        self,
        include_topics: bool = True,
        filter_subject: str = None
    ) -> Dict:
        """
        Export graph data for frontend visualization
        Compatible with D3.js, Cytoscape.js, etc.
        """
        # Filter nodes
        nodes_list = []
        for node_id, node in self.nodes.items():
            if filter_subject and node.subject != filter_subject:
                continue
            if not include_topics and node.type == 'topic':
                continue
            
            nodes_list.append({
                'id': node.id,
                'label': node.label,
                'type': node.type,
                'subject': node.subject,
                'difficulty': node.difficulty,
                'x': node.x,
                'y': node.y,
                'metadata': node.metadata
            })
        
        # Filter edges
        node_ids = {n['id'] for n in nodes_list}
        edges_list = []
        for edge in self.edges:
            if edge.source in node_ids and edge.target in node_ids:
                edges_list.append({
                    'source': edge.source,
                    'target': edge.target,
                    'type': edge.type,
                    'weight': edge.weight,
                    'metadata': edge.metadata or {}
                })
        
        # Export learning paths
        paths_list = [asdict(path) for path in self.learning_paths.values()]
        
        return {
            'nodes': nodes_list,
            'edges': edges_list,
            'learning_paths': paths_list,
            'stats': {
                'total_nodes': len(nodes_list),
                'total_edges': len(edges_list),
                'subjects': list(set(n['subject'] for n in nodes_list)),
                'difficulty_levels': list(set(n['difficulty'] for n in nodes_list if n['type'] == 'lesson'))
            }
        }


# Example: Build sample knowledge graph
def build_sample_graph() -> KnowledgeGraphGenerator:
    """Build a sample knowledge graph for demonstration"""
    graph = KnowledgeGraphGenerator()
    
    # Mathematics lessons
    graph.add_lesson(
        'math_101', 'Basic Arithmetic', 'mathematics', 'beginner',
        topics=['addition', 'subtraction', 'multiplication', 'division'],
        prerequisites=[],
        metadata={'duration': 30, 'exercises': 20}
    )
    
    graph.add_lesson(
        'math_102', 'Fractions and Decimals', 'mathematics', 'beginner',
        topics=['fractions', 'decimals', 'percentages'],
        prerequisites=['math_101'],
        metadata={'duration': 45, 'exercises': 25}
    )
    
    graph.add_lesson(
        'math_201', 'Introduction to Algebra', 'mathematics', 'intermediate',
        topics=['variables', 'equations', 'expressions'],
        prerequisites=['math_102'],
        metadata={'duration': 60, 'exercises': 30}
    )
    
    graph.add_lesson(
        'math_202', 'Linear Equations', 'mathematics', 'intermediate',
        topics=['linear equations', 'graphing', 'slope'],
        prerequisites=['math_201'],
        metadata={'duration': 60, 'exercises': 35}
    )
    
    graph.add_lesson(
        'math_301', 'Quadratic Equations', 'mathematics', 'advanced',
        topics=['quadratics', 'factoring', 'formula'],
        prerequisites=['math_202'],
        metadata={'duration': 75, 'exercises': 40}
    )
    
    # Physics lessons
    graph.add_lesson(
        'phys_101', 'Introduction to Physics', 'physics', 'beginner',
        topics=['motion', 'forces', 'energy'],
        prerequisites=['math_101'],
        metadata={'duration': 45, 'exercises': 15}
    )
    
    graph.add_lesson(
        'phys_201', 'Kinematics', 'physics', 'intermediate',
        topics=['velocity', 'acceleration', 'displacement'],
        prerequisites=['phys_101', 'math_201'],
        metadata={'duration': 60, 'exercises': 25}
    )
    
    graph.add_lesson(
        'phys_202', 'Dynamics', 'physics', 'intermediate',
        topics=['Newton laws', 'friction', 'momentum'],
        prerequisites=['phys_201'],
        metadata={'duration': 60, 'exercises': 30}
    )
    
    # Add related lessons
    for lesson_id in graph.nodes.keys():
        if graph.nodes[lesson_id].type == 'lesson':
            related = graph.find_related_lessons(lesson_id, similarity_threshold=0.4)
            for related_id, similarity in related[:3]:  # Top 3 related
                graph.add_edge(lesson_id, related_id, 'related', weight=similarity)
    
    return graph


# Example usage
if __name__ == "__main__":
    # Build sample graph
    graph = build_sample_graph()
    
    # Calculate layout
    graph.calculate_positions(layout="force")
    
    # Generate learning paths
    math_path = graph.generate_learning_path('math_101', 'math_301', 'Mathematics Mastery')
    print(f"Math learning path: {math_path.nodes if math_path else 'Not found'}")
    
    # Get learning sequence
    math_sequence = graph.get_learning_sequence('mathematics')
    print(f"\nMathematics learning sequence: {math_sequence}")
    
    # Export for visualization
    graph_data = graph.export_for_visualization(include_topics=True)
    
    # Save to file
    with open('knowledge_graph_data.json', 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"\n✓ Knowledge graph exported: {graph_data['stats']}")
    print(f"  Nodes: {graph_data['stats']['total_nodes']}")
    print(f"  Edges: {graph_data['stats']['total_edges']}")
    print(f"  Subjects: {', '.join(graph_data['stats']['subjects'])}")
