import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "state_rules")


def format_state_name(state):
    return state.lower().replace(" ", "_")


def load_state_data(state):
    file_path = os.path.join(DATA_PATH, f"{format_state_name(state)}.json")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_rules(state, district=None, city=None, road=None):
    data = load_state_data(state)

    if not data:
        return {"error": "State not found"}

    if district and city and road:
        try:
            return {
                "level": "road",
                "rules": data[district][city][road]
            }
        except KeyError:
            pass

    if district and city:
        try:
            city_data = data[district][city]
            combined = {}

            for road_name in city_data:
                for violation, rule in city_data[road_name].items():
                    combined[violation] = rule

            return {
                "level": "city",
                "rules": combined
            }
        except KeyError:
            pass

    if district:
        try:
            district_data = data[district]
            combined = {}

            for city_name in district_data:
                for road_name in district_data[city_name]:
                    for violation, rule in district_data[city_name][road_name].items():
                        combined[violation] = rule

            return {
                "level": "district",
                "rules": combined
            }
        except KeyError:
            pass

    combined = {}

    for district_name in data:
        for city_name in data[district_name]:
            for road_name in data[district_name][city_name]:
                for violation, rule in data[district_name][city_name][road_name].items():
                    combined[violation] = rule

    return {
        "level": "state",
        "rules": combined
    }
