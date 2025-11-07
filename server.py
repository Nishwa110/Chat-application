from flask import Flask
from flask_socketio import SocketIO
from Crypto.Cipher import AES
import base64
import threading
import sqlite3  
from datetime import datetime 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myflasksecret'
socketio = SocketIO(app, cors_allowed_origins="*")

SECRET_KEY = "mysecretkey12345"
BLOCK_SIZE = 16

conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    message TEXT,
    timestamp TEXT
)
""")
conn.commit()


# --- Encryption / Decryption Helpers ---
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


# --- Handle messages from clients ---
@socketio.on('message')
def handle_message(encrypted_msg):
    try:
        decrypted_msg = decrypt_message(encrypted_msg)
        print(f"Encrypted message received: {encrypted_msg}")
        print(f"Decrypted message: {decrypted_msg}")

        cursor.execute(
            "INSERT INTO chat_history (sender, message, timestamp) VALUES (?, ?, ?)",
            ("user", decrypted_msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

    except Exception as e:
        print(f"Decryption error (ignored): {e}")
# Server sends messages manually (admin / bot)
def send_server_messages():
    while True:
        msg = input("(server): ")
        if msg.strip():
            encrypted = encrypt_message(f"{msg}")
            socketio.emit('message', encrypted)
            print(f"Encrypted message sent: {encrypted}")

           
            cursor.execute(
                "INSERT INTO chat_history (sender, message, timestamp) VALUES (?, ?, ?)",
                ("bot", f"{msg}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()


if __name__ == "__main__":
    threading.Thread(target=send_server_messages, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000)
