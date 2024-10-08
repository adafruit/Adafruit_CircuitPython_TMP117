# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import os
os.environ['BLINKA_FT232H'] = "1"
import board

from adafruit_tmp11X import TMP116, AverageCount

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
t1 = TMP116(i2c_bus=i2c, address=0x49)

# uncomment different options below to see how it affects the reported temperature
# and measurement time

# t1.averaged_measurements = AverageCount.AVERAGE_1X
# t1.averaged_measurements = AverageCount.AVERAGE_8X
t1.averaged_measurements = AverageCount.AVERAGE_32X
# t1.averaged_measurements = AverageCount.AVERAGE_64X

print(
    "Number of averaged samples per measurement:",
    AverageCount.string[t1.averaged_measurements],
)
print(
    "Reads should take approximately",
    AverageCount.string[t1.averaged_measurements] * 0.0155,
    "seconds",
)

while True:
    print("Single measurement: %.2f degrees C" % t1.take_single_measurement())
    # time.sleep(1)
