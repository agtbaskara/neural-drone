import time
import board
import digitalio

print("Led Test")

led1 = digitalio.DigitalInOut(board.D20)
led2 = digitalio.DigitalInOut(board.D21)

led1.direction = digitalio.Direction.OUTPUT
led2.direction = digitalio.Direction.OUTPUT

while True:
    led1.value = True
    led2.value = False
    time.sleep(0.5)
    led1.value = False
    led2.value = True
    time.sleep(0.5)
