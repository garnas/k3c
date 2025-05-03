import logging
import os
from datetime import datetime, timedelta

from dotenv import dotenv_values
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

from backend.measurement_manager import measurement_manager
from backend.sqlc.gen.query import CreateMeasurementParams, Querier

_static_folder = os.path.join("..", "frontend", "dist")

app = Flask(__name__, static_folder=_static_folder)
app.logger.setLevel(logging.INFO)

config = dotenv_values(".env")
DB_NAME = config.get("db_name")
DB_USER = config.get("db_user")
DB_PASSWORD = config.get("db_password")
DB_HOST = config.get("db_host")
DB_PORT = config.get("db_port")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db = SQLAlchemy()
db.init_app(app)


socketio = SocketIO(app, cors_allowed_origins="*")


class SidHandler:
    sids: set[str] = set()

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def public(path):
    return app.send_static_file(path)

@app.route("/measurements-weekly")
def measurements_weekly():
    app.logger.info(db.engine.pool.status())
    with db.engine.connect() as connection:
        q = Querier(conn=connection)
        one_week_ago = datetime.now() - timedelta(days=7)
        result = q.list_measurements_by_time(
            timestamp=one_week_ago
        )
        app.logger.info(db.engine.pool.status())
        fetched = [measurement_manager.serialize_measurement(r) for r in result][::2][::2]
    return jsonify(fetched)

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

@socketio.on(message='json', namespace='/sensor')
def handle_sensor_message(data):
    app.logger.info('received sensor data: ' + str(data)) # Handle dict or str
    app.logger.info(db.engine.pool.status())
    with db.engine.connect() as connection:
        q = Querier(conn=connection)
        params = CreateMeasurementParams(
            timestamp=datetime.now(),
            humidity=data["humidity"],
            temperature=data["temperature"],
            pressure=data["pressure"],
            gas_resistance=data["gas_resistance"],
        )
        q.create_measurement(
            arg=params
        )
        connection.commit()
    app.logger.info("!!!")
    for sid in SidHandler.sids:
        # socketio.emit(event_name, message_payload, )
        socketio.emit('live_measurement', data, to=sid)
    return "CREATED"

# You can still handle the default 'message' event if needed
@socketio.on('message')
def handle_message(data):
    app.logger.info('received default message: ' + str(data))
    emit('message', 'Server echo: ' + str(data)) # Echo back on 'message' event

@socketio.on('live_measurement')
def handle_live_measurement(data):
    app.logger.info('received default message: ' + str(data))
    emit('message', 'Server echo: ' + str(data)) # Echo back on 'message' event