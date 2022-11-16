from adafruit_motorkit import MotorKit
import time
import board
import analogio

kit = MotorKit(i2c=board.I2C())
# Initialize analog input connected to photocell.
photocell = analogio.AnalogIn(board.A1)

# Make a function to convert from analog value to voltage.
def analog_voltage(adc):
    return adc.value / 65535 * adc.reference_voltage

ambientLight = []
oldVal = None
newVal = None
intDiff = 0
mode = 0

# Main loop reads value and voltage every second and prints them out.
while True:
    # Read the light intensity and the voltage.
    newVal = photocell.value
    volts = analog_voltage(photocell)
    # Print the values:
    print('Photocell value: {0} voltage: {1}V'.format(newVal, volts))

    # Calculate the difference in intensity
    if oldVal is not None:
        intDiff = newVal - oldVal
        print(intDiff)

    # Update the latested measured value
    oldVal = newVal

    # Continue if the difference is smaller than 3000
    if abs(intDiff) <3000:
        print(mode)
        kit.motor1.throttle = -0.50
        kit.motor3.throttle = -0.50
        time.sleep(2.0)


    # If the difference is larger than 3000
    # Change mode, wait for 10 seconds, mode changes back to initial
    else:
        mode = 1
        print(mode)
        kit.motor1.throttle = 0.75
        kit.motor3.throttle = 0.75
        time.sleep(5.0)
        mode = 0
print("runnig hehe")

#while True:
    #kit.motor1.throttle = -0.50
    #kit.motor3.throttle = -0.50
    #time.sleep(0.5)
    #kit.motor1.throttle = 0

    #time.sleep(0.5)
    #kit.motor3.throttle = 0
# Write your code here :-)
