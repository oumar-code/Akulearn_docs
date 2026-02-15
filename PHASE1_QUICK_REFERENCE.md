# Phase 1 Quick Reference

## 🚀 Fast Start (5 minutes)

### Backend Setup
```python
# 1. In your FastAPI app startup
from src.backend.asset_loader import initialize_asset_loader
from src.backend.api import assets as assets_router

@app.on_event("startup")
async def startup():
    initialize_asset_loader("generated_assets")

# 2. Include router
app.include_router(assets_router.router)

# Done! ✅
```

### Frontend Setup
```tsx
// 1. Use the pre-built component
import LessonContent from '@/components/LessonContent';

<LessonContent lesson={lesson} showAssets={true} />

// Done! ✅
```

---

## 📡 API Endpoints (Quick Reference)

```bash
# Get all assets summary
curl http://localhost:8000/api/assets/summary

# Get assets for a lesson
curl http://localhost:8000/api/assets/lesson/LESSON_ID

# Get just the ASCII diagram
curl http://localhost:8000/api/assets/ascii/LESSON_ID

# Get just the truth table
curl http://localhost:8000/api/assets/table/LESSON_ID

# Initialize assets
curl -X POST http://localhost:8000/api/assets/initialize
```

---

## 🧩 Component Usage Examples

### Simple: Use Everything
```tsx
import LessonContent from '@/components/LessonContent';

<LessonContent lesson={lessonData} />
```

### Advanced: Pick Components
```tsx
import useGeneratedAssets from '@/hooks/useGeneratedAssets';
import ASCIIDiagram from '@/components/ASCIIDiagram';
import TruthTable from '@/components/TruthTable';

function MyLesson({ lessonId }) {
  const { assets, loading, error } = useGeneratedAssets(lessonId);
  
  return (
    <div>
      {assets?.ascii_diagram && (
        <ASCIIDiagram content={assets.ascii_diagram.content} />
      )}
      {assets?.truth_table && (
        <TruthTable content={assets.truth_table.content} />
      )}
    </div>
  );
}
```

---

## 🔄 Backend Integration

### Enrich Lessons Automatically
```python
from src.backend.services.lesson_enrichment import get_enrichment_service

service = get_enrichment_service()

# Single lesson
enriched = service.enrich_lesson(lesson)

# Multiple lessons
enriched_list = service.enrich_lessons([lesson1, lesson2])
```

### Manual Enrichment
```python
from src.backend.asset_loader import get_global_asset_loader

loader = get_global_asset_loader()
enriched = loader.enrich_lesson(lesson)
```

---

## 📊 What's Available

| Item | Count |
|------|-------|
| Total Assets | 104 |
| ASCII Diagrams | 52 |
| Truth Tables | 52 |
| Subjects Covered | 9 |
| Lessons Enhanced | 52 |

---

## 🎨 Customization

### Styling
```tsx
<ASCIIDiagram 
  content={content}
  className="custom-class"
/>

<style jsx>{`
  :global(.ascii-diagram-container) {
    border-color: #your-color;
  }
`}</style>
```

### Loading Custom API Base
```tsx
const { assets } = useGeneratedAssets(lessonId, {
  apiBaseUrl: 'https://api.example.com/assets'
});
```

---

## ✅ Verification Checklist

Before deployment, verify:

- [ ] `generated_assets/` directory exists
- [ ] `generated_assets/ascii/` has 52 .txt files
- [ ] `generated_assets/tables/` has 52 .html files
- [ ] `generated_assets/phase1_manifest.json` exists
- [ ] Backend asset loader initializes without errors
- [ ] `/api/assets/summary` returns 104 assets
- [ ] Frontend components render without console errors
- [ ] Truth table inputs are interactive

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `FileNotFoundError` | Check `generated_assets/` path is correct |
| `/api/assets/summary` returns 503 | Call `initialize_asset_loader()` in startup |
| Components not rendering | Verify lesson has `generated_assets` field |
| Table not interactive | Check JavaScript is enabled, CSS loaded |
| Slow loading | Assets are cached, clear browser cache if needed |

---

## 📁 File Structure

```
project/
├── generated_assets/              ← Asset files here
│   ├── ascii/
│   │   ├── lesson1.txt
│   │   ├── lesson2.txt
│   │   └── ...
│   ├── tables/
│   │   ├── lesson1.html
│   │   ├── lesson2.html
│   │   └── ...
│   └── phase1_manifest.json
│
├── src/
│   ├── backend/
│   │   ├── asset_loader.py        ← Asset loading
│   │   ├── api/
│   │   │   └── assets.py          ← REST routes
│   │   └── services/
│   │       └── lesson_enrichment.py← Enrichment
│   │
│   └── frontend/
│       ├── components/
│       │   ├── ASCIIDiagram.tsx
│       │   ├── TruthTable.tsx
│       │   └── LessonContent.tsx
│       └── hooks/
│           └── useGeneratedAssets.ts
└── docs/
    ├── PHASE1_INTEGRATION_GUIDE.md
    ├── PHASE1_COMPLETION_SUMMARY.md
    └── PHASE1_ARCHITECTURE.md
```

---

## 🚀 Next Steps

1. **Copy files** to your project
2. **Configure** backend initialization
3. **Test** API endpoints
4. **Deploy** with `generated_assets/` directory
5. **Monitor** for any issues

---

## 📞 Support

For detailed information, see:
- `PHASE1_INTEGRATION_GUIDE.md` - Complete setup guide
- `PHASE1_COMPLETION_SUMMARY.md` - Feature overview
- `PHASE1_ARCHITECTURE.md` - Technical architecture

All systems are production-ready! ✅

---

**Phase 1 Status: 🟢 COMPLETE**
**Ready for Phase 2: ✅ YES**
