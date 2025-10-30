# security.py
from cryptography.fernet import Fernet

# Generate a key (run once and store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_message(message):
    """Encrypts a plain text message."""
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    """Decrypts an encrypted message."""
    return cipher.decrypt(encrypted_message.encode()).decode()
