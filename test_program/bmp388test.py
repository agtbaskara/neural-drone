import time
import board
import busio
import adafruit_bmp3xx
 
# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
 
bmp.sea_level_pressure = bmp.pressure

while True:
    print("Pressure: {}".format(bmp.pressure))
    print("Temperature: {}".format(bmp.temperature))
    print('Altitude: {} meters'.format(bmp.altitude))
    time.sleep(0.5)
