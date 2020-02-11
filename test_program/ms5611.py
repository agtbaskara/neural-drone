#!/usr/bin/python
# -*- coding: utf-8 -*-

import smbus
import time
import sys

bus = smbus.SMBus(1)

MS561101BA_ADDR_HIGH = 0x77   # CBR=1 0x76 I2C address when CSB is connected to HIGH (VCC)
MS561101BA_ADDR_LOW = 0x77    # CBR=0 0x77 I2C address when CSB is connected to LOW (GND)

# registers of the device
MS561101BA_D1 = 0x40
MS561101BA_D2 = 0x50
MS561101BA_RESET = 0x1E

# D1 and D2 result size (bytes)
MS561101BA_D1D2_SIZE = 3

# OSR (Over Sampling Ratio) constants
MS561101BA_OSR_256 = 0x00
MS561101BA_OSR_512 =  0x02
MS561101BA_OSR_1024 = 0x04
MS561101BA_OSR_2048 = 0x06
MS561101BA_OSR_4096 = 0x08

MS561101BA_PROM_BASE_ADDR = 0xA0    # by adding ints from 0 to 6 we can read all the prom configuration values. 
# C1 will be at 0xA2 and all the subsequent are multiples of 2
MS561101BA_PROM_REG_COUNT = 6       # number of registers in the PROM
MS561101BA_PROM_REG_SIZE = 2        # size in bytes of a prom registry.


c = []

def reset_sensor():
    try:
        bus.write_byte(MS561101BA_ADDR_HIGH, MS561101BA_RESET)    
        time.sleep(0.02)
    except IOError:
        print "Error reading the sensor"
        sys.exit(1)
    

def read_prom_params():
    try:
        for i in range(0, MS561101BA_PROM_REG_COUNT + 1):
            block = bus.read_i2c_block_data(MS561101BA_ADDR_HIGH, 2 * i + MS561101BA_PROM_BASE_ADDR)
            val = (block[0] << 8) | block[1]
            c.append(val) 
    except IOError:
        print "Error reading the sensor"
        sys.exit(1)

def read_raw_temp():
    raw_temperature = 0
    # start conversion
    bus.write_byte(MS561101BA_ADDR_HIGH, 0x58)
    time.sleep(0.01)
    raw_temp_block = bus.read_i2c_block_data(MS561101BA_ADDR_HIGH, 0x00)
    raw_temperature = (raw_temp_block[0] << 16) | (raw_temp_block[1] << 8) | (raw_temp_block[2] << 0)
    return raw_temperature


def read_raw_pressure():
    raw_pressure = 0 
    # start conversion
    bus.write_byte(MS561101BA_ADDR_HIGH, 0x48)
    time.sleep(0.01)
    raw_pressure_block = bus.read_i2c_block_data(MS561101BA_ADDR_HIGH, 0x00)
    raw_pressure = (raw_pressure_block[0] << 16) | (raw_pressure_block[1] << 8) | (raw_pressure_block[2] << 0)
    return raw_pressure

def get_data():
    raw_pressure = read_raw_pressure()
    raw_temp = read_raw_temp()
    deltaT = raw_temp - (c[5] << 8)
    temperature = 2000 + ((deltaT * c[6]) >> 23)
    offset = (c[2] << 16) + ((deltaT * c[4]) >> 7)
    sensitivity = (c[1] << 15) + ((c[3] * deltaT) >> 8)
    pressure = (((raw_pressure * sensitivity) >> 21) - offset) >> 15
    
    if temperature < 200:
        temperature_prime = 0
        offset_prime = 0
        sensitivity_prime = 0
        
        temperature_prime = (deltaT, 2) / 2147483648
        offset_prime = 5 * (((temperature - 2000) << 2) >> 2)
        sensitivity_prime = 5 * (((temperature - 2000) << 2) >> 4)

        if (temperature < -1500):
            offset_prime = offset_prime + 7 * ((temperature + 1500) << 2)
            sensitivitiy_prime = sensitivity_prime + 11 * (((temperature + 1500) << 2) >> 2)

        temperature -= temperature_prime
        offset -= offset_prime
        sensitivity -= sensitivity_prime

    return float(temperature) / 100, float(pressure) / 100

if __name__ == '__main__':
    reset_sensor() 
    read_prom_params()
    try:
        while True:
            temperature, pressure = get_data()
            print "Temperature: {0:.2f} °C\t Pressure: {1:.2f} hPa".format(temperature, pressure)
            time.sleep(1)
    except KeyboardInterrupt:
        print "Bye!"
        sys.exit(0)
    except IOError:
        print "Error reading the sensor"
        sys.exit(1)
