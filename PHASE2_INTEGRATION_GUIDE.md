# Phase 2: Mathematical Graphing Engine - Integration Guide

## Overview

Phase 2 extends the Akulearn platform with **mathematical graph generation and visualization**. This phase creates 70 SVG-based mathematical graphs across 36 lessons, providing interactive visual representations of mathematical concepts.

## Components

### 1. Backend Components

#### Extended Asset Loader (`src/backend/extended_asset_loader.py`)
- **Purpose**: Manages both Phase 1 and Phase 2 generated assets
- **Key Classes**: `ExtendedAssetLoader`
- **Methods**:
  - `get_graphs_for_lesson(lesson_id)` - Returns graphs grouped by type
  - `get_graph_svg(graph_id)` - Returns raw SVG content
  - `get_all_graphs_for_lesson(lesson_id)` - Flattened graph list
  - `enrich_lesson(lesson)` - Adds graphs to lesson object
  - `get_assets_summary()` - Summary statistics for all assets

#### Extended Assets API (`src/backend/api/assets_v2.py`)
- **Purpose**: REST API endpoints for asset retrieval
- **New Endpoints for Phase 2**:
  - `GET /api/assets/graphs/lesson/{lesson_id}` - Get all graphs for a lesson
  - `GET /api/assets/graph/{graph_id}` - Get specific graph SVG
  - `GET /api/assets/graphs/type/{graph_type}` - Get graphs by type
  - `GET /api/assets/summary` - Updated to include Phase 2 statistics

### 2. Frontend Components

#### MathGraph Component (`src/frontend/components/MathGraph.tsx`)
- **Purpose**: Interactive SVG graph viewer
- **Features**:
  - Zoom in/out (0.5x to 3x scale)
  - Pan via drag
  - Export to PNG
  - Reset view button
  - Responsive design
  - Accessibility support

#### useMathGraphs Hook (`src/frontend/hooks/useMathGraphs.ts`)
- **Purpose**: React hook for loading graphs from API
- **Returns**:
  - `graphs` - Organized graph data by type
  - `loading` - Loading state
  - `error` - Error messages
  - `hasGraphs` - Boolean indicating if graphs exist
  - `getAllGraphs()` - Helper to get flattened list

### 3. Generated Assets

#### Graph Manifest (`generated_assets/phase2_manifest.json`)
```json
{
  "function_graphs": [
    {
      "id": "graph_001",
      "lesson_id": "lesson_123",
      "title": "Quadratic Function",
      "type": "function_graph",
      "subject": "Mathematics",
      "path": "generated_assets/graphs/graph_001.svg"
    }
  ],
  "bar_charts": [...],
  "pie_charts": [...],
  "line_charts": [...]
}
```

#### Graph Types

| Type | Count | Use Cases |
|------|-------|-----------|
| Function Graphs | 42 | Quadratic, sine, exponential functions |
| Bar Charts | 8 | Data comparisons, statistics |
| Line Charts | 20 | Trends, time series data |
| Pie Charts | 0 | Proportions (generated on-demand) |

## Integration Steps

### Step 1: Initialize Extended Loader

```python
from src.backend.extended_asset_loader import initialize_extended_loader

# Call once on app startup
loader = initialize_extended_loader("generated_assets")
```

### Step 2: Register API Router

In your FastAPI application:

```python
from src.backend.api.assets_v2 import router as assets_router

app.include_router(assets_router)
```

### Step 3: Use Frontend Components

```tsx
import MathGraph from '@/components/MathGraph';
import useMathGraphs from '@/hooks/useMathGraphs';

function LessonView({ lessonId }) {
  const { graphs, loading, error, hasGraphs } = useMathGraphs(lessonId);
  
  if (loading) return <div>Loading graphs...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!hasGraphs) return <div>No graphs for this lesson</div>;
  
  return (
    <div>
      {graphs?.function_graphs?.map(graph => (
        <MathGraph
          key={graph.id}
          svgContent={graph.content}
          title={graph.title}
        />
      ))}
    </div>
  );
}
```

