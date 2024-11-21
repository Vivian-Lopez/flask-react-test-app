from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
from threading import Thread
import random

# Declare app as a new Flask app with the __name__ of this module (name of this script)
# This is an obejct which defines the routes and logic for handling HTTP requests and web socket connections.
app = Flask(__name__)

# Enable CORS for both HTTP and WebSocket
# --- What is CORS? Cross Origin Resource Sharing (Security Mechanism)
# When client sends a request to this server, the server sends a response with the origins that are
# allowed to access data from this server. We can specify the origins that are allowed to access data
# and the headers, Content-Type is needed for sending json data
CORS(app, origins=["http://localhost:3000"], allow_headers=["Content-Type"])

# Initialize Flask-SocketIO with appropriate CORS settings for WebSocket
# The cors_allowed_origins for this socket is the address and ip of the frontend
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

# Defining an API route allowing get methdods to act on it
# --- How does this decorator work?
# used to add functionality to the get_items function without modifying it by wrapping it.
# it binds a URL to a python function 
# so get_items should be called whenever a GET request is made to the /api/items path on the server
# an error is returned if GET is not used
@app.route('/api/items', methods=['GET'])
def get_items():
    # Retursns a json version of the items
    # Why is JSON used? serializable and deserializable, human readable and easy to convert to and from with libraries
    # standardised for APIs to use JSON
    # Also frontend is written with JS which natively supports JSON, so it comes with built in methods to 
    return jsonify(items)

# Start the background update function in a separate thread
def background_thread():
    """
    Creates a new thread that can run in parallel with the main function.
    It is a background task that doesn't need to complete before the program ends.
    So we also don't need to join when calling this thread as we don't have to wait for it to finish
    before exiting.
    """
    # Thread() creates a new thread
    # target=function sets the code that should run as the function code
    thread = Thread(target=update_items)
    # Setting daemon to be true means that it will not block the program from exiting when the main program finishes
    # If a thread is not a daemon, the program will wait for the thread to finish before exiting
    thread.daemon = True
    # Calling thread.start begins the exectuion of the update_items function in that thread
    thread.start()

# Start WebSocket and the background thread on application startup
@socketio.on('connect')
def handle_connect():
    """
    Event handler for someone connecting to our socket.
    """
    print("Client connected!")
    # Emit sends an event to the client, which can trigger a corresponding handler on the client side
    emit('update', items)  # Emit initial data to the client when it connects
    background_thread()

@socketio.on('disconnect')
def handle_disconnect():
    """
    Event handler for someone disconnected from our socket
    """
    print("Client disconnected!")

if __name__ == "__main__":
    # Starts a server that listens for HTTP and WebSocket connections
    # App is run in the context of the server making the Flask routes and WebSocket event handlers active
    # and ready to handle incoming connections
    # with debug=True, any change to the code will automatically reload the server and errors or exceptions
    # will be shown in the terminal, helping with development
    # How does it automatically reload? Reloader monitors any .py files and html are monitored
    # app restarta and web socket connections briefly disconnect
    socketio.run(app, debug=True)
