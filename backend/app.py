from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from routes.location_routes import location_bp
from routes.rules_routes import rules_bp
from routes.fine_routes import fine_bp
from routes.auth_routes import auth_bp
from routes.history_routes import history_bp

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(location_bp, url_prefix="/location")
app.register_blueprint(rules_bp, url_prefix="/rules")
app.register_blueprint(fine_bp, url_prefix="/fine")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(history_bp, url_prefix="/history")

@app.route('/')
def health_check():
    return {"status": "Drive Legal API is running"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
