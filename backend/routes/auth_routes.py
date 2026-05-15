from flask import Blueprint, request, jsonify
from services.auth_service import authenticate_admin, authenticate_user, register_user
from services.jwt_service import generate_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json() or {}

    key = data.get("key")
    password = data.get("password")

    if not key or not password:
        return jsonify({"error": "Missing credentials"}), 400

    if not authenticate_admin(key, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(key, role="admin")

    return jsonify({
        "message": "Admin login successful",
        "token": token
    })


@auth_bp.route("/user-login", methods=["POST"])
def user_login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    result = authenticate_user(email, password)

    if not result:
        return jsonify({"error": "Invalid credentials"}), 401

    user_id, user_email = result
    token = generate_token(user_email, role="user")

    return jsonify({
        "message": "Login successful",
        "token": token
    })


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    name      = data.get("name")
    email     = data.get("email")
    carnumber = data.get("carnumber")  # ✅ ADDED
    password  = data.get("password")

    if not name or not email or not carnumber or not password:  # ✅ ADDED carnumber check
        return jsonify({"error": "Missing fields"}), 400

    result = register_user(name, email, carnumber, password)  # ✅ ADDED carnumber

    if "error" in result:
        return jsonify(result), 409

    return jsonify({
        "message": "Account created successfully"
    }), 201