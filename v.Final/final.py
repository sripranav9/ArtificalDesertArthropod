# ============================================================================================
#            -- Final Project, Desert Media Art --
#                    Professor Michael Ang

# Authors             : Amy, Armaan, Injoo, Pranav
# Date Last Updated   : 26 November 2022
# Description         : Arth-E - An autonomous robot that mimics desert arthropods by 
#                       concentrating on the element of fear of human intervention using
#                       light and sound stimuli
# ============================================================================================

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
# --------------

# set the min and max threshold values of the microphone
potentiomter_threshold_min = 200.0
potentiomter_threshold_max = 700.0

#sound sensor variables
# initilialize variables to store the values in the while loop for comparison
oldSoundVal = 0
newSoundVal = 0
    # threshold = 450.0 - # this will be replaced by the potentiometer reading as the threshold

# 0 for default checking the values, once there is a difference, go to mode 1
# mode 1 - waits for sometime for the arthropod to perform the action and then go ahead for checking again
soundDiff = 0
soundMode = 0
sleepTime = 5.0  # for mode 1 - seconds to wait for

# to keep track of the sound intDiff 's initated, and skip the first value - printing first value not reqd.
count = 0

#light sensor variables
oldVal = None
newVal = None
intDiff = 0
lightThreshold = 2500

#testing time monotonic
startTime = time.monotonic()

# Main loop reads value and voltage every second and prints them out.
while True:

    # --
    # microphone
    # convert to arduino 10-bit [1024] fromhere 16-bit [65536]
    sample = microphone.value / 64

    # equate the sample to newVal to compare in further iterations
    newSoundVal = sample

    #print('The current sound value is: ', newSoundVal)
    if oldSoundVal is not None:
        soundDiff = newSoundVal - oldSoundVal

    # equating this for the next iteration
    oldSoundVal = newSoundVal

    # --
    # potentiometer
    voltage = get_voltage(potentiometer)      # store the potentiometer voltage

    # map the values from the potentiometer to
    mapped_thresholdValue = int(map_range(voltage, 0,3.1, potentiomter_threshold_min, potentiomter_threshold_max))
    #print(mapped_thresholdValue)
    newVal = photocell.value
    # volts = analog_voltage(photocell)
    # Print the values:
    # print('Photocell value: {0} voltage: {1}V'.format(newVal, volts))

    # Calculate the difference in light intensity
    if oldVal is not None:
        intDiff = newVal - oldVal
        #print(intDiff)

    # Update the latested measured value
    oldVal = newVal

    #print(mapped_thresholdValue)
    #time.sleep(0.3)
    if (count!=0) and (soundDiff > mapped_thresholdValue or soundDiff < (-mapped_thresholdValue)):
        print('hey')
        print('\nThreshold currently set at:',mapped_thresholdValue)
        print("Change in sound detected, value = ", soundDiff)
        soundMode = 1;
        print('Activated StandBy','\n')
        kit.motor2.throttle = -0.90
        kit.motor3.throttle = -0.90
        time.sleep(sleepTime) # currently 5.0
        print('Deactivated StandBy')
    else:
        soundCurrTime = time.monotonic()
        if (soundCurrTime - startTime) < 6.0:
            kit.motor2.throttle = 0.5
            kit.motor3.throttle = 0.5
            soundMode = 0
        elif ((soundCurrTime - startTime) > 6.0) and ((soundCurrTime - startTime) < 9.5 ):
            kit.motor2.throttle = 0.2
            kit.motor3.throttle = 0.2
        elif ((soundCurrTime - startTime) > 9.5) and ((soundCurrTime - startTime) < 13.0 ):
            kit.motor2.throttle = 0.0
            kit.motor3.throttle = 0.0
        elif ((soundCurrTime - startTime) > 13.0) and ((soundCurrTime - startTime) < 17.0 ):
            kit.motor2.throttle = 0.9
            kit.motor3.throttle = 0.9
        else:
            startTime = soundCurrTime #updating the value after 13.5 seconds so that it starts again
        

    # to skip the first extra value
    if (count == 0):
        count+=1;

    #LIGHT code
    # Continue if the difference is smaller than 3000

    #checking the current time
    currTime = time.monotonic()
    if ((currTime - startTime) > 1.0 ):
        if abs(intDiff) > lightThreshold:
            #mode = 1
            print("\nChange in light detected, value = ", intDiff)
            print('Activated StandBy (Mode 1)')
            kit.motor2.throttle = -0.75
            kit.motor3.throttle = -0.75
            time.sleep(sleepTime/2) #since it's taking the value twice - once for increase and another for decrease
            print('Deactivated StandBy, checking for changes in light...\n')
            startTime = currTime
        
# If the difference is larger than 3000
# Change mode, wait for 10 seconds, mode changes back to initial
        else:
            lightCurrTime = time.monotonic()
        if (lightCurrTime - startTime) < 6.0:
            kit.motor2.throttle = 0.5
            kit.motor3.throttle = 0.5
            soundMode = 0
        elif ((lightCurrTime - startTime) > 6.0) and ((lightCurrTime - startTime) < 9.5 ):
            kit.motor2.throttle = 0.2
            kit.motor3.throttle = 0.2
        elif ((lightCurrTime - startTime) > 9.5) and ((lightCurrTime - startTime) < 13.0 ):
            kit.motor2.throttle = 0.0
            kit.motor3.throttle = 0.0
        elif ((lightCurrTime - startTime) > 13.0) and ((lightCurrTime - startTime) < 17.0 ):
            kit.motor2.throttle = 0.9
            kit.motor3.throttle = 0.9
        else:
            startTime = lightCurrTime #updating the value after 13.5 seconds so that it starts again
            #time.sleep(1.0)
            #print(mode)

