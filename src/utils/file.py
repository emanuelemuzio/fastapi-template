import json
import os
from ..exceptions import JsonNotFoundException
from dotenv import load_dotenv

load_dotenv()

def load_json(filename : str, path : str) -> dict:
    full_path = os.path.join(path, filename)
    if not os.path.exists(full_path):
        raise JsonNotFoundException(filename)
    with open(path, 'r') as file:
        data = json.load(file)
        return data
    
def from_env(key : str) -> str | None:
    return os.getenv(key)