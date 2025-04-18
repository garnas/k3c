from time import sleep

import socketio
from dotenv import dotenv_values

from sensor import Measurement
# from sensor_mock import Measurement

sio = socketio.Client()

config = dotenv_values(".env")

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
            sio.emit(event='json', data=measurement.__dict__, namespace='/sensor')
            print("Sent sensor data")
            sleep(1)
    except Exception as e:
        print(e)
        print("Retrying in 5 seconds...")
        sleep(5)
        main()


if __name__ == '__main__':
    main()
