from flask import request
from services.jwt_service import verify_token

def require_auth():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]  
        return verify_token(token)
    except:
        return None
