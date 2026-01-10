# Phase 3 Integration Guide

Complete guide for integrating Phase 3 specialized diagrams into Akulearn.

## 📋 Overview

Phase 3 provides **100 specialized educational diagrams** across 7 types:
- **Venn Diagrams** (16): Set theory visualization
- **Flowcharts** (10): Algorithm and process flows
- **Timelines** (0): Historical events (infrastructure ready)
- **Electrical Circuits** (22): Series/parallel circuits with components
- **Logic Circuits** (40): AND/OR/NOT gates
- **Molecular Structures** (0): Atom bonds (infrastructure ready)
- **Chemical Reactions** (12): Reactants → Products

---

## 🏗️ Architecture

### Backend Components

```
src/backend/
├── phase3_asset_loader.py      # Asset management (extends ExtendedAssetLoader)
├── extended_asset_loader.py    # Phase 1 & 2 loader
└── api/
    ├── assets_v3.py            # Phase 3 REST API endpoints
    ├── assets_v2.py            # Phase 2 endpoints
    └── assets.py               # Phase 1 endpoints
```

### Frontend Components

```
src/frontend/
├── hooks/
│   └── usePhase3Diagrams.ts    # React hook for diagram fetching
└── components/
    ├── VennDiagramViewer.tsx   # Venn diagram display
    ├── FlowchartViewer.tsx     # Flowchart with pan/zoom
    ├── CircuitViewer.tsx       # Circuit diagrams (electrical & logic)
    ├── ChemistryViewer.tsx     # Chemistry diagrams
    └── Phase3DiagramsGallery.tsx  # Unified gallery view
```

### Generated Assets

```
generated_assets/
├── phase3_manifest.json        # Complete registry
├── diagrams/                   # Phase 3 SVG files (100 diagrams)
├── graphs/                     # Phase 2 graphs (70 files)
├── ascii/                      # Phase 1 ASCII (52 files)
└── tables/                     # Phase 1 tables (52 files)
```

---

## 🚀 Backend Integration

### Step 1: Initialize Asset Loader

```python
from src.backend.phase3_asset_loader import initialize_phase3_loader, get_phase3_loader

# Initialize on app startup
loader = initialize_phase3_loader("generated_assets")

# Access later
loader = get_phase3_loader()
```

### Step 2: Mount API Router

```python
from fastapi import FastAPI
from src.backend.api.assets_v3 import router as phase3_router

app = FastAPI()

# Mount Phase 3 endpoints
app.include_router(phase3_router)  # Prefix: /api/assets/phase3
```

### Step 3: Enrich Lessons

```python
from src.backend.phase3_asset_loader import Phase3AssetLoader

loader = Phase3AssetLoader()

# Enrich single lesson with all assets (Phase 1, 2, 3)
lesson = {
    "id": "nerdc-further-math-ss1-sets-20251221-195949",
    "title": "Set Theory",
    "subject": "Further Mathematics"
}

enriched_lesson = loader.enrich_lesson(lesson)

# enriched_lesson now contains:
# - generated_assets (Phase 1 & 2)
# - phase3_diagrams (Phase 3)
#   - venn_diagrams: [...]
#   - flowcharts: [...]
#   - circuits: [...]
#   - chemistry: [...]
# - phase3_diagram_count: N
```

---

## 🌐 API Endpoints

### Base URL
```
http://localhost:8000/api/assets/phase3
```

### Available Endpoints

#### 1. Get Phase 3 Summary
```http
GET /api/assets/phase3/summary
```

**Response:**
```json
{
  "total_diagrams": 100,
  "venn_diagrams": 16,
  "flowcharts": 10,
  "timelines": 0,
  "electrical_circuits": 22,
  "logic_circuits": 40,
  "molecular_structures": 0,
  "chemical_reactions": 12,
  "generated_at": "2026-01-10T12:00:00"
}
```

#### 2. Get Diagrams for Lesson
```http
GET /api/assets/phase3/lesson/{lesson_id}
```

**Example:**
```bash
curl http://localhost:8000/api/assets/phase3/lesson/nerdc-further-math-ss1-sets-20251221-195949
```

**Response:**
```json
{
  "venn_diagrams": [
    {
      "id": "venn_2_nerdc-further-math-ss1-sets-20251221-195949_62649361",
      "title": "Set Operations",
      "type": "venn_2",
      "path": "generated_assets/diagrams/...",
      "subject": "Further Mathematics"
    }
  ],
  "flowcharts": [],
  "electrical_circuits": [],
  "logic_circuits": [],
  "chemical_reactions": []
}
```

