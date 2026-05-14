from werkzeug.security import generate_password_hash
from db import admins_collection

admins = [
    {"key": "Rahul_Das", "password": "das123"},
    {"key": "Ayoshree_Dutta", "password": "dutta123"},
    {"key": "Nabarka_Mazumdar", "password": "nba123"},
    {"key": "Subhadip_Bhunia", "password": "bhu123"},
    {"key": "Riddhismita_Nath", "password": "smita123"},
    {"key": "Souradeep_Tarafdar", "password": "soura123"},
]

for admin in admins:

    existing = admins_collection.find_one({"key": admin["key"]})

    if existing:
        print(f"Already exists — skipping: {admin['key']}")
        continue

    admins_collection.insert_one({
        "key": admin["key"],
        "password": generate_password_hash(admin["password"])
    })
    print(f"Inserted: {admin['key']}")

print("Done!")
