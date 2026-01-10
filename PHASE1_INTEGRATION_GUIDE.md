# Phase 1 Integration Guide

## Overview
This guide explains how to integrate Phase 1 generated assets (ASCII diagrams and truth tables) into your Akulearn platform.

## Backend Integration

### 1. Initialize Asset Loader

In your FastAPI main application file (`connected_stack/backend/main.py` or `src/backend/main.py`):

```python
from src.backend.asset_loader import initialize_asset_loader
from src.backend.api import assets as assets_router

# Add to startup event
@app.on_event("startup")
async def startup_event():
    # ... existing startup code ...
    
    # Initialize Phase 1 assets
    try:
        initialize_asset_loader("generated_assets")
        logger.info("Phase 1 assets loaded successfully")
    except FileNotFoundError as e:
        logger.warning(f"Phase 1 assets not available: {e}")

# Include the assets router
app.include_router(assets_router.router)
```

### 2. Asset API Endpoints

Once integrated, the following endpoints are available:

```
GET  /api/assets/summary
     - Get summary of all generated assets
     
GET  /api/assets/lesson/{lesson_id}
     - Get all assets for a specific lesson
     - Returns: { lesson_id, ascii_diagram?, truth_table? }
     
GET  /api/assets/ascii/{lesson_id}
     - Get ASCII diagram only (raw text)
     
GET  /api/assets/table/{lesson_id}
     - Get truth table only (raw HTML)

POST /api/assets/initialize
     - Initialize asset loader (call once)
```

### 3. Enrich Lessons with Assets

Option A: Manual Enrichment
```python
from src.backend.asset_loader import get_global_asset_loader

loader = get_global_asset_loader()
if loader:
    enriched_lesson = loader.enrich_lesson(lesson_dict)
```

Option B: Using Enrichment Service
```python
from src.backend.services.lesson_enrichment import get_enrichment_service

enrichment_service = get_enrichment_service()
enriched_lesson = enrichment_service.enrich_lesson(lesson_dict)
enriched_lessons = enrichment_service.enrich_lessons(lesson_list)
```

### 4. Modify Lesson Endpoints

To automatically include assets in lesson responses:

```python
@app.get("/api/lessons/{lesson_id}")
async def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter_by(id=lesson_id).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson_dict = lesson.to_dict()
    
    # Enrich with assets
    enrichment_service = get_enrichment_service()
    enriched_lesson = enrichment_service.enrich_lesson(lesson_dict)
    
    return enriched_lesson
```

## Frontend Integration

### 1. Using React Components

#### Display Lesson with Assets

```tsx
import LessonContent from '@/components/LessonContent';

function LessonPage({ lessonId }) {
  const [lesson, setLesson] = useState(null);

  useEffect(() => {
    // Fetch lesson (assets will be included if available)
    fetch(`/api/lessons/${lessonId}`)
      .then(r => r.json())
      .then(setLesson);
  }, [lessonId]);

  if (!lesson) return <div>Loading...</div>;

  return <LessonContent lesson={lesson} showAssets={true} />;
}
```

#### Individual Components

```tsx
import ASCIIDiagram from '@/components/ASCIIDiagram';
import TruthTable from '@/components/TruthTable';

// ASCII Diagram
<ASCIIDiagram 
  content={asciiContent}
  title="Process Flow"
  className="my-component"
/>

// Truth Table
<TruthTable 
  content={tableHtml}
  lessonId={lesson.id}
  onAnswersChange={(answers) => console.log(answers)}
  showSolution={false}
/>
```

### 2. Using the Custom Hook

```tsx
import useGeneratedAssets from '@/hooks/useGeneratedAssets';
import ASCIIDiagram from '@/components/ASCIIDiagram';
import TruthTable from '@/components/TruthTable';

function MyLessonComponent({ lessonId }) {
  const { 
    assets, 
    loading, 
    error, 
    hasAssets,
    hasASCII,
    hasTruthTable
  } = useGeneratedAssets(lessonId);

  if (loading) return <div>Loading visuals...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!hasAssets) return <div>No visuals for this lesson</div>;

  return (
    <div>
      {hasASCII && (
        <ASCIIDiagram content={assets.ascii_diagram.content} />
      )}
      {hasTruthTable && (
        <TruthTable content={assets.truth_table.content} />
      )}
    </div>
  );
}
```

