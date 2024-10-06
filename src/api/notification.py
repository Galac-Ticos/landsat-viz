from flask import request, jsonify
from flask.views import MethodView
from src.utils import get_notifications, post_notification, verify_token, update_notification_read_by_message

class NotificationView(MethodView):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                user_notifications = get_notifications(user_id)
                if user_notifications:
                    return jsonify(user_notifications), 200
                return jsonify({"error": "User does not exist"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                data = request.get_json()
                message = data.get('message')
                if not message:
                    return jsonify({"error": "Notifications with message are required"}), 400
                user_notification = post_notification(user_id, message)
                if user_notification:
                    return jsonify(user_notification), 200
                return jsonify({"error": "Notification not created"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401

    def put(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            user_id = verify_token(token)
            if user_id:
                data = request.get_json()
                message = data.get('message')
                read = data.get('read')
                if not message or not read:
                    return jsonify({"error": "Notifications with message and read properties are required"}), 400
                user_notification = update_notification_read_by_message(user_id, message, read)
                if user_notification:
                    return jsonify(user_notification), 200
                return jsonify({"error": "Notification not created"}), 404
            return jsonify({"error": "Invalid token"}), 401
        return jsonify({"error": "Authorization header is required"}), 401
