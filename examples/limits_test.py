# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
import adafruit_tmp117

i2c = busio.I2C(board.SCL, board.SDA)

tmp117 = adafruit_tmp117.TMP117(i2c)

tmp117.high_limit = 25
tmp117.low_limit = 10
print("\nHigh limit", tmp117.high_limit)
print("Low limit", tmp117.low_limit)

print("\n\n")
while True:
    print("Temperature: %.2f degrees C" % tmp117.temperature)
    alert_status = tmp117.alert_status
    print("High temperature alert:", alert_status.high_alert)
    print("Low temperature alert:", alert_status.low_alert)
    print("")
    time.sleep(1)
