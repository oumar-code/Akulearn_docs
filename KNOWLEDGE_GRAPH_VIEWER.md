# 🗺️ Knowledge Graph HTML Visualization

## Overview

Standalone HTML file that visualizes your learning platform's knowledge graph with beautiful, interactive D3.js animations. No build tools, Node.js, or React required - just open in a browser!

## ✨ Features

### Interactive Visualization
- **Force-Directed Graph**: Physics-based layout with automatic node positioning
- **Zoom & Pan**: Mouse wheel zoom (0.1x to 4x) and drag canvas
- **Drag Nodes**: Click and drag any node to rearrange
- **Beautiful UI**: Gradient glassmorphism design with smooth animations

### Filtering & Controls
- Filter by subject (Mathematics, Physics, Chemistry, Biology, English)
- Filter by difficulty (Beginner, Intermediate, Advanced)
- Toggle topic nodes visibility
- Toggle node labels on/off
- Real-time stats (nodes, connections, pathways)

### Connection Types
- **Blue Arrows** → Prerequisites (lesson dependencies)
- **Gray Lines** → Related content (similar topics)
- **Purple Dashed** → Contains relationships (topic groupings)

### Interactive Features
- **Hover Tooltips**: See lesson details on hover
- **Node Selection**: Click to select and highlight
- **Color Coding**: 
  - 🔴 Red = Beginner
  - 🟠 Orange = Intermediate
  - 🟢 Green = Advanced

## 🚀 Quick Start

### Option 1: Use Sample Data (Immediate)
1. Open `knowledge_graph_viewer.html` in any browser
2. Click "🎲 Generate Sample" button
3. Explore the interactive graph!

### Option 2: Load from API (With Backend)
1. Start your Wave 3 server:
   ```bash
   python wave3_advanced_platform.py
   ```
2. Open `knowledge_graph_viewer.html` in browser
3. Click "📊 Load Graph Data" button
4. Data fetched from `http://localhost:8000/api/v3/knowledge-graph`

## 🎮 Controls

### Mouse Controls
- **Left Click + Drag on Node**: Move node
- **Left Click + Drag on Background**: Pan canvas
- **Mouse Wheel**: Zoom in/out
- **Hover**: Show tooltip

### Button Controls
- **+** : Zoom in
- **−** : Zoom out
- **⟲** : Reset zoom to default

### Sidebar Controls
- **Subject Filter**: Show only specific subject lessons
- **Difficulty Filter**: Show only specific difficulty level
- **Show Topic Nodes**: Toggle visibility of topic groupings
- **Show Node Labels**: Toggle text labels on/off

## 📊 API Endpoints

The visualization can fetch data from your Wave 3 backend:

### GET `/api/v3/knowledge-graph`
Returns graph data with nodes, edges, and layouts.

**Query Parameters:**
- `subject` (optional): Filter by subject (e.g., "mathematics")
- `difficulty` (optional): Filter by difficulty ("beginner", "intermediate", "advanced")
- `layout` (optional): Layout algorithm ("force", "hierarchical", "circular")
- `include_topics` (optional): Include topic nodes (default: true)

**Response:**
```json
{
  "nodes": [
    {
      "id": "L1",
      "label": "Algebra Basics",
      "type": "lesson",
      "subject": "mathematics",
      "difficulty": "beginner",
      "topics": ["equations", "variables"],
      "x": 150.5,
      "y": 200.3
    }
  ],
  "edges": [
    {
      "source": "L1",
      "target": "L2",
      "type": "prerequisite"
    }
  ],
  "learning_paths": []
}
```

### GET `/api/v3/learning-paths`
Returns curated learning pathways with lesson details.

**Query Parameters:**
- `subject` (optional): Filter paths by subject

