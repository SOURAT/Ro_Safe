from db import admins_collection, users_collection
from models.user_model import user_model
from werkzeug.security import check_password_hash, generate_password_hash



def authenticate_admin(key, password):
    admin = admins_collection.find_one({"key": key})

    if not admin:
        return False

    return check_password_hash(admin["password"], password)



def register_user(name, email,carnumber,password):
    existing = users_collection.find_one({"email": email})

    if existing:
        return {"error": "Email already registered"}

    hashed = generate_password_hash(password)

    users_collection.insert_one(user_model(name, email,carnumber,hashed))

    return {"success": True}


def authenticate_user(email, password):
    user = users_collection.find_one({"email": email})

    if not user:
        return None

    if not check_password_hash(user["password"], password):
        return None

    return str(user["_id"]), user["email"]
