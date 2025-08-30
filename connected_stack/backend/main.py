from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Placeholder for LLM integration
def query_llm(input_data):
    # TODO: Integrate with cloud LLM API
    return {"result": "LLM response"}

@app.post("/api/coach")
def coach(data: dict):
    return query_llm(data)

# Placeholder for cloud database
@app.get("/api/students")
def get_students():
    # TODO: Connect to PostgreSQL or MongoDB
    return {"students": []}
