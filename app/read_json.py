import json
import os

photographers_data = None
configfile_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "photographers.json"
)
with open(configfile_path, "r") as f:
    photographers_data = json.load(f)
