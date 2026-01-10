#!/usr/bin/env python3
"""
Export knowledge graph in visualization-friendly formats.
- GraphML for Gephi/Cytoscape
- DOT for Graphviz
- Interactive HTML D3.js
"""

import json
from pathlib import Path
from knowledge_graph import CurriculumGraphBuilder


def export_graphml(graph, filepath: Path):
    """Export as GraphML format for Gephi/Cytoscape."""
    # Lightweight GraphML (subset)
    graphml = """<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="node_type" for="node" attr.name="type" attr.type="string"/>
  <key id="node_curriculum" for="node" attr.name="curriculum" attr.type="string"/>
  <key id="edge_type" for="edge" attr.name="relationship" attr.type="string"/>
  <key id="edge_weight" for="edge" attr.name="weight" attr.type="double"/>
  <graph edgedefault="directed">
"""
    
    # Add nodes
    for node_id, node in graph.nodes.items():
        safe_id = node_id.replace(" ", "_")
        graphml += f"""    <node id="{safe_id}" labels=":({node.type})">
      <data key="node_type">{node.type}</data>
      <data key="node_curriculum">{node.curriculum or ""}</data>
    </node>
"""
    
    # Add edges
    for edge in graph.edges:
        src = edge.source_id.replace(" ", "_")
        tgt = edge.target_id.replace(" ", "_")
        graphml += f"""    <edge source="{src}" target="{tgt}">
      <data key="edge_type">{edge.relationship_type}</data>
      <data key="edge_weight">{edge.weight}</data>
    </edge>
"""
    
    graphml += """  </graph>
</graphml>"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(graphml)
    print(f"Exported GraphML: {filepath}")


def export_html_d3(graph, filepath: Path):
    """Export as interactive D3.js HTML visualization."""
    nodes_data = []
    edges_data = []
    
    # Prepare nodes
    for i, (node_id, node) in enumerate(graph.nodes.items()):
        nodes_data.append({
            "id": node_id,
            "name": node.name,
            "type": node.type,
            "curriculum": node.curriculum or "unknown",
            "index": i
        })
    
    # Create id-to-index mapping
    id_to_index = {node["id"]: i for i, node in enumerate(nodes_data)}
    
    # Prepare edges
    for edge in graph.edges:
        src_idx = id_to_index.get(edge.source_id)
        tgt_idx = id_to_index.get(edge.target_id)
        if src_idx is not None and tgt_idx is not None:
            edges_data.append({
                "source": src_idx,
                "target": tgt_idx,
                "type": edge.relationship_type,
                "weight": edge.weight
            })
    
    # HTML template
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; }}
    #canvas {{ width: 100%; height: 100vh; border: 1px solid #ccc; }}
    #info {{ position: absolute; top: 10px; right: 10px; background: white; 
             padding: 10px; border: 1px solid #ccc; border-radius: 5px; max-width: 300px; }}
    .stats {{ font-size: 12px; margin: 5px 0; }}
    svg {{ border: 1px solid #ddd; }}
  </style>
</head>
<body>
  <svg id="canvas"></svg>
  <div id="info">
    <h3>AkuLearn Knowledge Graph</h3>
    <div class="stats">Nodes: {len(nodes_data)}</div>
    <div class="stats">Edges: {len(edges_data)}</div>
    <div class="stats">
      <strong>Legend:</strong><br/>
      <span style="color: #1f77b4;">● Subject</span><br/>
      <span style="color: #ff7f0e;">● Topic</span><br/>
      <span style="color: #2ca02c;">● Lesson</span><br/>
      <span style="color: #d62728;">● Level</span>
    </div>
  </div>
  
  <script>
    const nodeData = {json.dumps(nodes_data)};
    const edgeData = {json.dumps(edges_data)};
    
    // Simple force-directed layout (d3-lite)
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    const svg = d3.select("#canvas")
      .attr("width", width)
      .attr("height", height);
    
    // Color mapping
    const colorMap = {{
      "subject": "#1f77b4",
      "topic": "#ff7f0e",
      "lesson": "#2ca02c",
      "level": "#d62728"
    }};
    
    // Draw edges
    edgeData.forEach(edge => {{
      svg.append("line")
        .attr("x1", nodeData[edge.source].index % 10 * 80 + 100)
        .attr("y1", Math.floor(nodeData[edge.source].index / 10) * 80 + 100)
        .attr("x2", nodeData[edge.target].index % 10 * 80 + 100)
        .attr("y2", Math.floor(nodeData[edge.target].index / 10) * 80 + 100)
        .attr("stroke", "#999")
        .attr("stroke-width", 1)
        .attr("opacity", 0.3);
    }});
    
    // Draw nodes
    nodeData.forEach((node, i) => {{
      const x = (i % 10) * 80 + 100;
      const y = Math.floor(i / 10) * 80 + 100;
      
      svg.append("circle")
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", 15)
        .attr("fill", colorMap[node.type] || "#999")
        .attr("opacity", 0.7)
        .attr("title", node.name);
      
      svg.append("text")
        .attr("x", x)
        .attr("y", y + 25)
        .attr("text-anchor", "middle")
        .attr("font-size", 10)
        .text(node.name.substring(0, 15));
    }});
  </script>
  
  <script src="https://d3js.org/d3.v7.min.js"></script>
</body>
</html>"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Exported HTML D3: {filepath}")


def export_summary_reports(graph, output_dir: Path):
    """Generate summary reports in multiple formats."""
    output_dir.mkdir(exist_ok=True)
    
    # Subject breakdown report
    report = "# AkuLearn Knowledge Graph Summary\n\n"
    report += f"**Total Nodes:** {len(graph.nodes)}\n"
    report += f"**Total Edges:** {len(graph.edges)}\n\n"
    
    stats = graph.stats()
    report += "## Node Types\n"
    for ntype, count in stats["node_types"].items():
        report += f"- {ntype}: {count}\n"
    
    report += "\n## Subjects\n"
    subjects = set()
    for node in graph.nodes.values():
        if node.metadata.get("subject"):
            subjects.add(node.metadata.get("subject"))
    
    for subj in sorted(subjects):
        lessons = len([n for n in graph.nodes.values() 
                      if n.type == "lesson" and n.metadata.get("subject") == subj])
        report += f"- {subj}: {lessons} lessons\n"
    
    with open(output_dir / "graph_summary.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Exported summary: {output_dir / 'graph_summary.md'}")


def main():
    print("\n=== Exporting Knowledge Graph ===\n")
    
    builder = CurriculumGraphBuilder()
    graph = builder.build()
    
    root = Path(__file__).parent
    
    # Export formats
    export_graphml(graph, root / "knowledge_graph.graphml")
    export_html_d3(graph, root / "knowledge_graph_viz.html")
    export_summary_reports(graph, root / "graph_exports")
    
    # Also export as JSON again
    graph.export_json(root / "knowledge_graph_full.json")
    
    print(f"\nExports complete!")
    print(f"  - GraphML: knowledge_graph.graphml (Gephi/Cytoscape)")
    print(f"  - HTML D3: knowledge_graph_viz.html (Browser)")
    print(f"  - JSON: knowledge_graph_full.json (Raw data)")
    print(f"  - Reports: graph_exports/ (Summary)")


if __name__ == "__main__":
    main()
