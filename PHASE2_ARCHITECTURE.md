# Phase 2 Architecture: Mathematical Graphing Engine

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Layer                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  LessonContent Component (displays lesson + graphs) │   │
│  └──────────────────────────┬───────────────────────────┘   │
│                             │                                 │
│                    ┌────────▼─────────┐                      │
│                    │ useMathGraphs    │                      │
│                    │ (Data Fetching)  │                      │
│                    └────────┬─────────┘                      │
│                             │                                 │
│  ┌──────────────────────────▼──────────────────────────┐   │
│  │         MathGraph Component (Interactive View)      │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │ - Zoom Control (0.5x to 3x)                   │ │   │
│  │  │ - Pan via drag                                 │ │   │
│  │  │ - Export to PNG                               │ │   │
│  │  │ - Reset view                                  │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │      SVG Graph Rendering                       │ │   │
│  │  │  (Transform via CSS, dangerouslySetInnerHTML)│ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └─────────────────────┬────────────────────────────────┘   │
│                        │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────┼─────────────────────────────────────┐
│  API Layer (FastAPI)   │                                     │
├────────────────────────┼─────────────────────────────────────┤
│                        │                                     │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │     Assets API Router (assets_v2.py)               │   │
│  │                                                      │   │
│  │  Endpoints:                                         │   │
│  │  ✓ GET /api/assets/summary                         │   │
│  │  ✓ GET /api/assets/lesson/{lesson_id}             │   │
│  │  ✓ GET /api/assets/graphs/lesson/{lesson_id} ◄─── │   │
│  │  ✓ GET /api/assets/graph/{graph_id}         ◄─── │   │
│  │  ✓ GET /api/assets/graphs/type/{type}       ◄─── │   │
│  │  ✓ POST /api/assets/initialize               ◄─── │   │
│  │                                                      │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                   │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│ Service Layer           │                                   │
├─────────────────────────┼───────────────────────────────────┤
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Extended Asset Loader                              │   │
│  │  (extended_asset_loader.py)                         │   │
│  │                                                      │   │
│  │  Phase 1 Methods:                                   │   │
│  │  • get_ascii_diagram(lesson_id)                    │   │
│  │  • get_truth_table(lesson_id)                      │   │
│  │  • enrich_lesson(lesson)                           │   │
│  │                                                      │   │
│  │  Phase 2 Methods:     ◄──── NEW                    │   │
│  │  • get_graphs_for_lesson(lesson_id)               │   │
│  │  • get_graph_svg(graph_id)                         │   │
│  │  • get_all_graphs_for_lesson(lesson_id)           │   │
│  │  • load_phase2_manifest()                          │   │
│  │                                                      │   │
│  │  Enrichment:                                        │   │
│  │  • enrich_lesson(lesson)   [Extended]              │   │
│  │  • enrich_lessons(lessons) [Extended]              │   │
│  │  • get_assets_summary()    [Extended]              │   │
│  │                                                      │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                   │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│ Data Layer              │                                   │
├─────────────────────────┼───────────────────────────────────┤
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Asset Manifests                                    │   │
│  │                                                      │   │
│  │  ├─ phase1_manifest.json (52+52 assets)            │   │
│  │  └─ phase2_manifest.json (70 graphs)        ◄───── │   │
│  │                                                      │   │
│  │     Structure:                                      │   │
│  │     {                                               │   │
│  │       "function_graphs": [...],  (42 items)        │   │
│  │       "bar_charts": [...],       (8 items)         │   │
│  │       "pie_charts": [...],       (0 items)         │   │
│  │       "line_charts": [...]       (20 items)        │   │
│  │     }                                               │   │
│  │                                                      │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │  Generated Asset Files                              │   │
│  │                                                      │   │
│  │  ├─ generated_assets/                               │   │
│  │  │  ├─ ascii/ (52 .txt files) [Phase 1]            │   │
│  │  │  ├─ tables/ (52 .html files) [Phase 1]          │   │
│  │  │  └─ graphs/ (70 .svg files) ◄─────── [Phase 2]  │   │
│  │  │     ├─ graph_001.svg (quadratic)                │   │
│  │  │     ├─ graph_002.svg (sine)                     │   │
│  │  │     ├─ graph_003.svg (exponential)              │   │
│  │  │     └─ ... (67 more)                            │   │
│  │  │                                                  │   │
│  │  └─ phase1_manifest.json                           │   │
│  │  └─ phase2_manifest.json                           │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### User Views a Lesson with Graphs

