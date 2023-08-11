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
    # Write item to values.txt file
    with open("values.txt", "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"data": data}
