import json
import os

SESSION_FILE = ".session"

def save_session(mobile, user_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"mobile": mobile, "user_id": user_id}, f)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("mobile"), data.get("user_id")

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)