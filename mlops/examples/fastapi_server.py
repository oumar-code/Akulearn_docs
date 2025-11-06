from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Aku MLOps Demo - Summarization")


class TextIn(BaseModel):
    text: str


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.post("/summarize")
def summarize(payload: TextIn):
    # NOTE: In a real deployment, the model would be loaded on startup and served
    # by a dedicated process. This minimal example uses Hugging Face transformers
    # pipeline for demonstration and will download the model on first run.
    try:
        from transformers import pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"transformers import failed: {e}")

    summarizer = pipeline("summarization")
    res = summarizer(payload.text, max_length=130, min_length=30, do_sample=False)
    return {"summary": res[0]["summary_text"]}
