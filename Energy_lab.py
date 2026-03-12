# This script detects two HI->LO transitions on one photogate and prints out the speed
#
# Setup:
# A PASCO photo gate is placed on its tand along an air track. A glider has an attachment with two leading edges 1cm apart to trigger a gate twice so speed can be detected.
# The script times HI->LO transitions and prints them all out
# The photo gate signal is connected to an Adafruit KB2040 pin GPIO6.
# When a photo gate is powered, the output is HIGH. When the gate is blocked, it reads LOW.
# This script prints out the time ticks (us) and speed.
# To stop, ctrl-c

# Define constants
d=0.01	# m Distance between edges on the glider attachment

# Initialize variables
t1=0
t2=0
# Import generic Python/MicroPython modules
from time import ticks_us
# Import MicroPython-only modules
from machine import Pin

# Initialize hardware
CH1=Pin(6,Pin.IN)	# CH1=Pin(28,Pin.IN)	# PCB version 1.0.1 uses pin 28. PCB version 1.0.2 uses pin 6

print("Release glider when ready...")
#Gate 1
while CH1.value():	# Wait until value=LOW
    pass
t1=ticks_us()

while not CH1.value():	# Wait out the LOW period, i.e. wait until value=HIGH
    pass

while CH1.value():	# Wait until value=LOW for a second time
    pass
t2=ticks_us()

print(f"t1(us)={t1}\t t2(us)={t2}\t v(m/s)={(t2-t1)/1e6/d}")