## API Usage Examples

### Get all graphs for a lesson

```bash
curl http://localhost:8000/api/assets/graphs/lesson/math-lesson-001
```

Response:
```json
{
  "function_graphs": [
    {
      "id": "graph_001",
      "title": "Quadratic Function",
      "type": "function_graph",
      "path": "generated_assets/graphs/graph_001.svg",
      "subject": "Mathematics"
    }
  ],
  "bar_charts": [],
  "pie_charts": [],
  "line_charts": []
}
```

### Get specific graph SVG

```bash
curl http://localhost:8000/api/assets/graph/graph_001
```

Response:
```json
{
  "graph_id": "graph_001",
  "type": "svg",
  "content": "<svg>...</svg>"
}
```

### Get graphs by type

```bash
curl "http://localhost:8000/api/assets/graphs/type/function_graphs"
```

### Get asset summary

```bash
curl http://localhost:8000/api/assets/summary
```

Response includes Phase 1 and Phase 2 statistics.

## Data Flow

```
User Request
    ↓
Frontend (React Component)
    ↓
useMathGraphs Hook
    ↓
/api/assets/graphs/lesson/{id}
    ↓
Extended Asset Loader
    ↓
Phase 2 Manifest + Graph Files
    ↓
SVG Content
    ↓
MathGraph Component (Interactive Viewer)
    ↓
Rendered Graph with Zoom/Pan
```

## Testing

Run integration tests:

```bash
python test_phase2_integration.py
```

Expected output:
```
============================================================
Phase 2 Integration Tests
============================================================
TEST 1: Extended Loader Initialization
  ✓ Loader initialized successfully
  ✓ Phase 1 manifest loaded: 52 ASCII + 52 tables
  ✓ Phase 2 manifest loaded: 70 graphs

TEST 2: Phase 2 Graph Loading
  ✓ Found graphs for lesson...

...

Test Results: 6/6 passed
```

## Performance Considerations

### Caching
- Graph SVG content is cached in memory after first retrieval
- Manifest is loaded once on initialization
- Use `reload()` method on hook to refresh

### File Size
- Average graph SVG: ~8KB
- Total Phase 2 assets: ~560KB
- Minimal network overhead due to SVG compression

### Rendering
- SVG rendering is GPU-accelerated in modern browsers
- Large graphs (>20KB) may require progressive loading
- Use `loading` state from hook for UX feedback

## Migration from Phase 1

The extended asset loader maintains full backward compatibility:

```python
# Old code still works
old_loader = Phase1AssetLoader("generated_assets")
ascii = old_loader.get_ascii_diagram("lesson_1")

# New code with Phase 2 support
new_loader = ExtendedAssetLoader("generated_assets")
graphs = new_loader.get_graphs_for_lesson("lesson_1")
```

## Troubleshooting

### Graphs not loading
1. Verify Phase 2 manifest exists: `generated_assets/phase2_manifest.json`
2. Check graph files exist: `generated_assets/graphs/*.svg`
3. Check API initialization: `POST /api/assets/initialize`

### SVG rendering issues
1. Verify SVG content is valid XML
2. Check browser console for errors
3. Test with simpler graph first

### Performance issues
1. Check browser DevTools for slow rendering
2. Reduce graph complexity in generator
3. Implement progressive loading for large batches

## Next Phases

**Phase 3**: Specialized Diagrams
- Chemistry structures (molecular diagrams)
- Circuit diagrams
- Venn diagrams
- Flow charts

**Phase 4**: Interactive Games
- Graph matching games
- Equation solvers
- Interactive simulations

## Related Files

- [Phase 1 Integration](../PHASE1_INTEGRATION_GUIDE.md)
- [Backend Implementation](../BACKEND_IMPLEMENTATION_GUIDE.md)
- [API Specification](../API_SPECIFICATION.md)
