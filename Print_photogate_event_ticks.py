# This script prints out the time tick (us) when either gate is triggered (HIGH->LOW transition).
# To stop, ctrl-c

# Define constants
d=0.1	# m Distance between photogates

# Initialize variables
time1=0
time2=0

# Import generic Python/MicroPython modules
from time import ticks_us
# Import MicroPython-only modules
from machine import Pin

# Initialize hardware
CH1=Pin(28,Pin.IN)
CH2=Pin(29,Pin.IN)

print("Start rotation when ready...")

# Store old and new values
CH1_old=CH1.value()
CH2_old=CH2.value()
CH1_new=CH1_old
CH2_new=CH2_old

while True:
    CH1_new=CH1.value()	# Always update new values at the beginning of each iteration
    CH2_new=CH2.value()
    if (not CH1_new) and CH1_old:
        time1=ticks_us()
        print("1:",time1)
    if (not CH2_new) and CH2_old:
        time2=ticks_us()
        print("2:",time2)
    CH1_old=CH1_new	# Always update old values with the new values at the end of each iteration
    CH2_old=CH2_new