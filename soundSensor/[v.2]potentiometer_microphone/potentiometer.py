# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from analogio import AnalogIn

potentiometer = AnalogIn(board.A3)  # potentiometer connected to A1, power & ground

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

while True:

    print(get_voltage(potentiometer))      # Display value

    time.sleep(1.0)                   # Wait a bit before checking all again
