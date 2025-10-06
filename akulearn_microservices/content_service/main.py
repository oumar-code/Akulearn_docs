from fastapi import Query

# Advanced search endpoint
@app.get("/search")
def search_content(q: str = Query(..., description="Search query")):
    results = []
    # Search textbooks
    for tb in textbooks_db:
        if q.lower() in tb.title.lower():
            results.append({"type": "textbook", "title": tb.title, "version": tb.format})
    # Search journals
    for j in journals_db:
        if q.lower() in j.title.lower():
            results.append({"type": "journal", "title": j.title, "issue": j.issue})
    # Search conference papers
    for cp in conference_papers_db:
        if q.lower() in cp.title.lower():
            results.append({"type": "conference_paper", "title": cp.title, "year": cp.year})
    # Search datasets
    for ds in datasets_db:
        if q.lower() in ds.title.lower():
            results.append({"type": "dataset", "title": ds.title, "format": ds.format})
    # Search code
    for c in code_db:
        if q.lower() in c.title.lower():
            results.append({"type": "code", "title": c.title, "language": c.language})
    # Search AR assets
    for ar in ar_assets_db:
        if q.lower() in ar.title.lower():
            results.append({"type": "ar_asset", "title": ar.title, "format": ar.format})
    # Search simulations
    for sim in simulations_db:
        if q.lower() in sim.title.lower():
            results.append({"type": "simulation", "title": sim.title})
    # Search VR experiences
    for vr in vr_experiences_db:
        if q.lower() in vr.title.lower():
            results.append({"type": "vr_experience", "title": vr.title})
    return results
class Journal(BaseModel):
    id: int
    title: str
    issue: str
    path: str
    metadata: str = ""

journals_db: List[Journal] = []

@app.post("/journals/add")
def add_journal(journal: Journal):
    journals_db.append(journal)
    return {"message": "Journal added", "journal": journal}

@app.get("/journals/list")
def list_journals():
    return journals_db

class ConferencePaper(BaseModel):
    id: int
    title: str
    year: str
    path: str
    metadata: str = ""

conference_papers_db: List[ConferencePaper] = []

@app.post("/conference_papers/add")
def add_conference_paper(paper: ConferencePaper):
    conference_papers_db.append(paper)
    return {"message": "Conference paper added", "paper": paper}

@app.get("/conference_papers/list")
def list_conference_papers():
    return conference_papers_db

class Dataset(BaseModel):
    id: int
    title: str
    format: str
    path: str
    metadata: str = ""

datasets_db: List[Dataset] = []

@app.post("/datasets/add")
def add_dataset(dataset: Dataset):
    datasets_db.append(dataset)
    return {"message": "Dataset added", "dataset": dataset}

@app.get("/datasets/list")
def list_datasets():
    return datasets_db

class CodeSnippet(BaseModel):
    id: int
    title: str
    language: str
    path: str
    metadata: str = ""

code_db: List[CodeSnippet] = []

@app.post("/code/add")
def add_code(code: CodeSnippet):
    code_db.append(code)
    return {"message": "Code added", "code": code}

@app.get("/code/list")
def list_code():
    return code_db
# Endpoints for creative tools
@app.post("/tools/add")
def add_tool(tool: Tool):
    tools_db.append(tool)
    return {"message": "Tool added", "tool": tool}

@app.get("/tools/list")
def list_tools():
    return tools_db
class VRExperience(BaseModel):
    id: int
    title: str
    description: str
    path: str  # unitypackage or other format

vr_experiences_db: List[VRExperience] = []

@app.post("/vr_experiences/add")
def add_vr_experience(exp: VRExperience):
    vr_experiences_db.append(exp)
    return {"message": "VR experience added", "experience": exp}

@app.get("/vr_experiences/list")
def list_vr_experiences():
    return vr_experiences_db
class Simulation(BaseModel):
    id: int
    title: str
    description: str
    path: str  # html/js or other format

simulations_db: List[Simulation] = []

@app.post("/simulations/add")
def add_simulation(sim: Simulation):
    simulations_db.append(sim)
    return {"message": "Simulation added", "simulation": sim}

