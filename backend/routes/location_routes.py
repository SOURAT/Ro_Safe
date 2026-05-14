#location_routes.py

from flask import Blueprint, request, jsonify
from services.location_service import get_location_details
from middleware.auth import require_auth

location_bp = Blueprint("location", __name__)


@location_bp.route("/", methods=["POST"])
def location():
    user = require_auth()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat is None or lon is None:
        return jsonify({"error": "Missing latitude or longitude"}), 400

    result = get_location_details(lat, lon)

    if "error" in result:
        return jsonify(result), 500

    return jsonify(result), 200
