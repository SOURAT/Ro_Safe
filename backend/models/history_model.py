from datetime import datetime


def history_model(vehicle_number, vehicle_type, violation, fine, repeated, email=None):
    return {
        "vehicle_number": vehicle_number,
        "vehicle_type": vehicle_type,
        "violation": violation,
        "fine": fine,
        "repeated": repeated,
        "email": email,
        "date": datetime.utcnow(),
        "status": "unpaid"
    }
