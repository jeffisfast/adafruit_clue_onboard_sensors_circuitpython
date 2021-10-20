import board
import busio
import time
import adafruit_sht31d
import adafruit_bmp280
import adafruit_lis3mdl
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_apds9960.apds9960 import APDS9960
import array
import math
import audiobusio
import digitalio

i2c = busio.I2C(board.SCL, board.SDA)

#Temp, pressure, altitude
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
sensor.sea_level_pressure = 1016

#Magnetometer
mag_sensor = adafruit_lis3mdl.LIS3MDL(i2c)

#Gyro and Acceleration
acc_sensor = LSM6DS33(i2c)

#humidity
hum_sensor = adafruit_sht31d.SHT31D(i2c)

#Proximity, Color, Gesture
apds_sensor = APDS9960(i2c)
apds_sensor.enable_proximity = True
apds_sensor.enable_gesture = True
apds_sensor.enable_color = True
# Uncomment and set the rotation if depending on how your sensor is mounted.
apds_sensor.rotation = 270 # 270 for CLUE

#Audio sampling
# Remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)

def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)


# Buttons
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP


while True:
    print('Temp: {} C'.format(sensor.temperature)) 
    print('Pressure: {}hPa'.format(sensor.pressure))
    print("Altitude: {:.1f} m".format(sensor.altitude))

    print('Humidity: {0}%'.format(hum_sensor.relative_humidity))
    
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (acc_sensor.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (acc_sensor.gyro))

    mag_x, mag_y, mag_z = mag_sensor.magnetic
    print('Mag X:{0:10.2f}, Mag Y:{1:10.2f}, Mag Z:{2:10.2f} uT'.format(mag_x, mag_y, mag_z))

    print("Proximity: {0}".format(apds_sensor.proximity))
    r, g, b, c = apds_sensor.color_data
    print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))

    gesture = apds_sensor.gesture()

    if gesture == 0x01:
        print("Gesture: up")
    elif gesture == 0x02:
        print("Gesture: down")
    elif gesture == 0x03:
        print("Gesture: left")
    elif gesture == 0x04:
        print("Gesture: right")
    else:
        print("Gesture: none")

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print("Microphone: %s" % (magnitude,))

    print("Button A: {}".format(not button_a.value))
    print("Button B: {}".format(not button_b.value))
    time.sleep(0.1)

    print("")


