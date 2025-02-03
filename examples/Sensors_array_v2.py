import os
os.environ['BLINKA_FT232H'] = "1"
import board
from adafruit_tmp11X import TMP117, TMP116, TMP119, AverageCount, MeasurementMode, MeasurementDelay, Symbols
import time
import datetime
import Logging_class
global sensors







# add  to this array multiple sensors.
# address limitation for single device allow to add up to 4 devises
# However you may add different I2C busses to array



def get_temperature(ret_as="array"):

    for i in range(10):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        t1 = TMP117(i2c_bus=i2c, address=0x48)
        t2 = TMP117(i2c_bus=i2c, address=0x49)
        t3 = TMP117(i2c_bus=i2c, address=0x4a)
        t4 = TMP117(i2c_bus=i2c, address=0x4b)
        sensors = [t1, t2, t3, t4]
        # print(AverageCount.AVERAGE_32X)

        for sensor in sensors:
            sensor.measurement_mode = MeasurementMode.CONTINUOUS
            sensor.averaged_measurements = AverageCount.AVERAGE_8X
            sensor.measurement_delay = MeasurementDelay.DELAY_0_0015_S

        try:
            temp_array = []
            temp_dict = {}
            for sensor in sensors:
                temp_array.append(sensor.temperature_updated)
            if ret_as == "arrya":
                return temp_array
            else:
                for i, item in enumerate(temp_array):
                    key = f"T{i}"
                    temp_dict[key] = item
                i2c.deinit()
                return temp_dict
        except Exception as e:
            print(f"query[{i}]: Error: {e}")





def get_csv_keys():
    keys = []
    for i in range(4):
        keys.append(f"T{i}")
    return keys

if __name__ == "__main__":
    logger = Logging_class.txt_logger()
    logger.init("temperature_TMP117")

    while True:

        txt = f"{get_temperature('dict')} {Symbols.degC}  "
        logger.print_and_log(txt)
        time.sleep(2)