# This script calculates the speed of a projectile using two photogates. It is a trimmed-down version of the script that measures launch speed and predicts the horizontal distance.
# Setup:
# Two PASCO photo gates are mounted in front of a PASCO projectile launcher. PASCO sells an adapter for this setup.
# The script times the consecutive triggering of the two gates.
# Both photo gate signals are connected to an Adafruit KB2040 pins 28(A2) and 29(A3).
# When a photo gate is powered, the output is HIGH. When the gate is blocked, it reads LOW.
# When the ball passes through a gate, that gate momentarily outputs LOW, until the ball clears the gate, when the gate will return to HIGH.
# To time the duration of the projectile traveling through the gates, first save the micrsecond tick to time1 when you sense a falling edge (HIGH->LOW) on gate 1 (ball passing gate 1).
# Then save the microsecond tick to time2 when you sense a falling edge (HIGH->LOW) on gate 2 (ball passing gate 2).
# Once you have both time1 and time2 values, subtract time1 from time2 to get the duration of the ball moving between the gates.
# The distance between the gates is 10 cm based on my measurement.
# With the duration, calculate the speed of the ball, and proceed to use this speed and other information and predict the x distance.
# To restart the measurement, restart the script, or wrap the script with a while loop and set time2 to 0 after printing.

# Define constants
d=0.1	# m Distance between photogates

# Initialize variables
time1=0
time2=0

# Import generic Python/MicroPython modules
from time import ticks_us
# Import MicroPython-only modules
from machine import Pin
# Import compphysmp-only modules

# Initialize hardware
CH1=Pin(28,Pin.IN)
CH2=Pin(29,Pin.IN)

print("Launch when ready...")

# Two methods to sense the photogates are included in the full script. Here, only method 1 using a while loop is included.
# Method 1: use a while loop to wait until CH1 turns LOW, save time1. Then wait until CH2 turns LOW and save time2.

while CH1.value():	# Wait for CH1 to go low
    pass
time1=ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=ticks_us()	# Get time tick once CH2 goes low

t=(time2-time1)/1000000	# Convert us to s
v0=d/t
print("Time:",t,"Speed:",v0)