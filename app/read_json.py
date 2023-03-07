import json
import os

PHOTOGRAPHERS_DATA = None
configfile_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "photographers.json"
)
with open(configfile_path, "r") as f:
    PHOTOGRAPHERS_DATA = json.load(f)
