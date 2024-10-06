from flask import request, jsonify
from flask.views import MethodView
from src.utils import get_user, post_user, put_user, verify_token

class UserView(MethodView):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                user_data = get_user(user_id)
                if user_data:
                    return jsonify(user_data), 200
                else:
                    return jsonify({"error": "User does not exist"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401

    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        user_data = post_user(email, password)
        if user_data:
            return jsonify(user_data), 200
        return jsonify({"error": "User not created"}), 404
    
    def put(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                data = request.get_json()
                email = data.get('email') 
                password = data.get('password')
                threshold = data.get('threshold')
                user_data = put_user(user_id, email, password, threshold)
                if user_data:
                    return jsonify(user_data), 200
                return jsonify({"error": "User not updated"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401