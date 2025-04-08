# This script calculates the speed of a projectile using two photogates. It is a trimmed-down version of the script that also predicts the horizontal distance.
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
from time import sleep,ticks_us
# Import MicroPython-only modules
from machine import Pin
# Import compphysmp-only modules

# Initialize hardware
CH1=Pin(28,Pin.IN)
CH2=Pin(29,Pin.IN)

print("Launch when ready...")

# Two methods to sense the photogates are included.
# Method 1: use interrupts. Each pin has its own interrupt routine to save the tick and then disable the interrupt to prevent overwriting the tick.
# You can disable an interrupt by passing None to it: CH2.irq(None)
# Method 2: use a while loop to wait until CH1 turns LOW, save time1. Then wait until CH2 turns LOW and save time2.

# Method 1: Using two interrupt service routines. This method consistently reports 0.3ms shorter time periods than PASCO timer.
@micropython.native
def CH1_h(pin):
    global time1
    if not time2:
        time1=ticks_us()
    
@micropython.native
def CH2_h(pin):
    global time2
    if not time2:
        time2=ticks_us()

CH1.irq(CH1_h, Pin.IRQ_FALLING, hard=True)
CH2.irq(CH2_h, Pin.IRQ_FALLING, hard=True)
while not time2:	# If time2 reads non-zero, time2 has been obtained. Time to print the result.
    sleep(0.1)

# Method 2: While loop. This method has the same average value as PASCO timer, with 0.06ms of variations.
'''
while CH1.value():	# Wait for CH1 to go low
    pass
time1=ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=ticks_us()	# Get time tick once CH2 goes low
'''
# Making an updated predictions based on the actual launching speed just measured.
t=(time2-time1)/1000000
v0=d/t
print("Time:",t,"Speed:",v0)