# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_tmp117`
================================================================================

CircuitPython library for the TI TMP117 Temperature sensor

* Author(s): Bryan Siepert

parts based on SparkFun_TMP117_Arduino_Library by Madison Chodikov @ SparkFun Electronics:
https://github.com/sparkfunX/Qwiic_TMP117
https://github.com/sparkfun/SparkFun_TMP117_Arduino_Library

Implementation Notes
--------------------

**Hardware:**

* Adafruit TMP117 Breakout <https:#www.adafruit.com/product/PID_HERE>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https:#github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https:#github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https:#github.com/adafruit/Adafruit_CircuitPython_Register
"""

from struct import unpack_from
from time import sleep
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits, ROBits
__version__ = "0.0.0-auto.0"
__repo__ = "https:#github.com/adafruit/Adafruit_CircuitPython_TMP117.git"


_I2C_ADDR = 0x48 # default I2C Address
_TEMP_RESULT = const(0x00)
_CONFIGURATION = const(0x01)
_T_HIGH_LIMIT = const(0x02)
_T_LOW_LIMIT = const(0x03)
_EEPROM_UL = const(0x04)
_EEPROM1 = const(0x05)
_EEPROM2 = const(0x06)
_TEMP_OFFSET = const(0x07)
_EEPROM3 = const(0x08)
_DEVICE_ID = const(0x0F)
_DEVICE_ID_VALUE = 0x0117
_TMP117_RESOLUTION = 0.0078125	# Resolution of the device, found on (page 1 of datasheet)

_CONTINUOUS_CONVERSION_MODE = 0b00 # Continuous Conversion Mode
_ONE_SHOT_MODE = 0b11 # One Shot Conversion Mode
_SHUTDOWN_MODE = 0b01 # Shutdown Conversion Mode

class TMP117:
  """Library for the TI TMP117 high-accuracy temperature sensor"""
  _part_id = ROUnaryStruct(_DEVICE_ID, ">H")
  _raw_temperature = ROUnaryStruct(_TEMP_RESULT, ">h")

  def __init__(self, i2c_bus, address=_I2C_ADDR):

    self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
    if self._part_id != _DEVICE_ID_VALUE:
        raise AttributeError("Cannot find a TMP117")

  @property
  def temperature(self):
    return self._raw_temperature * _TMP117_RESOLUTION
