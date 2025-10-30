from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")
    socketio.send(f"Bot: Got your message '{msg}'", broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
print("Encryption key:", key.decode())  # (For reference only)
@socketio.on('message')
def handle_message(msg):
    # Decrypt if possible
    try:
        decrypted_msg = cipher.decrypt(msg.encode()).decode()
        print(f"Decrypted message: {decrypted_msg}")
    except:
        decrypted_msg = msg  # normal text if not encrypted
        print(f"Plain message: {decrypted_msg}")

    # Process and reply securely
    reply = f"Server reply: {decrypted_msg}"
    encrypted_reply = cipher.encrypt(reply.encode()).decode()
    socketio.send(encrypted_reply, broadcast=True)
