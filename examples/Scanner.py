# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import os
os.environ['BLINKA_FT232H'] = "1"
import board
import time
import busio
import datetime
i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

while True:
    print(datetime.datetime.now(),"I2C addresses found:", [hex(device_address)
        for device_address in i2c.scan()])
    time.sleep(2)
