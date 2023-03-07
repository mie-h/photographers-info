from app.read_json import photographers_data
import json


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body:
        response['body'] = json.dumps(body)
    return response


def get_photographer_dict(photographer):
    photographer_dict = {
        "id": photographer['id'],
        "first_name": photographer['first_name'],
        "last_name": photographer['last_name'],
        "username": photographer['username'],
        "phone_number": photographer['phone_number'],
        "avatar": photographer['avatar'],
        "event_type": photographer['event_type']['type'],
    }
    return photographer_dict


def find_photographer(id):
    for i, photographer in enumerate(photographers_data):
        if photographer['id'] == id:
            return get_photographer_dict(photographer) 
        

def _get_photographers_by_event_type_helper(event_type):
    data = []
    for photographer in photographers_data:
        if event_type in photographer['event_type']['type']:
            data.append(get_photographer_dict(photographer))
    return data