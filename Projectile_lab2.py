# This script predicts the horizontal distance travelled by a projectile with the following information.
# h : height of the end of the barrel in meters
# th: angle of the launcher in radians.
# v0: projectile speed, calculated from photo gates.
# Setup:
# Two PASCO photo gates are mounted in front of a PASCO projectile launcher. PASCO sells an adapter for this setup.
# The script times the consecutive triggering of the two gates.
# Both photo gate signals are connected to an Adafruit KB2040 pins 0 and 1.
# When a photo gate is powered, the output is HIGH. When the gate is blocked, it reads LOW.
# When the ball passes through a gate, that gate momentarily outputs LOW, until the ball clears the gate, when the gate will return to HIGH.
# To time the duration of the projectile traveling through the gates, first save the micrsecond tick to time1 when you sense a falling edge (HIGH->LOW) on gate 1 (ball passing gate 1).
# Then save the microsecond tick to time2 when you sense a falling edge (HIGH->LOW) on gate 2 (ball passing gate 2).
# Once you have both time1 and time2 values, subtract time1 from time2 to get the duration of the ball moving between the gates.
# The distance between the gates is 10 cm based on my measurement.
# With the duration, calculate the speed of the ball, and proceed to use this speed and other information and predict the x distance.
# To restart the measurement, restart the script, or wrap the script with a while loop and set time2 to 0 after printing.
from math import sin, cos
from machine import Pin
import time
CH1=Pin(0,Pin.IN)
CH2=Pin(1,Pin.IN)
time1=0
time2=0
# Two implementations are included.
# First one is to use interrupts. Each pin has its own interrupt routine to save the tick and then disable the interrupt to prevent overwriting the tick.
# Second one is to use a simple while loop to wait until CH1 turns LOW, save time1. Then wait until CH2 turns LOW and save time2.
# You can disable an interrupt by passing None to it: CH2.irq(None)

# Using two interrupt service routines to save each microsecond tick. Based on measurements, this method consistently reports 0.3ms shorter time periods than PASCO timer.
@micropython.native
def CH1_h(pin):
    global time1
    if not time2:
        time1=time.ticks_us()
    
@micropython.native
def CH2_h(pin):
    global time2
    if not time2:
        time2=time.ticks_us()
    
CH1.irq(CH1_h, Pin.IRQ_FALLING, hard=True)
CH2.irq(CH2_h, Pin.IRQ_FALLING, hard=True)
while not time2:	# If time2 reads non-zero, time2 has been obtained. Time to print the result.
    time.sleep(0.1)

# While loop method to save the microsecond ticks. Based on measurements, this method has the same average value as PASCO timer, with 0.06ms of variations.
'''
while CH1.value():	# Wait for CH1 to go low
    pass
time1=time.ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=time.ticks_us()	# Get time tick once CH2 goes low
'''
g=9.8	# m/s/s
t=(time2-time1)/1000000
d=0.1	# Distance between gates
v0=d/t*1000
h=1.17
th=30/57.3
vx=v0*cos(th)
vy=v0*sin(th)
#y=0=h+vy*tf-1/2*g*tf**2
tf=1/(-g)*(-vy-(vy**2+2*g*h)**.5)
x=tf*vx
print("Time(s):",t, "Speed(m/s):",v0)	# Print results.
print("Predicted distance(m):",x)	# Print prediction.