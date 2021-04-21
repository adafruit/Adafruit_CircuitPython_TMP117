Simple test
------------

Ensure your device works with this simple test.

.. literalinclude:: ../examples/tmp117_simpletest.py
    :caption: examples/tmp117_simpletest.py
    :linenos:

Temperature limits and alerts
-----------------------------

Set high and low temperature limits and be alerted when they are surpassed.

.. literalinclude:: ../examples/tmp117_limits_test.py
    :caption: examples/tmp117_limits_test.py
    :linenos:

Measurement averaging and rate
------------------------------

Adjust the number of samples averaged for every reported temperature, and adjust the time beween new
measurement reports

.. literalinclude:: ../examples/tmp117_rate_and_averaging_test.py
    :caption: examples/tmp117_rate_and_averaging_test.py
    :linenos:

Temperature offset
------------------

Set an offset that will be applied to each measurement, to account for measurement biases in the
sensor's environment

.. literalinclude:: ../examples/tmp117_offset_test.py
    :caption: examples/tmp117_offset_test.py
    :linenos:

Single Measurement Test
-----------------------

Take different sample number and average to give a single temperature measure

.. literalinclude:: ../examples/tmp117_single_measurement_test.py
    :caption: examples/tmp117_single_measurement_test.py
    :linenos:
