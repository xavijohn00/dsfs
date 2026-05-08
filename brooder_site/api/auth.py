from functools import wraps
from flask import request, jsonify
from db import get_db

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        api_key = auth_header.split("Bearer ")[1].strip()

        if not api_key:
            return jsonify({"error": "API key is required"}), 401

        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT brooder_id FROM brooders WHERE api_key = %s AND status = 'active'",
            (api_key,)
        )
        brooder = cursor.fetchone()
        cursor.close()
        conn.close()

        if not brooder:
            return jsonify({"error": "Invalid API key"}), 403

        request.brooder_id = brooder["brooder_id"]
        return f(*args, **kwargs)

    return decorated
