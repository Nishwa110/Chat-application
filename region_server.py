# backend/region_server.py
# Run this file with an argument: region name and port
# Example: python region_server.py asia 5001

import sys
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Region server running"

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
