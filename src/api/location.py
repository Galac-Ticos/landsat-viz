from flask import request, jsonify
from flask.views import MethodView
from src.utils import get_locations, post_location, verify_token

class LocationView(MethodView):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                user_locations = get_locations(user_id)
                if user_locations:
                    return jsonify(user_locations), 200
                return jsonify({"error": "User not found"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                data = request.get_json()
                latitude = data.get('latitude')
                longitude = data.get('longitude')
                description = data.get('description')
                if not latitude or not longitude:
                    return jsonify({"error": "Location with latitude and longitude properties are required"}), 400
                user_location = post_location(user_id, latitude, longitude, description)
                if user_location:
                    return jsonify(user_location), 200
                return jsonify({"error": "Location not created"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401
