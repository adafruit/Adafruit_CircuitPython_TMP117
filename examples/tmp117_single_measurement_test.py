# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import board
import adafruit_tmp117

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tmp117 = adafruit_tmp117.TMP117(i2c)

# uncomment different options below to see how it affects the reported temperature
# and measurement time

# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_1X
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_8X
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_32X
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_64X

print(
    "Number of averaged samples per measurement:",
    tmp117.averaged_measurements,
)

while True:
    print("Single measurement: %.2f degrees C" % tmp117.take_single_measurement())
    # time.sleep(1)
