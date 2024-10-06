import firebase_admin
from firebase_admin import credentials, auth, db
import os
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
    "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_CERT_URL"),
    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL")
})

firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ.get('FIREBASE_DATABASE_URL')
})
API_KEY = os.environ.get('FIREBASE_API_KEY')
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"


def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']
        return user_id
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

# Create a user and save to Firebase Authentication and Realtime Database
def post_user(email, password, threshold=0.70, location=[], notifications=[]):
    try:
        # Create user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password  # Firebase will hash it internally
        )
        user_id = user.uid

        # Save user details to Firebase Realtime Database
        user_data = {
            "email": email,
            "threshold": threshold,
            "location": location,  # List of locations with longitude and latitude
            "notifications": notifications  # List of notifications
        }
        db.reference(f'users/{user_id}').set(user_data)
        print(f"User {email} created successfully!")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Update a user password, email or threshold
def put_user(user_id, email, password, threshold):
    try:
        if email is not None or threshold is not None:
            update_data ={"email": email,  "password": password}
            auth.update_user(user_id, **update_data)
            print(f"User with id {user_id} updated on Firebase.")
        if threshold is not None:
            db.reference(f'users/{user_id}').update({'threshold': threshold})
            print(f"Threshold of user with ID {user_id} updated to {threshold}.")
        return {"success": True, "message": "User updated successfully"}
    except Exception as e:
        print(f"Error updating user: {e}")
        return {"success": False, "message": f"Error updating user: {e}"}


# Get user data from Firebase Realtime Database
def get_user(user_id):
    try:
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            return user_data  # Return user data
        print(f"User with ID {user_id} not found.")
    except Exception as e:
        print(f"Error reading user data: {e}")
    return None

# Authenticate user and return user data from Firebase Realtime Database
def get_user_by_email_and_password(email, password):
    try:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(FIREBASE_AUTH_URL, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            id_token = response_data['idToken']
            print("User authenticate successfully")
            return id_token
        else:
            print(f"Error when authenticate: {response_data.get('error', {}).get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error when authenticate: {e}")
        return None

# Get notifications of a user
def get_notifications(user_id):
    try:
        # Fetch user data
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            notifications = user_data.get('notifications', [])
            return notifications
        print(f"No user data found for user ID {user_id}.")
    except Exception as e:
        print(f"Error fetching notifications: {e}")
    return None

# Add a notification to a user
def post_notification(user_id, message):
    try:
        # Fetch existing notifications
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            notifications = user_data.get('notifications', [])
            notifications.append({"read":False, "message":message})
            # Update notifications field in the database
            db.reference(f'users/{user_id}').update({"notifications": notifications})
            return True
        print(f"No user data found for user ID {user_id}.")
    except Exception as e:
        print(f"Error adding notification: {e}")
    return None

def update_notification_read_by_message(user_id, message, read):
    try:
        notifications_ref = db.reference(f'users/{user_id}/notifications')
        notifications = notifications_ref.get()
        if notifications:
            for idx, notification in enumerate(notifications):
                if notification.get('message') == message:
                    notifications[idx]['read'] = read
                    notifications_ref.set(notifications)
                    return {"success": True, "message": f"Notification read status updated to {read}"}
            return {"success": False, "message": "Notification with the specified message not found"}
        else:
            return {"success": False, "message": "No notifications found for user"}
    except Exception as e:
        print(f"Error updating notification: {e}")
        return {"success": False, "message": f"Error updating notification: {e}"}

# Get locations of a user
def get_locations(user_id):
    try:
        # Fetch user data
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            directions = user_data.get('location', [])
            return directions
        print(f"No user data found for user ID {user_id}.")
    except Exception as e:
        print(f"Error fetching locations: {e}")
    return None

# Add a new location to a user
def post_location(user_id, longitude, latitude, description):
    try:
        # Fetch existing directions (locations)
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            directions = user_data.get('location', [])
            directions.append({"longitude": longitude, "latitude": latitude, "description": description})
            # Update directions field in the database
            db.reference(f'users/{user_id}').update({"location": directions})
            return "Location added successfully!"
        print(f"No user data found for user ID {user_id}.")
    except Exception as e:
        print(f"Error adding location: {e}")
    return None