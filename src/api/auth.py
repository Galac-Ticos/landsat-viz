from flask import request, jsonify
from flask.views import MethodView
from src.utils import get_user_by_email_and_password

class AuthView(MethodView):
    def post(self):
        data = request.get_json()
        if 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400

        email = data['email']
        password = data['password']
        id_token = get_user_by_email_and_password(email, password)
        if id_token:
            return jsonify({"message": "Authentication successful", "token": id_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