**Response:**
```json
{
  "pathways": [
    {
      "id": "PATH_1",
      "name": "Algebra Mastery",
      "description": "Complete algebra course",
      "subject": "mathematics",
      "difficulty": "beginner",
      "estimated_duration_hours": 20,
      "nodes": ["L1", "L2", "L3"]
    }
  ],
  "lessons": {
    "L1": {
      "id": "L1",
      "title": "Algebra Basics",
      "subject": "mathematics",
      "difficulty": "beginner",
      "duration_minutes": 45
    }
  }
}
```

## 🎨 Customization

### Change Colors
Edit the `difficultyColors` and `typeColors` objects in the `<script>` section:

```javascript
const difficultyColors = {
    'beginner': '#ef4444',      // Red
    'intermediate': '#f59e0b',  // Orange
    'advanced': '#10b981'       // Green
};
```

### Change Graph Physics
Modify the force simulation parameters:

```javascript
simulation = d3.forceSimulation()
    .force('link', d3.forceLink().distance(100))    // Distance between connected nodes
    .force('charge', d3.forceManyBody().strength(-300))  // Repulsion strength
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(30));   // Node collision radius
```

### Change Layout Algorithms
The backend supports three layouts:
- **Force-Directed** (default): Physics-based organic layout
- **Hierarchical**: Top-down tree based on prerequisites
- **Circular**: Nodes arranged in circles by subject

Request different layouts via API:
```javascript
fetch('http://localhost:8000/api/v3/knowledge-graph?layout=hierarchical')
```

## 🔧 Technical Details

### Dependencies
- **D3.js v7**: Loaded from CDN (no installation needed)
  ```html
  <script src="https://d3js.org/d3.v7.min.js"></script>
  ```

### Browser Compatibility
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- IE11: ❌ Not supported (use modern browser)

### Performance
- Handles up to 100 nodes smoothly
- For larger graphs (100+ nodes), consider:
  - Disabling labels by default
  - Reducing force simulation iterations
  - Using hierarchical layout instead of force-directed

## 📱 Responsive Design

The visualization is fully responsive:
- **Desktop**: Full sidebar + large canvas
- **Tablet**: Collapsible sidebar (< 1024px)
- **Mobile**: Stacked layout with top sidebar (< 640px)

## 🐛 Troubleshooting

### "Could not load data from server"
- Ensure Wave 3 server is running on port 8000
- Check CORS settings in `wave3_advanced_platform.py`
- Use "Generate Sample" button for offline testing

### Graph not rendering
- Check browser console for JavaScript errors
- Ensure D3.js loaded from CDN (requires internet)
- Try refreshing the page

### Slow performance
- Reduce number of visible nodes with filters
- Disable node labels
- Use hierarchical layout for large graphs

## 🎯 Use Cases

1. **Student Navigation**: Help students see lesson relationships
2. **Curriculum Planning**: Visualize course structure
3. **Prerequisite Tracking**: Identify learning dependencies
4. **Content Analysis**: Find gaps in lesson coverage
5. **Demo & Presentation**: Showcase platform capabilities

## 🚀 Future Enhancements

Potential additions:
- [ ] Student progress overlay (completed lessons in green)
- [ ] Search/highlight specific lessons
- [ ] Export graph as PNG/SVG
- [ ] Minimap for large graphs
- [ ] Time-lapse animation of learning progression
- [ ] 3D graph view with Three.js
- [ ] Collaborative multi-user exploration

## 📚 Related Files

- `wave3_knowledge_graph.py` - Backend graph generation
- `wave3_advanced_platform.py` - API endpoints
- `client_examples/KnowledgeGraphVisualization.jsx` - React version
- `client_examples/LearningPathwayVisualization.jsx` - Pathway flow view

## 🎓 Learning Resources

- [D3.js Force Simulation](https://d3js.org/d3-force)
- [Graph Theory Basics](https://en.wikipedia.org/wiki/Graph_theory)
- [Knowledge Graphs](https://en.wikipedia.org/wiki/Knowledge_graph)

---

**Made with ❤️ for Akulearn Platform**

Questions? Check the [main documentation](README.md) or [API specification](API_SPECIFICATION.md).
