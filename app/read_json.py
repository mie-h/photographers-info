import json
import os
from decimal import Decimal
from app.db import PHOTOGRAPHERS_INFO_TABLE


PHOTOGRAPHERS_DATA = None
configfile_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "photographers.json"
)
with open(configfile_path, "r") as f:
    PHOTOGRAPHERS_DATA = json.load(f)


for photographer in PHOTOGRAPHERS_DATA:
        try:
                photographer = json.loads(json.dumps(photographer), parse_float=Decimal)
                PHOTOGRAPHERS_INFO_TABLE.put_item(Item=photographer)
        except Exception as e:
                print(f"Error message: {e}")

