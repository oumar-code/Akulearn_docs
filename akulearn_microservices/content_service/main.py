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
