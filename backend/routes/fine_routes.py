from flask import Blueprint, request, jsonify, make_response
from services.fine_calculator import calculate_fine
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from middleware.auth import require_auth
from services.jwt_service import is_admin
from db import history_collection, users_collection
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

    vehicle_type   = data.get("vehicle_type")
    violation      = data.get("violation")
    state          = data.get("state")
    vehicle_number = data.get("vehicle_number")

    if not all([vehicle_type, violation, state, vehicle_number]):
        return jsonify({"error": "Missing fields"}), 400

    vehicle_number = vehicle_number.upper()
    violation_key  = violation

   
    owner = users_collection.find_one(
        {"car_number": vehicle_number},
        {"_id": 0, "email": 1}
    )
    owner_email = owner["email"] if owner else None

    if not owner_email:
        return jsonify({"error": "Vehicle number not registered in the system"}), 404

    
    result = calculate_fine(state, violation_key, repeated=False)

    if "error" in result:
        return jsonify(result), 404

    
    previous_count = history_collection.count_documents({
        "vehicle_number": vehicle_number,
        "violation":      result["violation"]
    })

    repeated = previous_count > 0

    
    result = calculate_fine(state, violation_key, repeated)

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
            email=owner_email
        )
    )

    return jsonify({
        "vehicle_number": vehicle_number,
        "vehicle_type":   vehicle_type,
        "violation":      result["violation"],
        "fine":           fine_text,
        "repeated":       repeated
    })


@fine_bp.route("/generate-receipt", methods=["POST", "OPTIONS"])
def generate_receipt():
    # ✅ Handle CORS preflight
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"]  = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response, 200

    user = require_auth()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50, leftMargin=50,
        topMargin=50,   bottomMargin=50
    )

    styles = getSampleStyleSheet()

   
    title_style = ParagraphStyle(
        "CustomTitle",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=colors.HexColor("#1a1a2e"),
        alignment=1,
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.HexColor("#444444"),
        alignment=1,
        spaceBefore=8,
        spaceAfter=10
    )
    label_style = ParagraphStyle(
        "Label",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.HexColor("#1a1a2e"),
    )
    value_style = ParagraphStyle(
        "Value",
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.HexColor("#333333"),
    )
    footer_style = ParagraphStyle(
        "Footer",
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=colors.HexColor("#888888"),
        alignment=1,
        spaceBefore=10
    )
    warning_style = ParagraphStyle(
        "Warning",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=colors.HexColor("#cc0000"),
        alignment=1,
        spaceBefore=6
    )
    section_style = ParagraphStyle(
        "SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=4,
        spaceAfter=8
    )

    content = []

    
    content.append(Paragraph("DriveLegal", title_style))
    content.append(Spacer(1, 6))
    content.append(Paragraph("Official Traffic Violation Fine Receipt", subtitle_style))
    content.append(Spacer(1, 10))
    content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
    content.append(Spacer(1, 14))

    
    receipt_no = f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    issue_date = datetime.now().strftime("%d %B %Y")

    info_data = [[
        Paragraph("Receipt No:", label_style),
        Paragraph(receipt_no,    value_style),
        Paragraph("Issue Date:", label_style),
        Paragraph(issue_date,    value_style)
    ]]

    info_table = Table(info_data, colWidths=[90, 160, 80, 160])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#f0f4ff")),
        ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    content.append(info_table)
    content.append(Spacer(1, 16))

    
    content.append(Paragraph("Vehicle & Violation Details", section_style))

   
    repeated     = data.get("repeated", False)
    repeated_str = "YES" if repeated else "No"
    fine_color   = colors.HexColor("#cc0000") if repeated else colors.HexColor("#333333")

    details_data = [
        ["Field",            "Details"                        ],
        ["Vehicle Number",   data.get("vehicle_number", "-")  ],
        ["Vehicle Type",     data.get("vehicle_type",   "-")  ],
        ["Violation",        data.get("violation",      "-")  ],
        ["Fine Amount",      f"Rs. {data.get('fine',    '-')}"],
        ["Repeated Offence", repeated_str                     ],
        ["Date of Issue",    issue_date                       ],
        ["Status",           "UNPAID"                         ],
    ]

    details_table = Table(details_data, colWidths=[180, 310])
    details_table.setStyle(TableStyle([
        
        ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 12),
        ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

       
        ("FONTNAME",      (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",      (1, 1), (1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 11),
        ("TOPPADDING",    (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),

        
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.HexColor("#ffffff"),
            colors.HexColor("#f7f9ff")
        ]),

        
        ("TEXTCOLOR",  (1, 4), (1, 4), colors.HexColor("#cc0000")),
        ("FONTNAME",   (1, 4), (1, 4), "Helvetica-Bold"),

        
        ("TEXTCOLOR",  (1, 7), (1, 7), colors.HexColor("#cc0000")),
        ("FONTNAME",   (1, 7), (1, 7), "Helvetica-Bold"),

       
        ("TEXTCOLOR",  (1, 5), (1, 5), fine_color),
        ("FONTNAME",   (1, 5), (1, 5), "Helvetica-Bold"),

        
        ("BOX",        (0, 0), (-1, -1), 1,   colors.HexColor("#1a1a2e")),
        ("INNERGRID",  (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
    ]))

    content.append(details_table)
    content.append(Spacer(1, 20))

    
    vehicle_number_receipt = data.get("vehicle_number", "")
    violation_receipt      = data.get("violation", "")

    offence_count = history_collection.count_documents({
        "vehicle_number": vehicle_number_receipt,
        "violation":      violation_receipt
    }) if vehicle_number_receipt and violation_receipt else 0

    
    if repeated:
        content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cc0000")))

        if offence_count >= 3:
            content.append(Paragraph(
                "WARNING: 3rd or more offence detected — Fine has been doubled. "
                "Driving licence suspension recommended as per MV Act Section 206.",
                warning_style
            ))
        else:
            content.append(Paragraph(
                "WARNING: This is a repeated offence. "
                "Fine has been doubled as per traffic rules.",
                warning_style
            ))

        content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cc0000")))
        content.append(Spacer(1, 12))

   
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    content.append(Paragraph(
        "This is a computer-generated receipt and does not require a signature.",
        footer_style
    ))
    content.append(Paragraph(
        "DriveLegal | Drive Safe, Stay Legal | 2026",
        footer_style
    ))

    doc.build(content)
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers["Content-Type"]                 = "application/pdf"
    response.headers["Content-Disposition"]          = "attachment; filename=receipt.pdf"
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response