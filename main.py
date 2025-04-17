from backend.app import app, socketio

if __name__ == "__main__":
    app.logger.info("Starting server ...")
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True, port=5000)