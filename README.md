Introduction
============

I bought an Adafruit CLUE nrf5280 and found the getting started documentation scattered.  Here's what I put together to quickly sample all the sensors and onboard devices.

Installation
============

1. Download the latest CircuitPython image from https://circuitpython.org/board/clue_nrf52840_express/ (at time of writing this it is version 7.0.0)
2. Install CircuitPython by copying the .UF2 image onto your device.  To mount the device connect to your computer and double tap the reset button.  Note, copying this onto the device will erase anything on it.
3. Figure out which serial port your device it outputting to and use a terminal program to interact with it - way easier than trying to read the micro display on the device.


Example Output
==============
    Temp: 30.0975 C
    Pressure: 1012.93hPa
    Altitude: 25.6 m
    Humidity: 37.116%
    Acceleration: X:-5.92, Y: 5.29, Z: -5.51 m/s^2
    Gyro X:0.05, Y: -0.10, Z: -0.03 degrees/s
    Mag X:      9.78, Mag Y:     -1.74, Mag Z:    -45.88 uT
    Proximity: 0
    Red: 768, Green: 741, Blue: 812, Clear: 2097
    Gesture: none
    Microphone: 4.84187
    Button A: False
    Button B: False

Notes
=====

The overwhelming majority of this code is stuff that I borrowed from Adafruit's examples or CircuitPython's docs.  I just couldn't find a single place that had everything I needed in one spot. 