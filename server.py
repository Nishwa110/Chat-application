from flask import Flask # framework to run the backend
from flask_socketio import SocketIO # for real time communication
from Crypto.Cipher import AES # for encryption and decryption
import base64 # for converting binary data to readable strings
import threading # allows to run 2 actions at a time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myflasksecret'
socketio = SocketIO(app, cors_allowed_origins="*") # Important bcs it allows to send and recieve message.

SECRET_KEY = "mysecretkey12345"  #16 bytes key bcs this is required by AES, important for encryption and decryption
BLOCK_SIZE = 16

# The AES only encrypts multiple of 16 bytes data so if our message is not multiple of 16 it would add extra spaces before encryption -> def pad and it will remove extra spaces before decryption -> def unpad.

def pad(s):
    pad_len = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + chr(pad_len) * pad_len

def unpad(s):
    return s[:-ord(s[-1])]

def encrypt_message(msg):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    # AES comes from the crypto.cipher library, it helps to encrypt data
    padded = pad(msg)
    encrypted = cipher.encrypt(padded.encode('utf-8')) #utf format bcs this algo takes data in bytes not in plain text.
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_message(enc):
    cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_ECB)
    decoded = base64.b64decode(enc)
    decrypted = cipher.decrypt(decoded).decode('utf-8')
    return unpad(decrypted)

@socketio.on('message')
# This is just a decorator that alerts the func when a text is recieved.
def handle_message(encrypted_msg):
    try:
        decrypted_msg = decrypt_message(encrypted_msg)
        print(f"Encrypted message received: {encrypted_msg}")
        print(f"Decrypted message: {decrypted_msg}")

    except Exception as e:
        print(f"Decryption error (ignored): {e}")

# This function allows us to send message through server.

def send_server_messages():
    while True:
        msg = input("(server): ")
        if msg.strip():
            encrypted = encrypt_message(f"Bot: {msg}")
            socketio.emit('message', encrypted)
            print(f"Encrypted message sent: {encrypted}")

if __name__ == "__main__":
    threading.Thread(target=send_server_messages, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000)
 # Without the above code our projec won't start.
 # Without daemon our application won't stop.
