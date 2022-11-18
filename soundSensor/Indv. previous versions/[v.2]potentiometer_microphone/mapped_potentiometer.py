# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from analogio import AnalogIn

from adafruit_simplemath import map_range

potentiometer = AnalogIn(board.A3)  # potentiometer connected to A1, power & ground

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

threshold_min = 250.0
threshold_max = 550.0

while True:

    voltage = get_voltage(potentiometer)      # store the potentiometer voltage

    mapped_value = int(map_range(voltage, 0,3.1, threshold_min, threshold_max))
    print(mapped_value)

    time.sleep(1.0)                   # Wait a bit before checking all again
