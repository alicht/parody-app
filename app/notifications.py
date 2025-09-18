import os
from typing import Optional
import firebase_admin
from firebase_admin import credentials, messaging


# Global variable to track initialization
firebase_initialized = False


def init_firebase() -> bool:
    """
    Initialize Firebase Admin SDK with service account credentials.
    
    Returns:
        True if initialization successful, False otherwise
    """
    global firebase_initialized
    
    if firebase_initialized:
        return True
    
    try:
        # Check for service account key file
        service_account_path = os.getenv('FIREBASE_CREDENTIALS', 'serviceAccountKey.json')
        
        if not os.path.exists(service_account_path):
            print(f"Firebase service account key not found at: {service_account_path}")
            return False
        
        # Initialize Firebase app
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
        firebase_initialized = True
        print("Firebase initialized successfully")
        return True
        
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return False


def send_notification(title: str, url: str) -> Optional[str]:
    """
    Send push notification to all subscribed users.
    
    Args:
        title: The headline/title of the tragedy article
        url: The URL to the article
        
    Returns:
        Message ID if successful, None if failed
    """
    # Ensure Firebase is initialized
    if not firebase_initialized:
        if not init_firebase():
            print("Cannot send notification: Firebase not initialized")
            return None
    
    try:
        # Create notification message
        message = messaging.Message(
            notification=messaging.Notification(
                title="Tragedy detected!",
                body=f'"{title}" — Don\'t forget to read it!'
            ),
            data={
                'url': url,
                'type': 'tragedy_alert'
            },
            # Send to topic that all users are subscribed to
            topic='tragedies'
        )
        
        # Send the message
        response = messaging.send(message)
        print(f"Successfully sent notification: {response}")
        return response
        
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None


def send_test_notification() -> Optional[str]:
    """
    Send a test notification to verify Firebase setup.
    
    Returns:
        Message ID if successful, None if failed
    """
    return send_notification(
        title="Test Tragedy Article",
        url="https://example.com/test"
    )


def subscribe_token_to_topic(token: str, topic: str = 'tragedies') -> bool:
    """
    Subscribe a device token to a topic for receiving notifications.
    
    Args:
        token: The FCM registration token
        topic: The topic to subscribe to (default: 'tragedies')
        
    Returns:
        True if successful, False otherwise
    """
    if not firebase_initialized:
        if not init_firebase():
            return False
    
    try:
        response = messaging.subscribe_to_topic([token], topic)
        
        if response.success_count > 0:
            print(f"Successfully subscribed token to topic '{topic}'")
            return True
        else:
            print(f"Failed to subscribe token to topic '{topic}'")
            return False
            
    except Exception as e:
        print(f"Error subscribing to topic: {e}")
        return False


# Initialize Firebase when module is imported
init_firebase()