# import usb
# import usb.util
# dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
# print(dev)
import os
os.environ['BLINKA_FT232H'] = "1"
import board
from adafruit_tmp11X import TMP117, TMP116, TMP119, AverageCount, MeasurementMode, MeasurementDelay
import time
import datetime

deg_sybm = u'\N{DEGREE SIGN}'

i2c = board.I2C()  # uses board.SCL and board.SDA
t1 = TMP116(i2c_bus=i2c, address=0x49)
# t2 = TMP116(i2c_bus=i2c, address=0x47)
# t3 = TMP116(i2c_bus=i2c, address=0x48)


# add  to this array multiple sensors.
# address limitation for single device allow to add up to 4 devises
# However you may add different I2C busses to array
sensors = [t1,]
print(AverageCount.AVERAGE_32X)

for sensor in sensors:
    sensor.measurement_mode = MeasurementMode.CONTINUOUS
    sensor.averaged_measurements = AverageCount.AVERAGE_32X
    sensor.measurement_delay = MeasurementDelay.DELAY_0_0015_S


def get_temperature():
    temp = []
    for sensor in sensors:
        temp.append(sensor.temperature_updated)
    return temp


while True:
    txt = f"{datetime.datetime.now()},Temperature:[{deg_sybm}C]: {get_temperature()} "
    print(txt)
    # time.sleep(1)