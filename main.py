from backend.app import app, socketio

if __name__ == "__main__":
    app.logger.info("Starting development server ...")
    app.logger.info("http://127.0.0.1:5000/")
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True, port=5000, host="0.0.0.0")
