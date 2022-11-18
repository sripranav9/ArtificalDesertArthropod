# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from analogio import AnalogIn
from adafruit_simplemath import map_range

# Initialize analog input connected to photocell.
microphone = AnalogIn(board.A0)

# Initialize potentiometer connected to A1, power & ground
potentiometer = AnalogIn(board.A3)  

# Function to convert the potentiometer values to volts
def get_voltage(pin):
    return (pin.value * 3.3) / 65536

# set the min and max threshold values of the microphone
potentiomter_threshold_min = 250.0
potentiomter_threshold_max = 550.0

# initilialize variables to store the values in the while loop for comparison
oldVal = 0
newVal = 0
    # threshold = 450.0 - # this will be replaced by the potentiometer reading as the threshold

# 0 for default checking the values, once there is a difference, go to mode 1
# mode 1 - waits for sometime for the arthropod to perform the action and then go ahead for checking again
mode = 0
sleepTime = 5.0  # for mode 1 - seconds to wait for

# to keep track of the intDiff 's initated, and skip the first value - printing first value not reqd.
count = 0

# Main loop reads value and voltage at every specific interval and prints it out.
while True:
    
    # --
    # microphone
    # convert to arduino 10-bit [1024] fromhere 16-bit [65536]
    sample = microphone.value / 64

    # equate the sample to newVal to compare in further iterations
    newVal = sample

    if oldVal is not None:
        intDiff = newVal - oldVal

    # equating this for the next iteration
    oldVal = newVal
    
    # --
    # potentiometer
    voltage = get_voltage(potentiometer)      # store the potentiometer voltage

    mapped_thresholdValue = int(map_range(voltage, 0,3.1, potentiomter_threshold_min, potentiomter_threshold_max))
    #print(mapped_thresholdValue)

    # check for the difference and print
    # (count!=0) - ignores the 1st change in sound since it is not predictable.
    # we check for both + and - since sound travels in a wave form (visualize the graph)
    if (count!=0) and intDiff > mapped_thresholdValue or intDiff < (-mapped_thresholdValue):
        print('\nThreshold currently set at:',mapped_thresholdValue)
        print("Change in sound detected, value = ", intDiff)
        print('Activated StandBy (Mode 1)\n')
        time.sleep(sleepTime)
        mode = 1;
        print('Deactivated StandBy, checking for changes in sound...')

    # this is to ensure the program continues after skipping the first intDiff value.
    if (count == 0):
        count+=1;

