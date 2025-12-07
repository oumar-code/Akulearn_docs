from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json
import pandas as pd
from typing import List, Optional
import csv
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "content" / "catalog.json"
MANUAL_REVIEW_CSV = ROOT / "content" / "manual_review.csv"
MAPPING_TEMPLATE_CSV = ROOT / "content" / "lo_mapping_template.csv"
AUTO_TAG_SUGGESTIONS_PATH = ROOT / "content" / "auto_tag_suggestions.json"
UI_HTML = ROOT / "mlops" / "ui" / "lo_mapper.html"

app = FastAPI(title="LO Mapper / Content Review API")

# Serve the UI HTML at /ui
@app.get("/ui")
def ui_index():
    if UI_HTML.exists():
        return FileResponse(UI_HTML)
    raise HTTPException(status_code=404, detail="UI not found")

# Mount static directory (if there are assets)
static_dir = ROOT / "mlops" / "ui"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ReviewItem(BaseModel):
    asset_path: str
    issue: str
    notes: Optional[str] = ""
    reviewer: Optional[str] = ""
    status: Optional[str] = "open"


@app.get("/catalog")
def get_catalog():
    if not CATALOG_PATH.exists():
        raise HTTPException(status_code=404, detail="Catalog not found")
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


@app.get("/manual_review")
def get_manual_review():
    if not MANUAL_REVIEW_CSV.exists():
        return {"items": []}
    df = pd.read_csv(MANUAL_REVIEW_CSV)
    return {"items": df.to_dict(orient='records')}


@app.post("/manual_review")
def add_manual_review(item: ReviewItem):
    rec = item.dict()
    df = pd.DataFrame([rec])
    if MANUAL_REVIEW_CSV.exists():
        df_old = pd.read_csv(MANUAL_REVIEW_CSV)
        df = pd.concat([df_old, df], ignore_index=True)
    df.to_csv(MANUAL_REVIEW_CSV, index=False)
    return {"status": "ok", "recorded": rec}


@app.get("/mapping_template")
def get_mapping_template():
    if not MAPPING_TEMPLATE_CSV.exists():
        # create a header if file does not exist so the UI can download
        with open(MAPPING_TEMPLATE_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['asset_path', 'lo_id', 'score', 'reviewer', 'created_at'])
    return FileResponse(MAPPING_TEMPLATE_CSV)


@app.get("/suggestions")
def get_suggestions():
    """Serve the auto-generated LO suggestions file dynamically."""
    if not AUTO_TAG_SUGGESTIONS_PATH.exists():
        return {"suggestions": [], "message": "No suggestions file generated yet. Run auto-tagging first."}
    try:
        with open(AUTO_TAG_SUGGESTIONS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading suggestions: {str(e)}")


@app.post("/apply_mapping")
def apply_mapping(payload: dict):
    # payload expected: {asset_path, lo_id, score, reviewer?}
    asset_path = payload.get('asset_path')
    lo_id = payload.get('lo_id')
    score = payload.get('score')
    reviewer = payload.get('reviewer', '')
    if not asset_path or not lo_id:
        raise HTTPException(status_code=400, detail='asset_path and lo_id required')

    # ensure mapping CSV exists with header
    header = ['asset_path', 'lo_id', 'score', 'reviewer', 'created_at']
    created = False
    if not MAPPING_TEMPLATE_CSV.exists():
        with open(MAPPING_TEMPLATE_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        created = True

    with open(MAPPING_TEMPLATE_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([asset_path, lo_id, score or '', reviewer, datetime.utcnow().isoformat() + 'Z'])

    return JSONResponse({"status": "ok", "asset_path": asset_path, "lo_id": lo_id, "created": created})


if __name__ == '__main__':
    # quick import test
    print('LO Mapper API module loaded')
