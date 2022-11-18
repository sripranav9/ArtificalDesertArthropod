# 09 November 2022
# Final Project: Artificial Desert Arthropod
# Desert Media Art
# Professor Mang
# Microphone Testing: SparkFun Electret Microphone Breakout
# **********************************************************

#import necessary modules
import time
import board
import analogio


# Initialize analog input connected to photocell.
microphone = analogio.AnalogIn(board.A0)

# variables to store the values in the while loop (comparison purposes)
oldVal = 0
newVal = 0
threshold = 150.0

# 0 for default checking the values, once there is a difference, go to mode 1
# mode 1 - waits for sometime for the arthropod to perform the action and then go ahead for checking again
mode = 0
sleepTime = 5.0  # for mode 1 - seconds to wait for

# to keep track of the intDiff 's initated, and skip the first value
count = 0

# Main loop reads value and voltage every second and prints them out.
while True:

    # convert to arduino 10-bit [1024] fromhere 16-bit [65536]
    sample = microphone.value / 64

    # equate the sample to newVal to compare in further iterations
    newVal = sample

    if oldVal is not None:
        intDiff = newVal - oldVal

    # equating this for the next iteration
    oldVal = newVal

    # check for the difference and print
    # (count!=0) - ignores the 1st change in sound since it is not predictable.
    if (count!=0) and intDiff > threshold or intDiff < (-threshold):
        print("\nchange in sound detected, value = ", intDiff)
        print('Activated StandBy (Mode 1)')
        time.sleep(sleepTime)
        mode = 1;
        print('Deactivated StandBy, checking for changes in sound')

    # this is to ensure the program continues after skipping the first intDiff value.
    if (count == 0):
        count+=1;

    #print(intDiff)
