import time
import serial

telemetry = serial.Serial(port="/dev/ttyAMA0", baudrate=57600, timeout=0.1)
while True:
    text = b'Telemetry Test\n'
    telemetry.write(text)
    print(text)
    time.sleep(1)
