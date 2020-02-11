# Neural Drone
flight controller with a mix of neural network

## Requirement
- Raspberry Pi 4 Model B
- Flight Controller HAT

## Notes
- TODO

## Install Adafruit Blinka
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

## Enable I2C
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

## Enable SPI
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-spi

## Test Program Notes
- blinkatest.py
Test Blinka Installation I2C, SPI, and GPIO access
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- bmp388test.py
Test BMP388 Barometer
https://learn.adafruit.com/adafruit-bmp388/python-circuitpython
- bno055test.py
Test BNO055 IMU
https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/python-circuitpython
- gpstest.py
Test GPS
- ms5611test.py
Test MS5611 Barometer
- motortest.py
Test 4 Brushless Motor
- pca9685test.py
Test PCA9685 I2C PWM Driver
https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
- sbustest.py
Test SBUS


Install GPS
pip3 install pynmea2

Enable tty access
https://www.raspberrypi.org/forums/viewtopic.php?t=180254

enable additional serial port
https://lb.raspberrypi.org/forums/viewtopic.php?t=244827

enable_uart=1
dtoverlay=pi3-miniuart-bt
dtoverlay=uart5
dtoverlay=uart4
dtoverlay=uart3
dtoverlay=uart2

## Reference
- CoppeliaSim B0-based remote API http://www.coppeliarobotics.com/helpFiles/en/b0RemoteApi-python.htm
- Pygame Joystick https://www.pygame.org/docs/ref/joystick.html
- SBUS to USB https://github.com/agtbaskara/sbusjoystick-ardupilot-sitl