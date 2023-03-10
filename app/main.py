import app.utils as utils 
from fastapi import FastAPI
from app.models import Photographer


app = FastAPI()


@app.get("/api")
def get_api_root():
    body = {"message": "good"}
    return utils.build_response(200, body)


@app.get("/api/photographers")
def get_all_photographers():
    return utils.get_all_photographers()


@app.get("/api/photographers/{photographerID}")
def get_photographer_by_id(photographerID: int):
    return utils.get_photographer_by_id(photographerID)


@app.get("/api/photographers/events/{eventType}")
def get_photographers_by_event_type(eventType: str):
    return utils.get_photographers_by_event_type(eventType)


@app.post("/api/photographers")
def save_photographer(photographer: Photographer):
    return utils.save_photographer(photographer)


@app.patch("/api/photographers")
def update_photographer(id: int, key: str, value: str, value_type: str):
    return utils.update_photographer(id, key, value, value_type)


@app.delete("/api/photographers")
def delete_photographer(id: int):
    return utils.delete_photographer(id)