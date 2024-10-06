from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.api.auth import AuthView
from src.api.user import UserView
from src.api.notification import NotificationView
from src.api.location import LocationView

load_dotenv()
app = Flask(__name__)

ENV = os.environ.get('ENV', 'DEV')

# Setup CORS
cors = CORS(app, resources={
    r"/auth": {
        "origins": "*" if ENV == "DEV" else "https://landsat-viz.vercel.app"
    }
})

# Register resources views
app.add_url_rule('/auth', view_func=AuthView.as_view('auth'))
app.add_url_rule('/users', view_func=UserView.as_view('users'))
app.add_url_rule('/notifications', view_func=NotificationView.as_view('notifications'))
app.add_url_rule('/locations', view_func=LocationView.as_view('locations'))

# Basic route without authorization
@app.route('/hello', methods=['GET'])
def hello():
    return {"message": "Hello user without authentication process"}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
