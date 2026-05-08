from flask import Flask, jsonify
from config import Config
from routes.temperature import temperature_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(temperature_bp)


# GET /api/health — check the API is running
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Brooder API is running"}), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
