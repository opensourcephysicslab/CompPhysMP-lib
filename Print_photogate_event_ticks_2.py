# This script prints out the time tick (us) when either gate is triggered (HIGH->LOW transition).
# To stop, ctrl-c

# Define constants
d=0.1	# m Distance between photogates
trial_duration_us=15e6	# Duration
# Initialize variables
time1=0
time2=0

# Import generic Python/MicroPython modules
from time import ticks_us
# Import MicroPython-only modules
from machine import Pin

# Initialize hardware
CH1=Pin(6,Pin.IN)	# CH1=Pin(28,Pin.IN)	# PCB version 1.0.1 uses pin 28. PCB version 1.0.2 uses pin 6
CH2=Pin(7,Pin.IN)	# CH2=Pin(29,Pin.IN)	# PCB version 1.0.1 uses pin 29. PCB version 1.0.2 uses pin 7

print("Start rotation when ready...")

# Store old and new values
CH1_old=CH1.value()
CH2_old=CH2.value()
CH1_new=CH1_old
CH2_new=CH2_old
results=""
start=0
while True:
    CH1_new=CH1.value()	# Always update new values at the beginning of each iteration
    CH2_new=CH2.value()
    if (not CH1_new) and CH1_old:
        time1=ticks_us()
        results+="1:\t%d\n" %time1
        if start==0:
            start=time1
    if (not CH2_new) and CH2_old:
        time2=ticks_us()
        results+="2:\t%d\n" %time2
        if start==0:
            start=time2
    CH1_old=CH1_new	# Always update old values with the new values at the end of each iteration
    CH2_old=CH2_new
    if start and ticks_us()-start>trial_duration_us:
        break
print(results)