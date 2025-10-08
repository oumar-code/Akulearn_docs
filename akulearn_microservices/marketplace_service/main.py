"""
Marketplace Service
Handles item listing, buying, and Aku Coin transactions.
"""
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI(title="Akulearn Marketplace Service")

# Dummy data
items = [
    {"id": 1, "title": "Math Module", "price": 10},
    {"id": 2, "title": "Science Quiz", "price": 5}
]

@app.get("/items")
def get_items():
    return items

@app.post("/buy/{item_id}")
def buy_item(item_id: int):
    # Placeholder for Aku Coin transaction logic
    return {"message": f"Item {item_id} purchased. Aku Coin deducted."}
