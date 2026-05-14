import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "state_rules")


def format_state(state):
    return state.lower().replace(" ", "_")


def load_state_data(state):
    file_path = os.path.join(DATA_PATH, f"{format_state(state)}.json")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_fine(state, violation_key, repeated=False):
    data = load_state_data(state)

    if not data:
        return {"error": "State data not found"}

    for district in data:
        for city in data[district]:
            for road in data[district][city]:
                rules = data[district][city][road]

                if violation_key in rules:
                    rule = rules[violation_key]
                    fine = rule["fine"]

                    if isinstance(fine, dict):
                        min_fine = fine.get("min", 0)
                        max_fine = fine.get("max", 0)
                    else:
                        min_fine = max_fine = fine

                    if repeated:
                        min_fine *= 2
                        max_fine *= 2

                    return {
                        "violation": rule["description"],
                        "min_fine": min_fine,
                        "max_fine": max_fine
                    }

    return {"error": "Violation not found"}
