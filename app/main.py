from app.read_json import photographers_data
from app.utils import find_photographer, get_photographer_dict, build_response, _get_photographers_by_event_type_helper
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.get("/api")
def get_api_root():
    body = {"message": "good"}
    return build_response(200, body)


@app.get("/api/photographers")
def get_all_photographers():
    data = []
    for photographer in photographers_data:
        data.append(get_photographer_dict(photographer))
    return build_response(200, data)


@app.get("/api/photographers/{photographerID}")
def get_photographer_by_id(photographerID: int):
    photographer_dict = find_photographer(photographerID)
    if photographer_dict is None:
        raise HTTPException(status=404, detail=f"Photographer with id: {photographerID} not found")
    return build_response(200, photographer_dict)


@app.get("/api/photographers/event/{eventType}")
def get_photographers_by_event_type(eventType: str):
    data = _get_photographers_by_event_type_helper(eventType)
    return build_response(200, data)