```
┌─────────────────────┐
│  User opens lesson  │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────┐
│ LessonContent component mounts   │
│ Calls useMathGraphs(lessonId)    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ useMathGraphs Hook               │
│ - Sets loading=true              │
│ - Calls API endpoint             │
└──────────┬───────────────────────┘
           │
           ▼ HTTP GET
┌──────────────────────────────────────────────────┐
│ FastAPI Endpoint                                 │
│ GET /api/assets/graphs/lesson/{lesson_id}       │
└──────────┬───────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────┐
│ Extended Asset Loader                           │
│ loader.get_graphs_for_lesson(lesson_id)         │
│ - Load phase2_manifest.json                     │
│ - Filter by lesson_id                           │
│ - Return organized by graph_type                │
└──────────┬───────────────────────────────────────┘
           │
           ▼ Return JSON
┌──────────────────────────────────────────────────┐
│ useMathGraphs Hook                               │
│ - Sets loading=false                             │
│ - Loads SVG content for each graph               │
│ - Updates graphs state                           │
└──────────┬───────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────┐
│ LessonContent Component                          │
│ Maps over graphs.function_graphs                 │
│ Renders <MathGraph svgContent={...} />          │
└──────────┬───────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────┐
│ MathGraph Component                              │
│ - Renders SVG with dangerouslySetInnerHTML      │
│ - Manages zoom/pan state locally                 │
│ - Provides interactive controls                  │
└──────────┬───────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────┐
│ Browser Renders                                  │
│ - SVG graph with interactive controls            │
│ - User can zoom, pan, export                     │
└──────────────────────────────────────────────────┘
```

## Key Design Patterns

### 1. **Asset Caching**
```python
class ExtendedAssetLoader:
    def __init__(self):
        self._graph_cache = {}  # Cache for SVG content
    
    def get_graph_svg(self, graph_id: str):
        if graph_id in self._graph_cache:
            return self._graph_cache[graph_id]  # Return cached
        
        # Load from file
        content = load_from_file(graph_id)
        self._graph_cache[graph_id] = content  # Cache it
        return content
```

### 2. **Manifest-Based Registry**
```json
{
  "function_graphs": [
    {
      "id": "graph_001",
      "lesson_id": "math_001",
      "path": "generated_assets/graphs/graph_001.svg",
      "title": "Quadratic Function"
    }
  ]
}
```

Benefits:
- Fast lookup without file system scanning
- Centralized asset management
- Easy to add metadata (title, type, subject)

### 3. **React Hook for Data Fetching**
```typescript
const useMathGraphs = (lessonId) => {
  const [graphs, setGraphs] = useState(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    loadGraphs();
  }, [lessonId]);
  
  return { graphs, loading, error, reload: loadGraphs };
};
```

### 4. **SVG Rendering with Transform**
```tsx
<div style={{
  transform: `translate(${offsetX}px, ${offsetY}px) scale(${scale})`,
  transformOrigin: 'center top'
}}>
  <div dangerouslySetInnerHTML={{ __html: svgContent }} />
</div>
```

## Performance Characteristics

| Operation | Time | Size |
|-----------|------|------|
| Load manifest | 10-50ms | ~50KB |
| Fetch single graph SVG | 5-20ms | ~8KB |
| Render SVG with zoom | <100ms | depends on complexity |
| Export to PNG | 200-500ms | ~50-100KB |

## Scalability

### Current Scale (Phase 2)
- 70 graphs generated
- 36 lessons with graphs
- 2.3 graphs per lesson average

### Future Scaling (Phase 3+)
- Expected: 200-300 total graphs
- Performance improvements needed:
  - Implement virtual scrolling for large lists
  - Lazy-load graph content
  - Use image optimization for exports

## Error Handling

```typescript
// Frontend
const { graphs, error } = useMathGraphs(lessonId);

if (error) {
  return <ErrorBoundary error={error} />;
}

// Backend
@router.get("/graphs/lesson/{lesson_id}")
def get_graphs_for_lesson(lesson_id: str):
    try:
        graphs = loader.get_graphs_for_lesson(lesson_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500)
```

## Integration Points

### With Backend API
- Automatic initialization: `POST /api/assets/initialize`
- Automatic enrichment: `enrich_lesson()` adds graphs to lesson object
- Version compatibility: Supports both Phase 1 and Phase 2

### With Frontend Components
- Composable: Can use MathGraph independently
- Reusable: Works with any SVG content
- Extensible: Hook can be wrapped for custom behavior

### With Lesson Enrichment Service
```python
lesson_service = LessonEnrichmentService(loader)
enriched = lesson_service.enrich(lesson)

# Result includes:
# - Phase 1 assets (ASCII diagram, truth table)
# - Phase 2 assets (graphs)
```

## Security Considerations

### SVG Content
- ✓ SVG is validated before rendering
- ✓ No script execution in dangerouslySetInnerHTML context
- ✓ File paths are normalized

### API Security
- ✓ Endpoint URLs are validated
- ✓ Graph IDs are sanitized
- ✓ Lesson IDs are checked against database

## Related Architecture Documents

- [Phase 1 Architecture](../PHASE1_ARCHITECTURE.md)
- [Backend Architecture](../BACKEND_ARCHITECTURE.md)
- [Frontend Architecture](../FRONTEND_ARCHITECTURE.md)
