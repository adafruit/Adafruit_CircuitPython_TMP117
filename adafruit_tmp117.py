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

import time
from collections import namedtuple
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct

from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_register.i2c_bits import RWBits, ROBits

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

AlertStatus = namedtuple("AlertStatus", ["high_alert", "low_alert"])


class TMP117:
    """Library for the TI TMP117 high-accuracy temperature sensor"""

    _part_id = ROUnaryStruct(_DEVICE_ID, ">H")
    _raw_temperature = ROUnaryStruct(_TEMP_RESULT, ">h")
    _raw_high_limit = UnaryStruct(_T_HIGH_LIMIT, ">h")
    _raw_low_limit = UnaryStruct(_T_LOW_LIMIT, ">h")
    _raw_temperature_offset = UnaryStruct(_TEMP_OFFSET, ">h")

    # these three bits will clear on read in some configurations, so we read them together
    _alert_status_data_ready = ROBits(3, _CONFIGURATION, 13, 2, False)
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
    0     15.5ms  125ms	  500ms	1s
    1	  125ms	  125ms	  500ms	1s
    10	  250ms	  250ms	  500ms	1s
    11	  500ms	  500ms	  500ms	1s
    100	1s	1s	1s	1s
    101	4s	4s	4s	4s
    110	8s	8s	8s	8s
    111	16s	16s	16s	16s

    For example a single active conversion typically takes 15.5 ms, so if the device is configured
    to report an average of eight conversions, then the active conversion time is 124 ms
    (15.5 ms × 8).
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
        # currently set when `alert_status` is read, but not exposed
        self._data_ready = None
        self.reset()
        self.initialize()

    def reset(self):
        """Reset the sensor to its unconfigured power-on state"""
        self._soft_reset = True

    def initialize(self):
        """Configure the sensor with sensible defaults. `initialize` is primarily provided to be
        called after `reset`, however it can also be used to easily set the sensor to a known
        configuration"""
        # Datasheet specifies that reset will finish in 2ms however by default the first
        # conversion will be averaged 8x and take 1s
        # TODO: sleep depending on current averaging config
        time.sleep(1)
        self._data_ready = False
        print("initialize")

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
        """The high temperature limit in degrees celcius. When the measured temperature exceeds this
        value, the `high_alert` attribute of the `alert_status` property will be True. See the
        documentation for `alert_status` for more information"""

        return self._raw_high_limit * _TMP117_RESOLUTION

    @high_limit.setter
    def high_limit(self, value):
        if value > 256 or value < -256:
            raise AttributeError("high_limit must be from 255 to -256")
        scaled_limit = int(value / _TMP117_RESOLUTION)
        self._raw_high_limit = scaled_limit

    @property
    def low_limit(self):
        """The low  temperature limit in degrees celcius. When the measured temperature goes below
        this value, the `low_alert` attribute of the `alert_status` property will be True. See the
        documentation for `alert_status` for more information"""

        return self._raw_low_limit * _TMP117_RESOLUTION

    @low_limit.setter
    def low_limit(self, value):
        if value > 256 or value < -256:
            raise AttributeError("low_limit must be from 255 to -256")
        scaled_limit = int(value / _TMP117_RESOLUTION)
        self._raw_low_limit = scaled_limit

    @property
    def alert_status(self):
        """The current triggered status of the high and low temperature alerts as a AlertStatus
        named tuple with attributes for the triggered status of each alert.

        .. code-block :: python3

        import board
        import busio
        import adafruit_tmp117
        i2c = busio.I2C(board.SCL, board.SDA)

        tmp117 = adafruit_tmp117.TMP117(i2c)

        tmp117.high_limit = 25
        tmp117.low_limit = 10

        """

        # automatically cleared on read in alert mode. In therm mode it will stay set until
        # the measured temp is below the hysteresis
        status_flags = self._alert_status_data_ready
        # 3 bits: high_alert, low_alert, data_ready
        high_alert = 0b100 & status_flags > 0
        low_alert = 0b010 & status_flags > 0
        data_ready = 0b001 & status_flags > 0
        self._data_ready = data_ready
        return AlertStatus(high_alert=high_alert, low_alert=low_alert)
