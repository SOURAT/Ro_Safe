from flask import Blueprint, request, jsonify, send_file
from services.fine_calculator import calculate_fine
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from middleware.auth import require_auth
from services.jwt_service import is_admin
from db import history_collection
from models.history_model import history_model
from datetime import datetime
import io

fine_bp = Blueprint("fine", __name__)


@fine_bp.route("/calculate-fine", methods=["POST"])
def calculate():
    user = require_auth()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if not is_admin(user):
        return jsonify({"error": "Forbidden — admins only"}), 403

    data = request.get_json() or {}

    vehicle_type = data.get("vehicle_type")
    violation = data.get("violation")
    state = data.get("state")
    vehicle_number = data.get("vehicle_number")

    if not all([vehicle_type, violation, state, vehicle_number]):
        return jsonify({"error": "Missing fields"}), 400

    vehicle_number = vehicle_number.upper()
    violation_key = violation.lower().replace(" ", "_")

    previous_count = history_collection.count_documents({
        "vehicle_number": vehicle_number,
        "violation": violation
    })

    repeated = previous_count > 0

    result = calculate_fine(state, violation_key, repeated)

    if "error" in result:
        return jsonify(result), 404

    fine_text = (
        str(result["min_fine"])
        if result["min_fine"] == result["max_fine"]
        else f"{result['min_fine']} - {result['max_fine']}"
    )

    history_collection.insert_one(
        history_model(
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            violation=result["violation"],
            fine=fine_text,
            repeated=repeated,
            email=user.get("identity")
        )
    )

    return jsonify({
        "vehicle_number": vehicle_number,
        "vehicle_type": vehicle_type,
        "violation": result["violation"],
        "fine": fine_text,
        "repeated": repeated
    })


@fine_bp.route("/generate-receipt", methods=["POST"])
def generate_receipt():
    user = require_auth()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>DriveLegal Fine Receipt</b>", styles["Title"]))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Vehicle Number: {data.get('vehicle_number', '-')}", styles["Normal"]))
    content.append(Paragraph(f"Vehicle Type: {data.get('vehicle_type', '-')}", styles["Normal"]))
    content.append(Paragraph(f"Violation: {data.get('violation', '-')}", styles["Normal"]))
    content.append(Paragraph(f"Fine: ₹{data.get('fine', '-')}", styles["Normal"]))
    content.append(Paragraph(f"Repeated Offence: {data.get('repeated', '-')}", styles["Normal"]))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="receipt.pdf",
        mimetype="application/pdf"
    )
