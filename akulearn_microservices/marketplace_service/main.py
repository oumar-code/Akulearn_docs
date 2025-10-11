"""
Aku Platform Marketplace Service
Handles item listing, buying, and Aku Coin transactions.
"""
from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI(title="Aku Platform Marketplace Service")

# Dummy data
items: List[Dict] = [
    {"id": 1, "title": "Math Module", "price": 10},
    {"id": 2, "title": "Science Quiz", "price": 5}
]
user_aku_coins: Dict[str, int] = {"user1": 100, "user2": 50}

@app.get("/items")
def get_items():
    return items

@app.post("/buy/{item_id}")
def buy_item(item_id: int, user_id: str):
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if user_aku_coins.get(user_id, 0) < item["price"]:
        raise HTTPException(status_code=400, detail="Insufficient Aku Coin balance")
    user_aku_coins[user_id] -= item["price"]
    return {"message": f"Item {item_id} purchased. Aku Coin deducted.", "balance": user_aku_coins[user_id]}
