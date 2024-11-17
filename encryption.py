# encryption.py
import base64
import json
import os
import getpass
import hashlib
import secrets

class Encryption:
    def __init__(self):
        self.admin_file = "admin_credentials.json"
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

    def encrypt_data(self, data):
        """Encrypt data using the admin key."""
        if not self.key:
            raise ValueError("Encryption key not set")
        
        data_str = json.dumps(data)
        data_bytes = data_str.encode('utf-8')
        key_bytes = self.key * (len(data_bytes) // len(self.key) + 1)
        encrypted = bytes([a ^ b for a, b in zip(data_bytes, key_bytes)])
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_data(self, encrypted_data):
        """Decrypt data using the admin key."""
        if not self.key:
            raise ValueError("Encryption key not set")
            
        encrypted_bytes = base64.b64decode(encrypted_data)
        key_bytes = self.key * (len(encrypted_bytes) // len(self.key) + 1)
        decrypted = bytes([a ^ b for a, b in zip(encrypted_bytes, key_bytes)])
        return json.loads(decrypted.decode('utf-8'))

