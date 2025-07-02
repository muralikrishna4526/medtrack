import json
import os

DATA_FILE = 'users.json'

def load_users():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        return [{"username": k, **v} for k, v in data.items()]
