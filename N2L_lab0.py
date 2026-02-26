# This script detects two HI->LO transitions and prints out the time stamps
#
# Setup:
# Two PASCO photo gates are placed on their stands along an air track. A glider has an attachment with two leading edges 1cm apart to trigger a gate twice so speed can be detected.
# The script times HI->LO transitions and prints them all out
# Both photo gate signals are connected to an Adafruit KB2040 pins GPIO6 and GPIO7.
# When a photo gate is powered, the output is HIGH. When the gate is blocked, it reads LOW.
# This script prints out the time tick (us) when either gate is triggered (HIGH->LOW transition).
# To stop, ctrl-c

# Define constants
d=0.01	# m Distance between edges on the glider attachment

# Initialize variables
t1=0
t2=0
t3=0
t4=0
# Import generic Python/MicroPython modules
from time import ticks_us
# Import MicroPython-only modules
from machine import Pin

# Initialize hardware
CH1=Pin(6,Pin.IN)	# CH1=Pin(28,Pin.IN)	# PCB version 1.0.1 uses pin 28. PCB version 1.0.2 uses pin 6
CH2=Pin(7,Pin.IN)	# CH2=Pin(29,Pin.IN)	# PCB version 1.0.1 uses pin 29. PCB version 1.0.2 uses pin 7

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

# Gate 2
while CH2.value():	# Wait until value=LOW
    pass
t3=ticks_us()

while not CH2.value():	# Wait out the LOW period, i.e. wait until value=HIGH
    pass

while CH2.value():	# Wait until value=LOW for a second time
    pass
t4=ticks_us()
print(f"t1(us)={t1}\t t2(us)={t2}\t t3(us)={t3}\t t4(us)={t4}")