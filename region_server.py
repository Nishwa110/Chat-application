import sys #helps system to read command line instructions like port number
from flask import Flask
from flask_socketio import SocketIO, send #send helps to send messages.

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") #CORS = cross over resource sharing, it allows communication from all over the world.

@socketio.on('message')
def handle_message(msg):
    print(f"[REGION] Received: {msg}")
    # echo back with region tag
    send(f"[handled-by-region] {msg}", broadcast=True)

if __name__ == "__main__":
    region = sys.argv[1] if len(sys.argv) > 1 else "asia"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5001
    print(f"Starting region {region} on port {port}")
    socketio.run(app, host="127.0.0.1", port=port)
