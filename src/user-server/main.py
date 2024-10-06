import pyrebase
import hashlib
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Access the environment variables
api_key = os.environ.get('API_KEY')
database_url = os.environ.get('DATABASE_URL')

print(f"API Key: {api_key}")
print(f"Database URL: {database_url}")


# Firebase configuration, replace with your Firebase project's settings
config = {
    "apiKey": os.environ.get('API_KEY'),
    "authDomain": os.environ.get('AUTH_DOMAIN'),
    "databaseURL": os.environ.get('DATABASE_URL'), 
    "projectId": os.environ.get('PROJECT_ID'),
    "storageBucket": os.environ.get('STORAGE_BUCKET'),
    "messagingSenderId": os.environ.get('MESSAGING_SENDER_ID'),
    "appId": os.environ.get('APP_ID')
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Function to hash a password using SHA-256
def hash_password(password):
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

# Create a user and save to Firebase
def create_user(email, password, threshold, location, notifications):
    encrypted_password = hash_password(password)

    # Create user in Firebase Authentication
    try:
        user = auth.create_user_with_email_and_password(email, encrypted_password)
        user_id = user['localId']

        # Save user details to Firebase Realtime Database
        user_data = {
            "email": email,
            "threshold": threshold,
            "location": location,  # List of location with longitude and latitude
            "notifications": notifications  # List of notifications
        }
        db.child("users").child(user_id).set(user_data)
        print(f"User {email} created successfully!")
    except Exception as e:
        print(f"Error creating user: {e}")

# Example Data
email = "testuser@example.com"
password = "securepassword123"
threshold = 0.85  # Threshold example
location = [
    {"longitud": -84.123456, "latitud": 9.876543},
    {"longitud": -83.123456, "latitud": 10.876543}
]
notifications = [
    {"motivo": "Satellite view successful", "leido": False},
    {"motivo": "Threshold not met", "leido": True}
]

# Create user
#create_user(email, password, threshold, location, notifications)

# Read user data from Firebase
def get_user(user_id):
    try:
        user_data = db.child("users").child(user_id).get()
        if user_data.val():
            return user_data.val()  # Return user data
        else:
            return f"User with ID {user_id} not found."
    except Exception as e:
        return f"Error reading user data: {e}"

# Update user data in Firebase
def update_user(user_id, update_data):
    try:
        db.child("users").child(user_id).update(update_data)
        return f"User {user_id} updated successfully!"
    except Exception as e:
        return f"Error updating user data: {e}"

# Delete user from Firebase
def delete_user(user_id):
    try:
        # Delete user data from Realtime Database
        db.child("users").child(user_id).remove()
        return f"User {user_id} deleted successfully!"
    except Exception as e:
        return f"Error deleting user data: {e}"

# Get user by email and password
def get_user_by_email_and_password(email, password):
    encrypted_password = hash_password(password)  # Encrypt the password before sending

    try:
        # Authenticate user with email and password
        user = auth.sign_in_with_email_and_password(email, encrypted_password)
        user_id = user['localId']

        # Fetch user data from Realtime Database using the user ID
        user_data = db.child("users").child(user_id).get()
        if user_data.val():
            return user_data.val()  # Return the user data
        else:
            return f"No user data found for user ID {user_id}."
    except Exception as e:
        return f"Error fetching user data: {e}"

#user_info = get_user_by_email_and_password(email, password)
#print(user_info)

# Get notifications of a user
def get_user_notifications(email, password):
    try:
        # Authenticate the user using email and password
        user = auth.sign_in_with_email_and_password(email, hash_password(password))
        user_id = user['localId']

        # Fetch user data
        user_data = db.child("users").child(user_id).get()
        if user_data.val():
            # Retrieve the notifications
            notifications = user_data.val().get('notifications', [])
            return notifications
        else:
            return f"No user data found for user ID {user_id}."
    except Exception as e:
        return f"Error fetching notifications: {e}"

# Add a notification to a user
def add_user_notification(email, password, new_notification):
    try:
        # Authenticate the user
        user = auth.sign_in_with_email_and_password(email, hash_password(password))
        user_id = user['localId']

        # Fetch existing notifications
        user_data = db.child("users").child(user_id).get()
        if user_data.val():
            notifications = user_data.val().get('notifications', [])
            notifications.append(new_notification)

            # Update the notifications field in the database
            db.child("users").child(user_id).update({"notifications": notifications})
            return "Notification added successfully!"
        else:
            return f"No user data found for user ID {user_id}."
    except Exception as e:
        return f"Error adding notification: {e}"

#print("Current notifications:", get_user_notifications(email, password))

# Example: Add a new notification
#new_notification = {"motivo": "Satellite view successful", "leido": False}
#print(add_user_notification(email, password, new_notification))

# Check the notifications again
#print("Updated notifications:", get_user_notifications(email, password))

# Get the locations of a user
def get_user_locations(email, password):
    try:
        # Authenticate the user using email and password
        user = auth.sign_in_with_email_and_password(email, hash_password(password))
        user_id = user['localId']

        # Fetch user data
        user_data = db.child("users").child(user_id).get()
        if user_data.val():
            # Retrieve the locations (directions)
            directions = user_data.val().get('directions', [])
            return directions
        else:
            return f"No user data found for user ID {user_id}."
    except Exception as e:
        return f"Error fetching locations: {e}"

# Add a new location to a user
def add_user_location(email, password, new_location):
    try:
        # Authenticate the user using email and password
        user = auth.sign_in_with_email_and_password(email, hash_password(password))
        user_id = user['localId']

        # Fetch existing directions (locations)
        user_data = db.child("users").child(user_id).get()
        if user_data.val():
            directions = user_data.val().get('directions', [])
            directions.append(new_location)

            # Update the directions field in the database
            db.child("users").child(user_id).update({"directions": directions})
            return "Location added successfully!"
        else:
            return f"No user data found for user ID {user_id}."
    except Exception as e:
        return f"Error adding location: {e}"

print("Current locations:", get_user_locations(email, password))

# Example: Add a new location
new_location = {"longitud": -84.123456, "latitud": 9.876543}
print(add_user_location(email, password, new_location))

# Check the locations again
print("Updated locations:", get_user_locations(email, password))

