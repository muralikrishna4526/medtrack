import json
import os

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password, role):
    users = load_users()
    users[username] = {'password': password, 'role': role}
    save_users(users)

def validate_login(username, password):
    users = load_users()
    user = users.get(username)
    if user and user['password'] == password:
        return user['role']
    return None