@app.get("/simulations/list")
def list_simulations():
    return simulations_db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Content Service")


# Content models for each format
class Textbook(BaseModel):
    id: int
    title: str
    format: str  # pdf, epub
    path: str

class Module(BaseModel):
    id: int
    title: str
    format: str  # scorm, xapi
    path: str

class Quiz(BaseModel):
    id: int
    title: str
    path: str  # html/js file

class Video(BaseModel):
    id: int
    title: str
    path: str  # mp4 file

class ARAsset(BaseModel):
    id: int
    title: str
    format: str  # glb, obj, fbx, usdz
    path: str
    description: str = ""
    thumbnail: str = ""

class Game(BaseModel):
    id: int
    title: str
    path: str  # html/js file

class FlashcardSet(BaseModel):
    id: int
    title: str
    path: str  # json/csv file

class LocalizedContent(BaseModel):
    id: int
    title: str
    path: str

class Encyclopedia(BaseModel):
    id: int
    title: str
    path: str  # zim file

class Tool(BaseModel):
    id: int
    title: str
    path: str

# In-memory DBs
textbooks_db: List[Textbook] = []
modules_db: List[Module] = []
quizzes_db: List[Quiz] = []
videos_db: List[Video] = []
ar_assets_db: List[ARAsset] = []
games_db: List[Game] = []
flashcards_db: List[FlashcardSet] = []
localized_db: List[LocalizedContent] = []
encyclopedia_db: List[Encyclopedia] = []
tools_db: List[Tool] = []

# Endpoints for each format
@app.post("/textbooks/add")
def add_textbook(textbook: Textbook):
    textbooks_db.append(textbook)
    return {"message": "Textbook added", "textbook": textbook}

@app.get("/textbooks/list")
def list_textbooks():
    return textbooks_db

@app.post("/modules/add")
def add_module(module: Module):
    modules_db.append(module)
    return {"message": "Module added", "module": module}

@app.get("/modules/list")
def list_modules():
    return modules_db

@app.post("/quizzes/add")
def add_quiz(quiz: Quiz):
    quizzes_db.append(quiz)
    return {"message": "Quiz added", "quiz": quiz}

@app.get("/quizzes/list")
def list_quizzes():
    return quizzes_db

@app.post("/videos/add")
def add_video(video: Video):
    videos_db.append(video)
    return {"message": "Video added", "video": video}

@app.get("/videos/list")
def list_videos():
    return videos_db

@app.post("/ar_assets/add")
def add_ar_asset(asset: ARAsset):
    ar_assets_db.append(asset)
    return {"message": "AR asset added", "asset": asset}

@app.get("/ar_assets/list")
def list_ar_assets():
    return ar_assets_db

@app.get("/ar_assets/{asset_id}")
def get_ar_asset(asset_id: int):
    for asset in ar_assets_db:
        if asset.id == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="AR asset not found")

@app.post("/games/add")
def add_game(game: Game):
    games_db.append(game)
    return {"message": "Game added", "game": game}

@app.get("/games/list")
def list_games():
    return games_db

@app.post("/flashcards/add")
def add_flashcard_set(flashcard: FlashcardSet):
    flashcards_db.append(flashcard)
    return {"message": "Flashcard set added", "flashcard": flashcard}

@app.get("/flashcards/list")
def list_flashcards():
    return flashcards_db

@app.post("/localized/add")
def add_localized(content: LocalizedContent):
    localized_db.append(content)
    return {"message": "Localized content added", "content": content}

@app.get("/localized/list")
def list_localized():
    return localized_db

@app.post("/encyclopedia/add")
def add_encyclopedia(entry: Encyclopedia):
    encyclopedia_db.append(entry)
    return {"message": "Encyclopedia added", "entry": entry}

@app.get("/encyclopedia/list")
def list_encyclopedia():
    return encyclopedia_db

@app.post("/tools/add")
def add_tool(tool: Tool):
    tools_db.append(tool)
    return {"message": "Tool added", "tool": tool}

@app.get("/tools/list")
def list_tools():
    return tools_db
