# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_tmp117

i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_debug_i2c import DebugI2C
i2c = DebugI2C(i2c)


tmp117 = adafruit_tmp117.TMP117(i2c)

while True:
    print("Temperature: %.2f degrees C"%tmp117.temperature)
    time.sleep(1)