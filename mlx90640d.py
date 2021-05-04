#!/usr/bin/python3

import board
import adafruit_mlx90640
import yaml
import socket
import busio
import numpy as np
import time

print("setting up mlx90640")
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)    # Set I2C freqency here
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # Set refresh rate here
refresh_rate = 2**(mlx.refresh_rate-1)
print("fps:", refresh_rate)
serial_number = mlx.serial_number
print("serial number:", serial_number)

print("connecting to frame socket... ")
connected = False
while not connected:
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect("/var/run/lepton-frames")
        connected = True
    except Exception:
        print("failed to connect to socket. Tying again in 5 seconds")
        time.sleep(5)
print("connected")

print("sending camera data over socket... ", end="")
camera_data = {
    "ResX": 32,
    "ResY": 24,
    "FPS": refresh_rate,
    "Model": "MLX90640",
    "Brand": "Melexis",
    "PixelBits": 16,
    "FrameSize": 32*24*2,
    "Firmware": "mlx90640 0.1.0",
    "CameraSerial": serial_number,
}
cameraYAML = yaml.dump(camera_data)
sock.sendall(bytes(cameraYAML, 'utf-8'))
sock.sendall(bytes("\n", 'utf-8'))
print("done")

print("sending frame data over socket")
frame = np.arange(768, dtype=np.half)
while (True):
    try:
        mlx.getFrame(frame)
    except ValueError:
        print("value error")
        continue
    sock.sendall(frame.tobytes())
