import time

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 50

min_pulse=988
max_pulse=2012
min_duty = int((min_pulse * pca.channels[0].frequency) / 1000000 * 0xffff)
max_duty = (max_pulse * pca.channels[0].frequency) / 1000000 * 0xffff
duty_range = int(max_duty - min_duty)
print(duty_range)
print(min_duty)
print(max_duty)

value = 0
duty_cycle = min_duty + int(value * duty_range)
pca.channels[0].duty_cycle = duty_cycle
pca.channels[1].duty_cycle = duty_cycle
pca.channels[2].duty_cycle = duty_cycle
pca.channels[3].duty_cycle = duty_cycle

# Konversi PWM ke duty cycle
#pwm = 988
#duty_cycle = int((pwm * pca.channels[0].frequency) / 1000000 * 0xffff)