#### 3. Get Diagram SVG Content
```http
GET /api/assets/phase3/diagram/{diagram_id}
```

**Response:**
```json
{
  "id": "venn_2_...",
  "title": "Set Operations",
  "type": "venn_2",
  "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\">...</svg>"
}
```

#### 4. Get Diagrams by Type
```http
GET /api/assets/phase3/type/{diagram_type}?lesson_id={optional}
```

**Types:** `venn_2`, `venn_3`, `flowchart`, `circuit_electrical`, `circuit_logic`, `chemistry_reaction`

#### 5. Initialize Loader
```http
POST /api/assets/phase3/initialize?assets_dir=generated_assets
```

---

## ⚛️ Frontend Integration

### Step 1: Install Hook

```tsx
import { usePhase3Diagrams } from '@/hooks/usePhase3Diagrams';
```

### Step 2: Fetch Diagrams for Lesson

```tsx
function LessonPage({ lessonId }: { lessonId: string }) {
  const { diagrams, loading, error } = usePhase3Diagrams(lessonId);

  if (loading) return <div>Loading diagrams...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h2>Lesson Diagrams</h2>
      {diagrams?.venn_diagrams.map(diagram => (
        <VennDiagramViewer key={diagram.id} diagramId={diagram.id} />
      ))}
    </div>
  );
}
```

### Step 3: Use Individual Viewers

#### Venn Diagrams
```tsx
import VennDiagramViewer from '@/components/VennDiagramViewer';

<VennDiagramViewer
  diagramId="venn_2_..."
  title="Set Operations"
  showControls={true}
/>
```

#### Flowcharts
```tsx
import FlowchartViewer from '@/components/FlowchartViewer';

<FlowchartViewer
  diagramId="flowchart_..."
  title="Algorithm Flow"
  showControls={true}
/>
```

#### Circuits
```tsx
import CircuitViewer from '@/components/CircuitViewer';

<CircuitViewer
  diagramId="circuit_electrical_..."
  circuitType="electrical"
  title="Series Circuit"
/>
```

#### Chemistry
```tsx
import ChemistryViewer from '@/components/ChemistryViewer';

<ChemistryViewer
  diagramId="chemistry_reaction_..."
  chemistryType="reaction"
  title="Chemical Reaction"
/>
```

### Step 4: Use Gallery View

```tsx
import Phase3DiagramsGallery from '@/components/Phase3DiagramsGallery';

<Phase3DiagramsGallery lessonId="nerdc-further-math-ss1-sets-..." />
```

---

## 🧪 Testing

### Run Integration Tests

```bash
# Run all Phase 3 tests
pytest test_phase3_integration.py -v

# Run specific test class
pytest test_phase3_integration.py::TestPhase3AssetLoader -v

# Run with coverage
pytest test_phase3_integration.py --cov=src.backend.phase3_asset_loader
```

### Test Coverage

The test suite covers:
- ✅ Asset loader initialization
- ✅ Manifest loading and validation
- ✅ Diagram retrieval (by lesson, by ID, by type)
- ✅ SVG content loading
- ✅ Lesson enrichment
- ✅ Statistics generation
- ✅ File integrity
- ✅ Global loader singleton

### Manual API Testing

```bash
# Test summary endpoint
curl http://localhost:8000/api/assets/phase3/summary

# Test lesson diagrams
curl http://localhost:8000/api/assets/phase3/lesson/nerdc-further-math-ss1-sets-20251221-195949

# Test diagram content
curl http://localhost:8000/api/assets/phase3/diagram/venn_2_nerdc-further-math-ss1-sets-20251221-195949_62649361

# Test by type
curl http://localhost:8000/api/assets/phase3/type/circuit_logic
```

---

## 📊 Asset Management

### Manifest Structure

```json
{
  "venn_diagrams": [...],
  "flowcharts": [...],
  "timelines": [],
  "electrical_circuits": [...],
  "logic_circuits": [...],
  "molecular_structures": [],
  "chemical_reactions": [...],
  "metadata": {
    "phase": 3,
    "generated_at": "2026-01-10T...",
    "total_diagrams": 100,
    "venn_diagrams_count": 16,
    "flowcharts_count": 10,
    "electrical_circuits_count": 22,
    "logic_circuits_count": 40,
    "chemical_reactions_count": 12
  }
}
```

