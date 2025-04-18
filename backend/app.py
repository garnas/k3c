import logging
import os

from flask import Flask, request
from flask_socketio import SocketIO, emit

_static_folder = os.path.join("..", "frontend", "dist")

app = Flask(__name__, static_folder=_static_folder)
app.logger.setLevel(logging.INFO)

socketio = SocketIO(app, cors_allowed_origins="*")


class SidHandler:
    sids: set[str] = set()

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def public(path):
    return app.send_static_file(path)

@app.route('/b')
def broadcast():
    # Define the message payload
    message_payload = {'data': "Someone just accessed the root ('/') page!"}

    # Define the event name for the clients to listen to
    event_name = 'server_broadcast'

    app.logger.info(f"Broadcasting message via Socket.IO event '{event_name}' due to GET / request.")

    # Use socketio.emit() to send to ALL connected clients
    # The first argument is the event name.
    # The second argument is the data payload (must be JSON-serializable).
    socketio.emit(event_name, message_payload)

    # Optional: If you want to use the default 'message' event name, you can use:
    # socketio.send("Someone just accessed the root ('/') page!")
    message_payload = {'data': f"0PAYLOAD!!{SidHandler.sids}"}
    for sid in SidHandler.sids:
        socketio.emit(event_name, message_payload, to=sid)
    app.logger.info(f"Sent message via route to (SID: {SidHandler.sids}): HELLO!!")

    # Return the standard HTTP response for the route
    return "Hello World! A broadcast message was sent to all connected Socket.IO clients."

# Standard Socket.IO connection event
@socketio.on('connect')
def handle_connect():
    SidHandler.sids.add(request.sid)
    app.logger.info(f'Client connected {request.sid}')

# Standard Socket.IO disconnection event
@socketio.on('disconnect')
def handle_disconnect():
    SidHandler.sids.remove(request.sid)
    app.logger.info('Client disconnected')

# Custom event handler - rename from 'message' to avoid conflict
# with the default 'message' event if you want distinct handling.
# Or keep 'message' if that's what your client sends.
@socketio.on('my_message')
def handle_my_message(data):
    app.logger.info('received custom message: ' + str(data)) # Handle dict or str
    # Echo the message back to the specific client who sent it
    emit('my_response', {'data': 'Server received: ' + str(data)})
    # Or broadcast to everyone:
    # emit('my_response', {'data': 'Server received: ' + str(data)}, broadcast=True)

@socketio.on('my_send_message')
def handle_my_send_message(data):
    app.logger.info('received custom message: ' + str(data)) # Handle dict or str
    # Echo the message back to the specific client who sent it
    emit('my_response', {'data': 'Server received: ' + str(data)}, broadcast=True)


# You can still handle the default 'message' event if needed
@socketio.on('message')
def handle_message(data):
    app.logger.info('received default message: ' + str(data))
    emit('message', 'Server echo: ' + str(data)) # Echo back on 'message' event