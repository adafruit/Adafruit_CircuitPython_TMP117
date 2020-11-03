# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member

# This example is best viewed using a serial plotter such as the one built into the Mu editor.
import time
import board
import busio
from adafruit_tmp117 import TMP117, AverageCount

i2c = busio.I2C(board.SCL, board.SDA)

tmp117 = TMP117(i2c)

tmp117.averaged_measurements = AverageCount.AVERAGE_1X
tmp117.averaged_measurements = AverageCount.AVERAGE_32X
print(
    "Number of averaged samples per measurement:",
    AverageCount.string[tmp117.averaged_measurements],
)

while True:
    print("Temperature:", tmp117.temperature)
    time.sleep(0.01)