## Asset Response Format

### Lesson with Assets
```json
{
  "id": "nerdc-further-math-ss1-sets-20251221-195949",
  "title": "Sets, Logic and Proof",
  "subject": "Further Mathematics",
  "content": "...",
  "generated_assets": {
    "ascii_diagram": {
      "type": "text",
      "content": "  ┌────────────┐\n  │   Item 1   │\n  └────────────┘\n        ↓",
      "format": "ascii"
    },
    "truth_table": {
      "type": "html",
      "content": "<div class='truth-table'>...</div>",
      "format": "interactive_html"
    }
  }
}
```

### Assets Endpoint Response
```json
{
  "lesson_id": "nerdc-further-math-ss1-sets-20251221-195949",
  "ascii_diagram": {
    "type": "text",
    "content": "  ┌────────────┐\n  │   Item 1   │\n  └────────────┘",
    "format": "ascii"
  },
  "truth_table": {
    "type": "html",
    "content": "<div class='truth-table'>...</div>",
    "format": "interactive_html"
  }
}
```

### Assets Summary Response
```json
{
  "total_ascii_diagrams": 52,
  "total_truth_tables": 52,
  "total_assets": 104,
  "by_subject": {
    "Mathematics": {"ascii": 4, "tables": 4},
    "Computer Science": {"ascii": 8, "tables": 8},
    ...
  },
  "by_type": {
    "flow": 20,
    "hierarchy": 15,
    "cycle": 10,
    "comparison": 7
  }
}
```

## Styling Customization

### CSS Classes Available

**ASCII Diagram:**
- `.ascii-diagram-container`
- `.ascii-diagram-title`
- `.ascii-diagram-wrapper`
- `.ascii-diagram-content`
- `.ascii-diagram-copy-btn`

**Truth Table:**
- `.truth-table-container`
- `.truth-table-header`
- `.truth-table-wrapper`
- `.truth-table-controls`
- `.truth-table-btn-submit`
- `.truth-table-btn-reset`
- `.truth-table-feedback`

**Lesson Content:**
- `.lesson-content`
- `.lesson-header`
- `.lesson-body`
- `.lesson-assets`
- `.assets-container`
- `.assets-title`

### Custom Styling Example

```tsx
<ASCIIDiagram 
  content={content}
  className="my-custom-class"
/>

<style jsx>{`
  :global(.ascii-diagram-container) {
    border-color: #ff6b6b;
    background: #fff5f5;
  }
  
  :global(.ascii-diagram-content) {
    background: #f0f0f0;
    font-size: 14px;
  }
`}</style>
```

## Troubleshooting

### Assets Not Loading

1. **Check Asset Files Exist**
   ```bash
   ls -la generated_assets/
   ls -la generated_assets/ascii/
   ls -la generated_assets/tables/
   ```

2. **Verify Manifest**
   ```bash
   cat generated_assets/phase1_manifest.json
   ```

3. **Check API Endpoint**
   ```bash
   curl http://localhost:8000/api/assets/summary
   ```

### Asset Loader Not Initialized

1. Ensure `initialize_asset_loader()` is called in startup
2. Check for FileNotFoundError in logs
3. Verify `generated_assets` directory exists in correct location

### Frontend Not Showing Assets

1. Check browser console for API errors
2. Verify lesson has `generated_assets` field
3. Check component CSS is loading
4. Use React DevTools to inspect component state

## Performance Considerations

- Assets are cached in memory after first load
- Each lesson is fetched only once
- HTML truth tables are rendered inline (no external dependencies)
- ASCII diagrams use monospace font (pre-rendered)
- Consider lazy-loading assets for lesson lists

## Next Steps

- **Phase 2:** Mathematical graphing engine (matplotlib/plotly)
- **Phase 3:** Specialized diagrams (chemistry, circuits)
- **Phase 4:** Interactive simulations and games

---

For questions or issues, refer to the project documentation or contact the development team.
