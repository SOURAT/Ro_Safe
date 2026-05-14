#jwt_service.py

import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET")
EXP_MIN = int(os.getenv("JWT_EXPIRE_MIN", 60))


def generate_token(identity, role="user"):
    payload = {
        "identity": identity,  
        "role": role,          
        "exp": datetime.utcnow() + timedelta(minutes=EXP_MIN)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def is_admin(token_data):
    return token_data.get("role") == "admin"


def is_user(token_data):
    return token_data.get("role") == "user"
