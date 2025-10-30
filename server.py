from flask import Flask
from flask_socketio import SocketIO
from Crypto.Cipher import AES
import base64, threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myflasksecret'
socketio = SocketIO(app, cors_allowed_origins="*")

# 🔐 Must match frontend
SECRET_KEY = "mysecretkey12345"  # 16 bytes
BLOCK_SIZE = 16

def pad(s):
    pad_len = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + chr(pad_len) * pad_len

def unpad(s):
    return s[:-ord(s[-1])]

def encrypt_message(msg):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    padded = pad(msg)
    encrypted = cipher.encrypt(padded.encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_message(enc):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    decoded = base64.b64decode(enc)
    decrypted = cipher.decrypt(decoded).decode('utf-8')
    return unpad(decrypted)

@socketio.on('message')
def handle_message(encrypted_msg):
    try:
        decrypted_msg = decrypt_message(encrypted_msg)
        print(f"Encrypted message received: {encrypted_msg}")
        print(f"Decrypted message: {decrypted_msg}")

        '''if decrypted_msg:
            print(f"User says: {decrypted_msg}")
            global last_user_message
            last_user_message = decrypted_msg'''

    except Exception as e:
        # Ignore unencrypted or malformed messages
        print(f"Decryption error (ignored): {e}")

def send_server_messages():
    while True:
        msg = input("You (server): ")
        if msg.strip():
            encrypted = encrypt_message(f"Bot: {msg}")
            socketio.emit('message', encrypted)
            print(f"Encrypted message sent: {encrypted}")

if __name__ == "__main__":
    threading.Thread(target=send_server_messages, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000)
