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
def create_user(email, password, threshold, location, notifications):
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

# Update user data in Firebase Realtime Database
def update_user(user_id, update_data):
    try:
        db.reference(f'users/{user_id}').update(update_data)
        print(f"User {user_id} updated successfully!")
        return True
    except Exception as e:
        print(f"Error updating user data: {e}")
    return None

# Delete user from Firebase Authentication and Realtime Database
def delete_user(user_id):
    try:
        # Delete user from Firebase Authentication
        auth.delete_user(user_id)

        # Delete user data from Firebase Realtime Database
        db.reference(f'users/{user_id}').delete()
        print(f"User {user_id} deleted successfully!")
        return True
    except Exception as e:
        print(f"Error deleting user data: {e}")
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
def get_user_notifications(user_id):
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
def add_user_notification(user_id, new_notification):
    try:
        # Fetch existing notifications
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            notifications = user_data.get('notifications', [])
            notifications.append(new_notification)

            # Update notifications field in the database
            db.reference(f'users/{user_id}').update({"notifications": notifications})
            return True
        print(f"No user data found for user ID {user_id}.")
    except Exception as e:
        print(f"Error adding notification: {e}")
    return None

# Get locations of a user
def get_user_locations(user_id):
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
def add_user_location(user_id, new_location):
    try:
        # Fetch existing directions (locations)
        user_data = db.reference(f'users/{user_id}').get()
        if user_data:
            directions = user_data.get('location', [])
            directions.append(new_location)

            # Update directions field in the database
            db.reference(f'users/{user_id}').update({"location": directions})
            return "Location added successfully!"
        print(f"No user data found for user ID {user_id}.")
    except Exception as e:
        print(f"Error adding location: {e}")
    return None