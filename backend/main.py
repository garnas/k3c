from backend.app import app, socketio

if __name__ == "__main__":
    # app.run(debug=False, port=5000,)
    app.logger.info("Starting server ...")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000)

    # socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000, host="0.0.0.0")
