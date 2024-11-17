from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
from threading import Thread
import random

app = Flask(__name__)

# Enable CORS for both HTTP and WebSocket
CORS(app, origins=["http://localhost:3000"], allow_headers=["Content-Type", "Authorization"])

# Initialize Flask-SocketIO with appropriate CORS settings for WebSocket
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Sample starting data
items = [
    {"id": 1, "name": "Item 1", "price": 10},
    {"id": 2, "name": "Item 2", "price": 20},
    {"id": 3, "name": "Item 3", "price": 30},
]

# A function to simulate updates to the items
def update_items():
    global items
    while True:
        time.sleep(2)  # Simulate an update every 5 seconds
        # Randomly change one item’s price to simulate a change
        items[random.randint(0, 2)]['price'] += random.randint(-1, 1)
        # Emit the updated data to all connected WebSocket clients
        socketio.emit('update', items)

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items)

# Start the background update function in a separate thread
def background_thread():
    thread = Thread(target=update_items)
    thread.daemon = True
    thread.start()

# Start WebSocket and the background thread on application startup
@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    emit('update', items)  # Emit initial data to the client when it connects
    background_thread()

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected!")

if __name__ == "__main__":
    socketio.run(app, debug=True)
