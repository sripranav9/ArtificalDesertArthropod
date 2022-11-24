# Write your code here :-)
from adafruit_motorkit import MotorKit
import time
import board
import analogio
from adafruit_simplemath import map_range


# ------------
# Intialize the Motors
kit = MotorKit(i2c=board.I2C())

# Initialize analog input connected to photocell.
microphone = analogio.AnalogIn(board.A5)

# Initialize potentiometer connected to A3, power & ground
potentiometer = analogio.AnalogIn(board.A3)

# Initialize light sensor connected to A1
photocell = analogio.AnalogIn(board.A1)
# ------------

# --------------
# Make a function to convert from analog value to voltage.
def analog_voltage(adc):
    return adc.value / 65535 * adc.reference_voltage

# Function to convert the potentiometer values to volts
def get_voltage(pin):
    return (pin.value * 3.3) / 65536

# Function to convert the light sensor values to volts
def analog_voltage(adc):
    return adc.value / 65535 * adc.reference_voltage
# --------------

# set the min and max threshold values of the microphone
potentiomter_threshold_min = 450.0
potentiomter_threshold_max = 800.0

# initilialize variables to store the values in the while loop for comparison
oldSoundVal = 0
newSoundVal = 0
    # threshold = 450.0 - # this will be replaced by the potentiometer reading as the threshold

# 0 for default checking the values, once there is a difference, go to mode 1
# mode 1 - waits for sometime for the arthropod to perform the action and then go ahead for checking again
#sound sensor variables
soundDiff = 0
soundMode = 0
sleepTime = 5.0  # for mode 1 - seconds to wait for

# to keep track of the intDiff 's initated, and skip the first value - printing first value not reqd.
count = 0

#light sensor variables
ambientLight = []
oldVal = None
newVal = None
intDiff = 0
mode = 0
lightThreshold = 3000;



print("runnig hehe")


# Main loop reads value and voltage every second and prints them out.
while True:


    # --
    # microphone
    # convert to arduino 10-bit [1024] fromhere 16-bit [65536]
    sample = microphone.value / 64

    # equate the sample to newVal to compare in further iterations
    newSoundVal = sample

    if oldSoundVal is not None:
        soundDiff = newSoundVal - oldSoundVal

    # equating this for the next iteration
    oldSoundVal = newSoundVal

    # --
    # potentiometer
    voltage = get_voltage(potentiometer)      # store the potentiometer voltage

    mapped_thresholdValue = int(map_range(voltage, 0,3.1, potentiomter_threshold_min, potentiomter_threshold_max))
    #print(mapped_thresholdValue)
    newVal = photocell.value
    volts = analog_voltage(photocell)
    # Print the values:
    # print('Photocell value: {0} voltage: {1}V'.format(newVal, volts))

    # Calculate the difference in light intensity
    if oldVal is not None:
        intDiff = newVal - oldVal
        #print(intDiff)

    # Update the latested measured value
    oldVal = newVal

    # Continue if the difference is smaller than 3000
    #if abs(intDiff) < 3000:
    #    kit.motor1.throttle = -0.50
    #    kit.motor3.throttle = -0.50


    # If the difference is larger than 3000
    # Change mode, wait for 10 seconds, mode changes back to initial
    #else:
    #    mode = 1
    #    print("\nChange in light detected, value = ", intDiff)
    #    print('Activated StandBy (Mode 1)')
    #    kit.motor1.throttle = 0.75
    #    kit.motor3.throttle = 0.75
    #    time.sleep(5.0)
    #    print('Deactivated StandBy, checking for changes in light...\n')
    #    mode = 0

    # check for the difference and print
    # (count!=0) - ignores the 1st change in sound since it is not predictable.
    # we check for both + and - since sound travels in a wave form (visualize the graph)
    if (count!=0) and soundDiff > mapped_thresholdValue or soundDiff < (-mapped_thresholdValue) or abs(intDiff) >= lightThreshold:
        if abs(intDiff)>= 3000:
            print("\nChange in Light detected, value = ", intDiff)
            mode = 0
        else:
            print('\nThreshold currently set at:',mapped_thresholdValue)
            print("Change in sound detected, value = ", soundDiff)
            soundMode = 1;
        print('Activated StandBy','\n')
        kit.motor1.throttle = 0.75
        kit.motor3.throttle = 0.75
        #time.sleep(5.0)
        time.sleep(sleepTime)

        print('Deactivated StandBy')
    else:
        kit.motor1.throttle = -0.5
        kit.motor3.throttle = -0.5
        #time.sleep(2)

    # this is to ensure the program continues after skipping the first intDiff value.
    if (count == 0):
        count+=1;

    # Read the light intensity and the voltage.





# Main loop reads value and voltage at every specific interval and prints it out.



#while True:
    #kit.motor1.throttle = -0.50
    #kit.motor3.throttle = -0.50
    #time.sleep(0.5)
    #kit.motor1.throttle = 0

    #time.sleep(0.5)
    #kit.motor3.throttle = 0
# Write your code here :-)
