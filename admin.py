import os
import json
import getpass
import hashlib
import secrets
import base64

class AdminManager:
    def __init__(self, admin_file="admin_credentials.json"):
        self.admin_file = admin_file
        self.key = None

    def initialize_admin(self):
        """Set up admin credentials if they don't exist."""
        if not os.path.exists(self.admin_file):
            print("\nFirst-time setup: Create admin credentials")
            while True:
                admin_password = getpass.getpass("Create admin password: ")
                confirm_password = getpass.getpass("Confirm admin password: ")
                if admin_password == confirm_password:
                    salt = secrets.token_bytes(16)
                    key = hashlib.pbkdf2_hmac(
                        'sha256',
                        admin_password.encode('utf-8'),
                        salt,
                        100000
                    )
                    admin_data = {
                        'salt': base64.b64encode(salt).decode('utf-8'),
                        'key': base64.b64encode(key).decode('utf-8')
                    }
                    with open(self.admin_file, 'w') as f:
                        json.dump(admin_data, f)
                    print("Admin credentials created successfully!")
                    break
                else:
                    print("Passwords don't match. Please try again.")

    def verify_admin(self):
        """Verify admin credentials and set encryption key."""
        if not os.path.exists(self.admin_file):
            print("Admin credentials not found. Please set up first.")
            return False

        with open(self.admin_file, 'r') as f:
            admin_data = json.load(f)

        salt = base64.b64decode(admin_data['salt'])
        stored_key = base64.b64decode(admin_data['key'])

        password = getpass.getpass("Enter admin password: ")
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        if key == stored_key:
            self.key = key
            return True
        return False
    
    def reset_admin(self):
        """Reset admin credentials."""
        print("\nAdmin Password Reset")
        if os.path.exists(self.admin_file):
            os.remove(self.admin_file)
        
        print("Creating new admin credentials")
        self.initialize_admin()

    def get_key(self):
        return self.key
