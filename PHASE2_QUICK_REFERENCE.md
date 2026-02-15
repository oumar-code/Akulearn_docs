# Phase 2 Quick Reference

## What is Phase 2?

Phase 2 adds **interactive mathematical graphs and visualizations** to 36 lessons in the Akulearn platform. This includes 70 SVG-based graphs covering functions, statistics, and data visualization.

## Quick Stats

| Metric | Value |
|--------|-------|
| Lessons with graphs | 36/52 (69%) |
| Total graphs generated | 70 |
| Function graphs | 42 |
| Bar charts | 8 |
| Line charts | 20 |
| Average graphs/lesson | 2.3 |
| Graph file size | ~8KB each |
| Total Phase 2 size | ~560KB |

## Generated Graph Types

- **Function Graphs** (42)
  - Quadratic functions (y = ax² + bx + c)
  - Sine/cosine waves (trigonometric)
  - Exponential functions (y = e^x)

- **Bar Charts** (8)
  - Categorical data comparisons
  - Statistical distributions
  - Growth/decline patterns

- **Line Charts** (20)
  - Trend analysis
  - Time series data
  - Multi-line comparisons

## Key Files

### Backend
```
src/backend/
├── extended_asset_loader.py  # ← NEW: Asset loading for Phase 1 & 2
├── api/
│   └── assets_v2.py          # ← NEW: Extended API endpoints
└── services/
    └── lesson_enrichment.py   # Enriches lessons with assets
```

### Frontend
```
src/frontend/
├── components/
│   ├── MathGraph.tsx          # ← NEW: Interactive graph viewer
│   └── LessonContent.tsx      # Updated to show graphs
└── hooks/
    └── useMathGraphs.ts       # ← NEW: Graph data fetching hook
```

### Generated Assets
```
generated_assets/
├── phase2_manifest.json       # ← NEW: Graph registry (70 items)
├── graphs/                    # ← NEW: 70 SVG files
│   ├── graph_001.svg
│   ├── graph_002.svg
│   └── ...
```

## Getting Started (5 minutes)

### 1. Initialize Loader
```python
from src.backend.extended_asset_loader import initialize_extended_loader

# Call once on startup
loader = initialize_extended_loader("generated_assets")
```

### 2. Include API
```python
from src.backend.api.assets_v2 import router as assets_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(assets_router)
```

### 3. Use in Frontend
```tsx
import MathGraph from '@/components/MathGraph';
import useMathGraphs from '@/hooks/useMathGraphs';

function MyLesson() {
  const { graphs, loading } = useMathGraphs('lesson_123');
  
  return graphs?.function_graphs?.map(g => (
    <MathGraph key={g.id} svgContent={g.content} title={g.title} />
  ));
}
```

## API Cheat Sheet

### Get all graphs for lesson
```bash
GET /api/assets/graphs/lesson/lesson_123
```
Returns: Collection of graphs by type

### Get specific graph
```bash
GET /api/assets/graph/graph_001
```
Returns: SVG content for rendering

### Get all Function Graphs
```bash
GET /api/assets/graphs/type/function_graphs
```
Returns: All 42 function graphs

### Get everything
```bash
GET /api/assets/summary
```
Returns: Phase 1 + Phase 2 statistics

## Component Usage

### MathGraph Props
```typescript
<MathGraph
  svgContent={svgString}        // Required: SVG markup
  title="Quadratic Function"    // Optional: Display title
  width="100%"                  // Optional: Container width
  height="400px"                // Optional: Container height
  interactive={true}            // Optional: Enable zoom/pan
  onExport={(png) => {...}}     // Optional: Export callback
/>
```

### useMathGraphs Return
```typescript
{
  graphs: {
    function_graphs: [...],
    bar_charts: [...],
    pie_charts: [...],
    line_charts: [...]
  },
  loading: boolean,
  error: string | null,
  hasGraphs: boolean,
  graphCount: number,
  reload: () => Promise<void>,
  getAllGraphs: () => GraphAsset[]
}
```

## Interactive Features

### Zoom Controls
- 🔍+ Button: Zoom in (max 3x)
- 🔍− Button: Zoom out (min 0.5x)
- Scroll: Wheel to zoom
- Display: Shows current zoom %

### Pan Control
- Drag: Click and drag to move around

### Other Controls
- ↺ Reset: Return to original view
- ⬇ Export: Save as PNG

## Testing

### Run Integration Tests
```bash
python test_phase2_integration.py
```

Expected: 6/6 tests passing

### Manual Testing
1. Open lesson with graphs
2. Verify graphs load
3. Test zoom (scroll wheel)
4. Test pan (click+drag)
5. Test export (export button)

## Troubleshooting

### Graphs not showing?
- Check: `generated_assets/phase2_manifest.json` exists
- Check: SVG files in `generated_assets/graphs/` exist
- Check: API endpoint returns data (call `/api/assets/summary`)

### Zoom/pan not working?
- Verify: `interactive={true}` prop on MathGraph
- Verify: Component is properly mounted
- Check: Browser console for errors

### Export not working?
- Verify: Browser allows downloads
- Verify: SVG content is valid
- Try: Different browser/OS

## Lesson Coverage by Subject

| Subject | Lessons | Graphs |
|---------|---------|--------|
| Mathematics | 14 | 32 |
| Physics | 8 | 18 |
| Biology | 4 | 8 |
| Economics | 5 | 10 |
| Chemistry | 3 | 2 |
| **Total** | **36** | **70** |

## Migration from Phase 1

**No breaking changes!** Phase 1 assets still work:

```python
# Old Phase 1 loader still works
from src.backend.asset_loader import Phase1AssetLoader
loader = Phase1AssetLoader()

# New Phase 2 features also available
from src.backend.extended_asset_loader import ExtendedAssetLoader
loader = ExtendedAssetLoader()  # ← Supports both phases
```

## Common Tasks

### Add graphs to lesson display
```tsx
const lesson = await fetchLesson('lesson_123');
const enriched = enrichWithGraphs(lesson);
// enriched.generated_assets.graphs now included
```

### Display all graphs for subject
```tsx
const response = await fetch('/api/assets/graphs/type/function_graphs');
const graphs = await response.json();
return graphs.graphs.map(g => <MathGraph {...} />);
```

### Export graph as image
```tsx
<MathGraph
  svgContent={svgContent}
  onExport={(pngDataUrl) => {
    // Send to server or download
    const link = document.createElement('a');
    link.href = pngDataUrl;
    link.download = 'graph.png';
    link.click();
  }}
/>
```

## Performance Tips

1. **Lazy load graphs**: Only fetch when needed
2. **Cache SVG content**: Reuse from state
3. **Use virtual scrolling**: For many graphs
4. **Optimize SVG**: Minimize file size
5. **CDN delivery**: Serve from edge

## Next Steps

1. ✅ Phase 2: Mathematical graphs (COMPLETE)
2. → Phase 3: Specialized diagrams (chemistry, circuits)
3. → Phase 4: Interactive games & simulations

## Support & Documentation

- [Full Integration Guide](../PHASE2_INTEGRATION_GUIDE.md)
- [Architecture Document](../PHASE2_ARCHITECTURE.md)
- [Backend Guide](../BACKEND_IMPLEMENTATION_GUIDE.md)
- [API Specification](../API_SPECIFICATION.md)

## Related Files

- Generator: `phase2_generator.py`
- Analyzer: `phase2_analyzer.py`
- Tests: `test_phase2_integration.py`
- Manifest: `generated_assets/phase2_manifest.json`
- Graphs: `generated_assets/graphs/*.svg`
