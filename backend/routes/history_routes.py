#history_routes.py

from flask import Blueprint, request, jsonify
from db import history_collection
from middleware.auth import require_auth
from services.jwt_service import is_admin
from datetime import datetime

history_bp = Blueprint("history", __name__)



@history_bp.route("/fine-history", methods=["GET"])
def get_history():
    user = require_auth()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if not is_admin(user):
        return jsonify({"error": "Forbidden — admins only"}), 403

    vehicle = request.args.get("vehicle", "").upper()
    limit = int(request.args.get("limit", 10))

    if not vehicle:
        return jsonify({"error": "Vehicle number required"}), 400

    records = list(
        history_collection
        .find({"vehicle_number": vehicle}, {"_id": 0})
        .sort("date", -1)
        .limit(limit)
    )

    return jsonify({
        "vehicle": vehicle,
        "count": len(records),
        "records": records
    })



@history_bp.route("/my-history", methods=["GET"])
def get_my_history():
    user = require_auth()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if not is_admin(user):
        email = user.get("identity")
        records = list(
            history_collection
            .find({"email": email}, {"_id": 0})
            .sort("date", -1)
        )

        return jsonify({
            "email": email,
            "count": len(records),
            "records": records
        })

    return jsonify({"error": "Users only"}), 403
