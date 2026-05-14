from datetime import datetime


def user_model(name, email,carnumber,password):
    return {
        "name": name,
        "email": email,
        "car_number": carnumber,
        "password": password,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
