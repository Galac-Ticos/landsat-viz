from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.data_user import verify_token, get_user_by_email_and_password

# Load environment variables from the .env file
load_dotenv()
app = Flask(__name__)

cors = CORS(app, resources={
    r"/auth": {
        "origins": "*" #"https://landsat-viz.vercel.app"
    }
})

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello user without authentication process"}), 200

@app.route('/hello-auth', methods=['GET'])
def protected_route_hello():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
        if user_id:
            return jsonify({"message": "Hello user authenticated", "user_id": user_id}), 200
        else:
            return jsonify({"error": "Invalid token"}), 401
    else:
        return jsonify({"error": "Authorization header is required"}), 401

@app.route('/auth', methods=['POST'])
def authenticate():
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
