import bcrypt
import uuid
import re
from datetime import datetime
from .database import load_data, save_data

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(username, email, password):
    users = load_data("users.json")
    
    for user_id, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get("username") == username:
            return False, "Username already exists"
        if isinstance(user_data, dict) and user_data.get("email") == email:
            return False, "Email already registered"
    
    new_user = {
        "id": str(uuid.uuid4()),
        "username": username,
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "verified": True,
        "premium": False,
        "voice_profiles": [],
        "call_history": [],
        "favorites": [],
        "assistants": [],
        "settings": {
            "input_device": "Default",
            "output_device": "Default",
            "volume": 80,
        }
    }
    
    users[new_user["id"]] = new_user
    save_data(users, "users.json")
    
    return True, "Registration successful! You can now log in."

def authenticate_user(username, password):
    users = load_data("users.json")
    
    for user_id, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get("username") == username:
            if verify_password(password, user_data.get("password", "")):
                user_data["last_login"] = datetime.now().isoformat()
                users[user_id] = user_data
                save_data(users, "users.json")
                return True, user_data
            else:
                return False, "Invalid password"
    
    return False, "User not found"