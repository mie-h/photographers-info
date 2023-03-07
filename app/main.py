from app.read_json import photographers_data
import app.utils as utils 
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.get("/api")
def get_api_root():
    body = {"message": "good"}
    return utils.build_response(200, body)


@app.get("/api/photographers")
def get_all_photographers():
    data = utils._get_all_photographers()
    return utils.build_response(200, data)


@app.get("/api/photographers/{photographerID}")
def get_photographer_by_id(photographerID: int):
    photographer_dict = utils.find_photographer(photographerID)
    if photographer_dict is None:
        raise HTTPException(status=404, detail=f"Photographer with id: {photographerID} not found")
    return utils.build_response(200, photographer_dict)


@app.get("/api/photographers/event/{eventType}")
def get_photographers_by_event_type(eventType: str):
    data = utils._get_photographers_by_event_type_helper(eventType)
    return utils.uild_response(200, data)