### Regenerate Diagrams

```bash
# Regenerate all diagrams
python phase3_generator.py phase3_diagram_specs.json

# Extract new specs from lessons
python phase3_content_extractor.py

# Full regeneration pipeline
python phase3_content_extractor.py && python phase3_generator.py phase3_diagram_specs.json
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Assets directory
ASSETS_DIR=generated_assets

# API base URL (frontend)
VITE_API_BASE_URL=http://localhost:8000
```

### Asset Loader Options

```python
# Custom assets directory
loader = Phase3AssetLoader(assets_dir="custom_assets")

# Disable caching (for development)
loader._diagram_cache.clear()
```

---

## 🎨 Customization

### Custom Diagram Styles

Add CSS to override default styles:

```css
/* Venn diagram customization */
.venn-diagram-viewer {
  border-color: #your-color;
  background: #your-bg;
}

/* Circuit diagram customization */
.circuit-viewer.circuit-electrical {
  border-color: #your-color;
}
```

### Custom Zoom Controls

```tsx
<VennDiagramViewer
  diagramId="..."
  showControls={false}  // Hide default controls
/>

{/* Add your custom controls */}
<button onClick={() => setCustomZoom(zoom + 0.1)}>Zoom In</button>
```

---

## 🐛 Troubleshooting

### Issue: Diagrams not loading

**Check:**
1. Manifest file exists: `generated_assets/phase3_manifest.json`
2. SVG files exist in `generated_assets/diagrams/`
3. Loader initialized: `initialize_phase3_loader()`
4. API router mounted correctly

### Issue: Empty diagram list

**Possible causes:**
- Lesson ID mismatch
- No diagrams generated for that lesson
- Manifest not loaded

**Solution:**
```python
# Check what's in the manifest
manifest = loader.load_phase3_manifest()
print(f"Total diagrams: {manifest['metadata']['total_diagrams']}")

# Check specific lesson
diagrams = loader.get_diagrams_for_lesson(lesson_id)
print(f"Found {len(diagrams)} diagrams")
```

### Issue: SVG rendering issues

**Check:**
1. SVG content is valid: `assert "<svg" in content`
2. dangerouslySetInnerHTML used correctly
3. No conflicting CSS styles

---

## 📈 Performance

### Caching

Phase 3 loader implements automatic caching:
- **Manifest caching**: Loaded once on initialization
- **SVG caching**: Loaded on first access, cached thereafter
- **Clear cache**: `loader._diagram_cache.clear()`

### Optimization Tips

1. **Lazy load diagrams**: Only fetch when needed
2. **Use pagination**: Load diagrams in batches for large lessons
3. **Optimize SVG**: Minify SVG files for production
4. **CDN delivery**: Serve static SVG files via CDN

---

## 🚢 Deployment Checklist

- [ ] Generate all Phase 3 diagrams
- [ ] Verify manifest integrity
- [ ] Run integration tests (all passing)
- [ ] Initialize loader in app startup
- [ ] Mount API router
- [ ] Build frontend with Phase 3 components
- [ ] Test API endpoints
- [ ] Verify diagram rendering
- [ ] Set up asset CDN (optional)
- [ ] Configure caching headers

---

## 📚 Additional Resources

- **Phase 3 Status**: [PHASE3_STATUS.md](PHASE3_STATUS.md)
- **Architecture**: [PHASE3_ARCHITECTURE.md](PHASE3_ARCHITECTURE.md) (if exists)
- **Phase 1 Guide**: [PHASE1_INTEGRATION_GUIDE.md](PHASE1_INTEGRATION_GUIDE.md)
- **Phase 2 Guide**: [PHASE2_INTEGRATION_GUIDE.md](PHASE2_INTEGRATION_GUIDE.md)
- **API Spec**: [API_SPECIFICATION.md](API_SPECIFICATION.md)

---

## 🎯 Next Steps

1. **Scale Generation**: Increase from 100 to 200+ diagrams
2. **Add Timeline Support**: Implement historical timeline generation
3. **Molecular Structures**: Complete chemistry molecular diagrams
4. **Interactive Features**: Add clickable elements, tooltips
5. **Export Options**: PDF, PNG export for diagrams
6. **Analytics**: Track diagram usage and effectiveness

---

**Phase 3 Integration Complete!** 🎉

For questions or issues, refer to the troubleshooting section or check the test suite for usage examples.
