from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import json

app = FastAPI()

# Add the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Read items from values.txt file
with open("values.txt", "r") as f:
    items = [line.strip() for line in f.readlines()]


@app.get("/")
def read_root():
    return {"oieeeee": "World"}


@app.get("/items/")
def read_items():
    with open("values.txt", "r") as f:
        items = [json.loads(line) for line in f.readlines()]
    return {"items": items}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    # Read items from values.txt file
    with open("values.txt", "r") as f:
        items = [json.loads(line) for line in f.readlines()]
    
    # Find item with matching ID
    for item in items:
        if str(item.get("id")) == str(item_id):
            return item
    
    return {"message": "Item not found"}


@app.post("/items/")
async def create_item(request: Request):
    data = await request.json()
    
    # Generate and assign unique ID to item
    with open("values.txt", "r") as f:
        items = [json.loads(line) for line in f.readlines()]
    max_id = 0
    for item in items:
        if "id" in item and item["id"] > max_id:
            max_id = item["id"]
    data["id"] = max_id + 1
    
    # Check if there is an existing item with the same name and replace its values
    item_found = False
    new_items = []
    for item in items:
        if "chest" in data and "chest" in item:
            item["chest"] = data["chest"]
            item_found = True
        new_items.append(item)
    
    if not item_found:
        new_items.append(data)
    
    # Write updated items to values.txt file
    with open("values.txt", "w") as f:
        for item in new_items:
            f.write(json.dumps(item) + "\n")
    
    return {"data": data}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # Read items from values.txt file
    with open("values.txt", "r") as f:
        items = [json.loads(line) for line in f.readlines()]
    
    # Find and delete item with matching ID
    item_found = False
    new_items = []
    for item in items:
        if str(item.get("id")) == str(item_id):
            item_found = True
        else:
            new_items.append(item)
    
    # Write updated items to values.txt file
    with open("values.txt", "w") as f:
        for item in new_items:
            f.write(json.dumps(item) + "\n")
    
    if item_found:
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}
