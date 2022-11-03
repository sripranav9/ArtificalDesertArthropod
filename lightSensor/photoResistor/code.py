import time

import board
import analogio


# Initialize analog input connected to photocell.
photocell = analogio.AnalogIn(board.A1)

# Make a function to convert from analog value to voltage.
def analog_voltage(adc):
    return adc.value / 65535 * adc.reference_voltage

ambientLight = []
oldVal = 0
newVal = 0

# Main loop reads value and voltage every second and prints them out.
while True:
    # Read the light intensity and the voltage.
    newVal = photocell.value
    volts = analog_voltage(photocell)
    # Print the values:
    print('Photocell value: {0} voltage: {1}V'.format(newVal, volts))
    # Calculate the difference in intensity
    if oldVal is not None:
        intDifference = newVal - oldVal
    print(intDifference)
    # Update the latest measured intensity
    oldVal = newVal
    # Wait for five seconds to repeat
    time.sleep(5.0)
