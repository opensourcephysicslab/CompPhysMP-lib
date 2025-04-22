# This script calculates the speed of a projectile using two photogates. It is a trimmed-down version of the script that also predicts the horizontal distance.

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

print("Launch when ready...")

while CH1.value():	# Wait for CH1 to go low
    pass
time1=ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=ticks_us()	# Get time tick once CH2 goes low

t=(time2-time1)/1000000	# Convert us to s
v0=d/t
print("Time:",t,"Speed:",v0)
