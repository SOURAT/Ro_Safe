#rules_routes.py

from flask import Blueprint, request, jsonify
from services.rule_engine import get_rules
from middleware.auth import require_auth

rules_bp = Blueprint("rules", __name__)


@rules_bp.route("/", methods=["GET"])
def rules():
    user = require_auth()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    state = request.args.get("state")
    district = request.args.get("district")
    city = request.args.get("city")
    road = request.args.get("road")

    if not state:
        return jsonify({"error": "State is required"}), 400

    result = get_rules(state, district, city, road)

    return jsonify(result)
