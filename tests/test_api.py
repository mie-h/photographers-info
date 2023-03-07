

from app.read_json import PHOTOGRAPHERS_DATA
from app.utils import _get_photographers_by_event_type_helper
import requests
import pytest
import ast


base_url = "http://127.0.0.1:8000"
# base_url = "http://0.0.0.0:80"


def test_get_api_root():
    url = base_url + "/api"
    response = requests.get(url)
    assert response.status_code == 200


def test_get_all_photographers():
    url = base_url + "/api/photographers"
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()
    lst = ast.literal_eval(data['body'])
    assert len(lst) == len(PHOTOGRAPHERS_DATA)


@pytest.mark.parametrize(("id", "photographer"), [(photographer["id"], photographer) for photographer in PHOTOGRAPHERS_DATA])
def test_get_photographer_by_id(id, photographer):
    print(id, photographer)
    url = base_url + f"/api/photographers/{id}"
    print(url)
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()
    data = ast.literal_eval(data['body'])
    assert data['id'] == photographer['id']
    assert data['username'] == photographer['username']
    assert data['avatar'] == photographer['avatar']


@pytest.mark.parametrize("event_type", ["wedding", "bridal showers", "food","sports"])
def test_get_photographers_by_event_type(event_type):
    url = base_url + f"/api/photographers/event/{event_type}"
    print(url)
    response = requests.get(url)
    assert response.status_code == 200

    data = response.json()
    lst = ast.literal_eval(data['body'])
    assert len(lst) == len(_get_photographers_by_event_type_helper(event_type))

