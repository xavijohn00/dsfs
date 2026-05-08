from flask import Blueprint, request, jsonify
from db import get_db
from auth import require_api_key

temperature_bp = Blueprint("temperature", __name__)


# POST /api/readings — RPi pushes a temperature + humidity reading
# Body: { "temperature": 32.5, "humidity": 58.0 }
@temperature_bp.route("/api/readings", methods=["POST"])
@require_api_key
def post_reading():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    temperature = data.get("temperature")
    humidity    = data.get("humidity")

    if temperature is None:
        return jsonify({"error": "temperature is required"}), 400

    try:
        temperature = float(temperature)
    except (ValueError, TypeError):
        return jsonify({"error": "temperature must be a number"}), 400

    if humidity is not None:
        try:
            humidity = float(humidity)
        except (ValueError, TypeError):
            return jsonify({"error": "humidity must be a number"}), 400

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO temperature_readings (brooder_id, temperature, humidity) VALUES (%s, %s, %s)",
        (request.brooder_id, temperature, humidity)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Reading saved", "brooder_id": request.brooder_id}), 201


# GET /api/readings — get the latest reading for this brooder
@temperature_bp.route("/api/readings", methods=["GET"])
@require_api_key
def get_reading():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT temperature, humidity, recorded_at
        FROM temperature_readings
        WHERE brooder_id = %s
        ORDER BY recorded_at DESC
        LIMIT 1
        """,
        (request.brooder_id,)
    )
    reading = cursor.fetchone()
    cursor.close()
    conn.close()

    if not reading:
        return jsonify({"message": "No readings yet"}), 404

    reading["recorded_at"] = str(reading["recorded_at"])
    return jsonify(reading), 200


# GET /api/settings — RPi polls for the current target temperature
@temperature_bp.route("/api/settings", methods=["GET"])
@require_api_key
def get_settings():
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT target_temp, set_at
        FROM temperature_settings
        WHERE brooder_id = %s
        ORDER BY set_at DESC
        LIMIT 1
        """,
        (request.brooder_id,)
    )
    setting = cursor.fetchone()
    cursor.close()
    conn.close()

    if not setting:
        return jsonify({"message": "No target temperature set yet"}), 404

    setting["set_at"] = str(setting["set_at"])
    return jsonify(setting), 200


# POST /api/settings — PHP calls this when a student sets a new target temp
# Body: { "target_temp": 32.5, "student_id": 3 }
@temperature_bp.route("/api/settings", methods=["POST"])
@require_api_key
def post_settings():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    target_temp = data.get("target_temp")
    student_id  = data.get("student_id")

    if target_temp is None or student_id is None:
        return jsonify({"error": "target_temp and student_id are required"}), 400

    try:
        target_temp = float(target_temp)
        student_id  = int(student_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO temperature_settings (brooder_id, student_id, target_temp) VALUES (%s, %s, %s)",
        (request.brooder_id, student_id, target_temp)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Target temperature saved", "target_temp": target_temp}), 201
