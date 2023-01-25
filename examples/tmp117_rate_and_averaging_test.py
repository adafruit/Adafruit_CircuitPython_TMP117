# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member

# This example is best viewed using a serial plotter
# such as the one built into the Mu editor.
import time
import board
import adafruit_tmp117

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tmp117 = adafruit_tmp117.TMP117(i2c)

# uncomment different options below to see how it affects the reported temperature
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_1X
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_8X
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_32X
# tmp117.averaged_measurements = adafruit_tmp117.AVERAGE_64X

# tmp117.measurement_delay = adafruit_tmp117.DELAY_0_0015_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_0_125_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_0_250_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_0_500_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_1_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_4_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_8_S
# tmp117.measurement_delay = adafruit_tmp117.DELAY_16_S

print(
    "Number of averaged samples per measurement:",
    tmp117.averaged_measurements,
)
print("Minimum time between measurements:", tmp117.measurement_delay)
print("")

while True:
    print("Temperature:", tmp117.temperature)
    time.sleep(1)
