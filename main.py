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
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(request: Request):
    data = await request.json()
    
    # Check if there is a repeated "chest" value in values.txt file
    if "chest" in data:
        with open("values.txt", "r") as f:
            items = [json.loads(line) for line in f.readlines()]
        chest_count = 0
        for item in items:
            for key in item.keys():
                if key.startswith("chest"):
                    chest_count += 1
        data["chest" + str(chest_count + 1)] = data.pop("chest")
    
    # Write item to values.txt file
    with open("values.txt", "a") as f:
        f.write(json.dumps(data) + "\n")
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
