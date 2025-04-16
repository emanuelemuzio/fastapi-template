import json
import os
from ..exceptions import JsonNotFoundException

def load_json(filename : str, path : str) -> dict:
    full_path = os.path.join(path, filename)
    if not os.path.exists(full_path):
        raise JsonNotFoundException(filename)
    with open(path, 'r') as file:
        data = json.load(file)
        return data