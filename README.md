Introduction
============

I bought an Adafruit CLUE nrf5280 and found the getting started documentation scattered.  Here's what I put together to quickly sample all the sensors and onboard devices.

Installation
============

1. Download the latest CircuitPython image from https://circuitpython.org/board/clue_nrf52840_express/ (at time of writing this it is version 7.0.0)
2. Install CircuitPython by copying the .UF2 image onto your device.  To mount the device connect to your computer and double tap the reset button.  Note, copying this onto the device will erase anything on it.
3. Figure out which serial port your device it outputting to and use a terminal program to interact with it - way easier than trying to read the micro display on the device.
