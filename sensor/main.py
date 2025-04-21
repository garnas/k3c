from time import sleep

import requests
import socketio
from dotenv import dotenv_values

config = dotenv_values("../.env")

if config["sensor.is_mocked"].lower() == "true":
    from sensor_mock import Measurement
else:
    from sensor import Measurement


http_session = requests.Session()
http_session.verify = False

sio = socketio.Client(http_session=http_session)
# sio = socketio.Client()


@sio.event
def connect():
    print('connected to server')


@sio.event
def disconnect(reason):
    print('disconnected from server, reason:', reason)

def main():
    try:
        while True:
            if not sio.connected:
                print("Connecting to server")
                sio.connect(config['server.url'], namespaces="/sensor")

            print("Waiting for sensor data")
            measurement = Measurement.from_sensor()
            if measurement:
                sio.emit(event='json', data=measurement.__dict__, namespace='/sensor')
                print("Sent sensor data")
    except Exception as e:
        print(e)
        print("Retrying in 5 seconds...")
        sleep(5)
        main()


if __name__ == '__main__':
    main()
