#!/usr/bin/env python3
"""
Wave 3 Visualization Module
Interactive graph visualization, learning pathways, and progress dashboards
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
from pathlib import Path

try:
    from neo4j import GraphDatabase, basic_auth
    NEO4J_AVAILABLE = True
except (ImportError, Exception):
    NEO4J_AVAILABLE = False
    GraphDatabase = None


class Wave3Visualizer:
    """
    Visualization tools for Wave 3 knowledge graph and progress data
    """

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password"):
        self.uri = neo4j_uri
        self.user = neo4j_user
        self.password = neo4j_password
        self.driver = None
        
        self.output_dir = Path("visualizations")
        self.output_dir.mkdir(exist_ok=True)
        
        self._connect()

    def _connect(self):
        """Connect to Neo4j"""
        try:
            from neo4j import GraphDatabase, basic_auth
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 7687))
            sock.close()
            
            if result != 0:
                return
            
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=basic_auth(self.user, self.password)
            )
            print("✅ Connected to Neo4j for visualization")
        except Exception:
            pass

    def visualize_knowledge_graph(self, output_file: str = None) -> str:
        """Create interactive knowledge graph visualization"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return ""
        
        with self.driver.session() as session:
            # Get lessons and connections
            result = session.run("""
                MATCH (l:Lesson)
                WHERE l.wave = 3
                OPTIONAL MATCH (l)-[c:CONNECTS_TO]-(l2:Lesson)
                RETURN l.id as id, l.subject as subject, l.title as title,
                       collect({target: l2.id, type: c.type, strength: c.strength}) as connections
            """)
            
            # Build network graph
            G = nx.Graph()
            node_colors = {}
            subject_colors = {
                'Chemistry': '#FF6B6B',
                'Biology': '#4ECDC4',
                'English Language': '#95E1D3',
                'Economics': '#F38181',
                'Geography': '#AA96DA',
                'History': '#FCBAD3',
                'Computer Science': '#A8E6CF'
            }
            
            for record in result:
                node_id = record['id']
                subject = record['subject']
                title = record['title']
                
                G.add_node(node_id, subject=subject, title=title)
                node_colors[node_id] = subject_colors.get(subject, '#CCCCCC')
                
                for conn in record['connections']:
                    if conn['target']:
                        G.add_edge(node_id, conn['target'],
                                 conn_type=conn['type'],
                                 strength=conn['strength'] or 0.5)
            
            # Create Plotly visualization
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            edge_trace = []
            for edge in G.edges(data=True):
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                
                edge_trace.append(go.Scatter(
                    x=[x0, x1, None],
                    y=[y0, y1, None],
                    mode='lines',
                    line=dict(width=edge[2].get('strength', 0.5) * 3, color='#888'),
                    hoverinfo='none',
                    showlegend=False
                ))
            
            node_trace = go.Scatter(
                x=[pos[node][0] for node in G.nodes()],
                y=[pos[node][1] for node in G.nodes()],
                mode='markers+text',
                hoverinfo='text',
                marker=dict(
                    size=20,
                    color=[node_colors[node] for node in G.nodes()],
                    line=dict(width=2, color='white')
                ),
                text=[G.nodes[node]['subject'][:4] for node in G.nodes()],
                textposition='middle center',
                textfont=dict(size=8, color='white'),
                hovertext=[f"{G.nodes[node]['subject']}<br>{G.nodes[node]['title']}"
                          for node in G.nodes()]
            )
            
            fig = go.Figure(data=edge_trace + [node_trace],
                          layout=go.Layout(
                              title='Wave 3 Knowledge Graph: Cross-Subject Connections',
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=0, l=0, r=0, t=40),
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              height=800
                          ))
            
            if not output_file:
                output_file = self.output_dir / "knowledge_graph.html"
            
            fig.write_html(str(output_file))
            print(f"✅ Knowledge graph visualization: {output_file}")
            return str(output_file)

    def visualize_learning_pathway(self, path_id: str, output_file: str = None) -> str:
        """Visualize a learning pathway"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return ""
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (lp:LearningPath {id: $path_id})-[inc:INCLUDES_LESSON]->(l:Lesson)
                RETURN lp.name as path_name,
                       l.id as lesson_id,
                       l.subject as subject,
                       l.title as title,
                       inc.order as order,
                       inc.total_lessons as total
                ORDER BY inc.order
            """, {"path_id": path_id})
            
            records = list(result)
            if not records:
                print(f"⚠️ Learning path not found: {path_id}")
                return ""
            
            path_name = records[0]['path_name']
            
            # Create pathway diagram
            fig = go.Figure()
            
            for i, record in enumerate(records):
                # Add lesson box
                fig.add_trace(go.Scatter(
                    x=[i],
                    y=[0],
                    mode='markers+text',
                    marker=dict(size=60, color='lightblue', line=dict(width=2, color='darkblue')),
                    text=f"Lesson {record['order']}",
                    textposition='middle center',
                    hovertext=f"{record['subject']}<br>{record['title']}",
                    showlegend=False
                ))
                
                # Add arrow to next lesson
                if i < len(records) - 1:
                    fig.add_annotation(
                        x=i+0.5, y=0,
                        ax=i, ay=0,
                        xref='x', yref='y',
                        axref='x', ayref='y',
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor='gray'
                    )
            
            fig.update_layout(
                title=f'Learning Pathway: {path_name}',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
                height=300,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            
            if not output_file:
                output_file = self.output_dir / f"pathway_{path_id}.html"
            
            fig.write_html(str(output_file))
            print(f"✅ Learning pathway visualization: {output_file}")
            return str(output_file)

    def visualize_student_progress(self, student_id: str, output_file: str = None) -> str:
        """Create comprehensive progress dashboard"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return ""
        
        with self.driver.session() as session:
            # Get progress data
            result = session.run("""
                MATCH (s:Student {id: $student_id})-[r:STUDYING]->(l:Lesson)
                WHERE l.wave = 3
                RETURN l.subject as subject,
                       l.title as title,
                       r.mastery_level as mastery_level,
                       r.mastery_percentage as mastery_percentage,
                       r.time_spent_seconds as time_spent
                ORDER BY l.subject, l.id
            """, {"student_id": student_id})
            
            records = list(result)
            if not records:
                print(f"⚠️ No progress data for student: {student_id}")
                return ""
            
            # Prepare data
            df = pd.DataFrame([{
                'subject': r['subject'],
                'title': r['title'],
                'mastery_level': r['mastery_level'] or 'not_started',
                'mastery_percentage': r['mastery_percentage'] or 0,
                'time_hours': (r['time_spent'] or 0) / 3600
            } for r in records])
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Mastery by Subject', 'Time Spent by Subject',
                              'Mastery Distribution', 'Progress Overview'),
                specs=[[{'type': 'bar'}, {'type': 'bar'}],
                      [{'type': 'pie'}, {'type': 'scatter'}]]
            )
            
            # Mastery by subject
            subject_mastery = df.groupby('subject')['mastery_percentage'].mean()
            fig.add_trace(
                go.Bar(x=subject_mastery.index, y=subject_mastery.values,
                      marker_color='lightblue', name='Avg Mastery'),
                row=1, col=1
            )
            
            # Time by subject
            subject_time = df.groupby('subject')['time_hours'].sum()
            fig.add_trace(
                go.Bar(x=subject_time.index, y=subject_time.values,
                      marker_color='lightgreen', name='Time (hours)'),
                row=1, col=2
            )
            
            # Mastery distribution
            mastery_counts = df['mastery_level'].value_counts()
            fig.add_trace(
                go.Pie(labels=mastery_counts.index, values=mastery_counts.values,
                      name='Mastery Levels'),
                row=2, col=1
            )
            
            # Progress overview
            fig.add_trace(
                go.Scatter(x=df.index, y=df['mastery_percentage'],
                          mode='lines+markers', name='Progress',
                          line=dict(color='purple', width=2),
                          marker=dict(size=8)),
                row=2, col=2
            )
            
            fig.update_layout(
                title_text=f'Student Progress Dashboard: {student_id}',
                height=800,
                showlegend=True
            )
            
            if not output_file:
                output_file = self.output_dir / f"progress_{student_id}.html"
            
            fig.write_html(str(output_file))
            print(f"✅ Progress dashboard: {output_file}")
            return str(output_file)

    def visualize_time_analytics(self, student_id: str, days: int = 30,
                                 output_file: str = None) -> str:
        """Visualize time-on-task analytics"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return ""
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Student {id: $student_id})-[:PERFORMED_ACTIVITY]->(a:LearningActivity)
                WHERE a.timestamp >= $cutoff_date
                RETURN a.timestamp as timestamp,
                       a.type as activity_type,
                       a.duration_seconds as duration
                ORDER BY a.timestamp
            """, {
                "student_id": student_id,
                "cutoff_date": cutoff_date
            })
            
            records = list(result)
            if not records:
                print(f"⚠️ No activity data for student: {student_id}")
                return ""
            
            # Prepare data
            df = pd.DataFrame([{
                'timestamp': datetime.fromisoformat(r['timestamp']),
                'activity_type': r['activity_type'],
                'duration_minutes': r['duration'] / 60
            } for r in records])
            
            df['date'] = df['timestamp'].dt.date
            
            # Create visualizations
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Daily Study Time', 'Activity Type Distribution')
            )
            
            # Daily study time
            daily_time = df.groupby('date')['duration_minutes'].sum()
            fig.add_trace(
                go.Bar(x=daily_time.index.astype(str), y=daily_time.values,
                      marker_color='steelblue', name='Minutes'),
                row=1, col=1
            )
            
            # Activity distribution
            activity_counts = df['activity_type'].value_counts()
            fig.add_trace(
                go.Bar(x=activity_counts.index, y=activity_counts.values,
                      marker_color='coral', name='Count'),
                row=2, col=1
            )
            
            fig.update_layout(
                title_text=f'Time Analytics ({days} days): {student_id}',
                height=800,
                showlegend=False
            )
            
            if not output_file:
                output_file = self.output_dir / f"time_analytics_{student_id}.html"
            
            fig.write_html(str(output_file))
            print(f"✅ Time analytics visualization: {output_file}")
            return str(output_file)

    def generate_subject_heatmap(self, output_file: str = None) -> str:
        """Generate subject connection heatmap"""
        if not self.driver:
            print("❌ Neo4j not connected")
            return ""
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l1:Lesson)-[c:CONNECTS_TO]-(l2:Lesson)
                WHERE l1.wave = 3 AND l2.wave = 3
                RETURN l1.subject as subject1, l2.subject as subject2,
                       count(c) as connection_count
            """)
            
            # Build connection matrix
            subjects = ['Chemistry', 'Biology', 'English Language', 'Economics',
                       'Geography', 'History', 'Computer Science']
            
            matrix = [[0] * len(subjects) for _ in range(len(subjects))]
            
            for record in result:
                i = subjects.index(record['subject1'])
                j = subjects.index(record['subject2'])
                count = record['connection_count']
                matrix[i][j] = count
                matrix[j][i] = count
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=matrix,
                x=subjects,
                y=subjects,
                colorscale='Blues',
                text=matrix,
                texttemplate='%{text}',
                textfont={"size": 12}
            ))
            
            fig.update_layout(
                title='Subject Connection Heatmap',
                xaxis_title='Subject',
                yaxis_title='Subject',
                height=600,
                width=700
            )
            
            if not output_file:
                output_file = self.output_dir / "subject_heatmap.html"
            
            fig.write_html(str(output_file))
            print(f"✅ Subject heatmap: {output_file}")
            return str(output_file)

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()


def main():
    """Generate all visualizations"""
    print("=" * 60)
    print("Wave 3 Visualization Generator")
    print("=" * 60)
    
    viz = Wave3Visualizer()
    
    if not viz.driver:
        print("\n⚠️ Neo4j not available. Start with:")
        print("docker-compose -f docker-compose-neo4j.yaml up -d")
        return
    
    print("\n1. Generating knowledge graph visualization...")
    viz.visualize_knowledge_graph()
    
    print("\n2. Generating subject heatmap...")
    viz.generate_subject_heatmap()
    
    print("\n3. Generating learning pathway examples...")
    viz.visualize_learning_pathway("path_environmental_science")
    viz.visualize_learning_pathway("path_nigerian_development")
    
    print("\n4. Example: Student progress dashboard...")
    print("   (Run viz.visualize_student_progress('STU001') after recording progress)")
    
    print("\n" + "=" * 60)
    print(f"✅ Visualizations saved to: {viz.output_dir}")
    print("=" * 60)
    
    viz.close()


if __name__ == "__main__":
    main()
