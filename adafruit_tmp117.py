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

from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct

from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_register.i2c_bits import RWBits

__version__ = "0.0.0-auto.0"
__repo__ = "https:#github.com/adafruit/Adafruit_CircuitPython_TMP117.git"


_I2C_ADDR = 0x48  # default I2C Address
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
_TMP117_RESOLUTION = (
    0.0078125  # Resolution of the device, found on (page 1 of datasheet)
)

_CONTINUOUS_CONVERSION_MODE = 0b00  # Continuous Conversion Mode
_ONE_SHOT_MODE = 0b11  # One Shot Conversion Mode
_SHUTDOWN_MODE = 0b01  # Shutdown Conversion Mode


class TMP117:
    """Library for the TI TMP117 high-accuracy temperature sensor"""

    _part_id = ROUnaryStruct(_DEVICE_ID, ">H")
    _raw_temperature = ROUnaryStruct(_TEMP_RESULT, ">h")
    _temp_high_limit = UnaryStruct(_T_HIGH_LIMIT, ">h")
    _temp_low_limit = UnaryStruct(_T_LOW_LIMIT, ">h")
    _raw_temperature_offset = UnaryStruct(_TEMP_OFFSET, ">h")

    _high_alert_triggered = ROBit(_CONFIGURATION, 15, 2, False)
    _low_alert_triggered = ROBit(_CONFIGURATION, 14, 2, False)
    _data_ready = ROBit(_CONFIGURATION, 13, 2, False)
    _eeprom_busy = ROBit(_CONFIGURATION, 12, 2, False)

    _mode = RWBits(2, _CONFIGURATION, 10, 2, False)
    """		00: Continuous conversion (CC)
          01: Shutdown (SD)
          10: Continuous conversion (CC), Same as 00 (reads back = 00)
          11: One-shot conversion (OS)
    """
    _conversion_cycle = RWBits(3, _CONFIGURATION, 7, 2, False)
    """
    CONV[2:0]	AVG[1:0] = 00	AVG[1:0] = 01	AVG[1:0] = 10	AVG[1:0] = 11
    0	1 5.5ms	  125ms	  500ms	1s
    1	  125ms	  125ms	  500ms	1s
    10	  250ms	  250ms	  500ms	1s
    11	  500ms	  500ms	  500ms	1s
    100	1s	1s	1s	1s
    101	4s	4s	4s	4s
    110	8s	8s	8s	8s
    111	16s	16s	16s	16s
    """
    _averaging = RWBits(2, _CONFIGURATION, 5, 2, False)
    """
          00: No averaging
          01: 8 Averaged conversions
          10: 32 averaged conversions
          11: 64 averaged conversions
    """
    _therm_mode_en = RWBit(_CONFIGURATION, 4, 2, False)
    _int_active_high = RWBit(_CONFIGURATION, 3, 2, False)
    _data_ready_int_en = RWBit(_CONFIGURATION, 2, 2, False)
    _soft_reset = RWBit(_CONFIGURATION, 1, 2, False)

    def __init__(self, i2c_bus, address=_I2C_ADDR):

        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        if self._part_id != _DEVICE_ID_VALUE:
            raise AttributeError("Cannot find a TMP117")

    @property
    def temperature(self):
        """The current measured temperature in degrees celcius"""
        return self._raw_temperature * _TMP117_RESOLUTION

    @property
    def temperature_offset(self):
        """User defined temperature offset to be added to measurements from `temperature`"""
        return self._raw_temperature_offset * _TMP117_RESOLUTION

    @temperature_offset.setter
    def temperature_offset(self, value):
        if value > 256 or value < -256:
            raise AttributeError("temperature_offset must be ")
        scaled_offset = int(value / _TMP117_RESOLUTION)
        self._raw_temperature_offset = scaled_offset

    @property
    def high_limit(self):
        """The high temperature limit. When the measure temperature exceeds this value TODO"""
        return self._raw_high_limit

    @high_limit.setter
    def high_limit(self, value):
        if value > 256 or value < -256:
            raise AttributeError("high_limit must be from 255 to -256")
        self._raw_high_limit = value
