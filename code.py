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
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

#BLE setup
SEND_RATE = 10 # how often in seconds to send text
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
ble.start_advertising(advertisement)

#I2C setup
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
# Set the rotation if depending on how your sensor is mounted.
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
    output_text = 'Temp: {} C'.format(sensor.temperature) 
    output_text += "\nPressure: {} hPa".format(sensor.pressure)
    output_text += "\nAltitude: {:.1f} m".format(sensor.altitude)
    output_text += "\nHumidity: {0}%".format(hum_sensor.relative_humidity)
    output_text += "\nAcceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (acc_sensor.acceleration)
    output_text += "\nGyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (acc_sensor.gyro)

    mag_x, mag_y, mag_z = mag_sensor.magnetic

    output_text +="\nMag X:{0:10.2f}, Mag Y:{1:10.2f}, Mag Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z)

    output_text +="\nProximity: {0}".format(apds_sensor.proximity)

    r, g, b, c = apds_sensor.color_data
    output_text += "Red: {0}, Green: {1}, Blue: {2}, Clear: {3}:".format(r, g, b, c)
    
    gesture = apds_sensor.gesture()

    if gesture == 0x01:
        my_gesture = "Gesture: up"
    elif gesture == 0x02:
        my_gesture = "Gesture: down"
    elif gesture == 0x03:
        my_gesture = "Gesture: left"
    elif gesture == 0x04:
        my_gesture = "Gesture: right"
    else:
        my_gesture = "Gesture: none"

    output_text += "\n" + my_gesture

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    output_text += "\nMicrophone: %s" % (magnitude,)

    output_text += "\nButton A: {}".format(not button_a.value)
    output_text += "\nButton B: {}".format(not button_b.value)

    output_text += "\n\n"

    print(output_text)

    if ble.connected:
        ble.stop_advertising()
        print("BLE CONNECTED")
        uart_server.write(output_text.encode())
    time.sleep(0.1)
