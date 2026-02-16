# This script predicts the horizontal distance travelled by a projectile with the following required information.
# h : height of the end of the barrel in meters
# v0: projectile speed (from previous measurements)
#
# Measured by the board:
# th: angle of the launcher in radians measured by an accelerometer on the board
# v0: projectile speed measured at the photogates
# 
# Setup:
# Two PASCO photo gates are mounted in front of a PASCO projectile launcher. PASCO sells an adapter for this setup.
# The script times the consecutive triggering of the two gates.
# Both photo gate signals are connected to an Adafruit KB2040 pins 28(A2) and 29(A3).
# An accelerometer is connected to the board to automate the angle measurements.
# The board is mounted on top of both gates so it is tilted at the same angle as the launcher.
# When a photo gate is powered, the output is HIGH. When the gate is blocked, it reads LOW.
# When the ball passes through a gate, that gate momentarily outputs LOW, until the ball clears the gate, when the gate will return to HIGH.
# To time the duration of the projectile traveling through the gates, first save the micrsecond tick to time1 when you sense a falling edge (HIGH->LOW) on gate 1 (ball passing gate 1).
# Then save the microsecond tick to time2 when you sense a falling edge (HIGH->LOW) on gate 2 (ball passing gate 2).
# Once you have both time1 and time2 values, subtract time1 from time2 to get the duration of the ball moving between the gates.
# The distance between the gates is 10 cm based on my measurement.
# With the duration, calculate the speed of the ball, and proceed to use this speed and other information and predict the x distance.
# To restart the measurement, restart the script, or wrap the script with a while loop and set time2 to 0 after printing.

# Define constants
g=9.8	# m/s/s
d=0.1	# m Distance between photogates
h=1.17  # m Launch height
v0=4.3  # m/s Launch speed from previous measurements

# Initialize variables
time1=0
time2=0

# Import generic Python/MicroPython modules
from math import sin, cos, atan2
from time import sleep,ticks_us
# Import MicroPython-only modules
from machine import Pin, I2C
# Import compphysmp-only modules
from Driver_LiuDr_LIS3DH import LIS3DH

# Initialize hardware
CH1=Pin(6,Pin.IN)	# CH1=Pin(28,Pin.IN)	# PCB version 1.0.1 uses pin 28. PCB version 1.0.2 uses pin 6
CH2=Pin(7,Pin.IN)	# CH2=Pin(29,Pin.IN)	# PCB version 1.0.1 uses pin 29. PCB version 1.0.2 uses pin 7
i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=400000)
sleep(0.01)
lis=LIS3DH(i2c)

# Finding the average acceleration from an accelerometer that has .read_g() method. Returns average components in g. By default, average 10 readings with 0.1s delay. 
def acc_avg(acc,n=10,delay_s=0.1):
    ax_sum=0;ay_sum=0;az_sum=0
    for i in range(n):
        ax,ay,az=acc.read_g() # ret is a tuple (ax,ay,az).
        ax_sum+=ax
        ay_sum+=ay
        az_sum+=az
        sleep(delay_s)
    return ax_sum/n,ay_sum/n,az_sum/n

# Making a prediction based on known information including launch height, speed (from previous measurements), and angle (accelerometer readings)
print("Steady the launcher! Angle measurements in 3 seconds...")
sleep(3)
ax,ay,az=acc_avg(lis)
th=atan2(-ax,az)
vx=v0*cos(th)
vy=v0*sin(th)
#y=0=h+vy*tf-1/2*g*tf**2
tf=1/(-g)*(-vy-(vy**2+2*g*h)**.5)
x=tf*vx
print("Angle:", th*57.3, "Height:",h)
print("Predicted distance(m):",x)	# Print prediction.print("Launch when ready...")
print("Launch when ready...")

# Two methods to sense the photogates are included.
# Method 1: use a while loop to wait until CH1 turns LOW, save time1. Then wait until CH2 turns LOW and save time2.
# Method 2: use interrupts. Each pin has its own interrupt routine to save the tick and then disable the interrupt to prevent overwriting the tick.
# You can disable an interrupt by passing None to it: CH2.irq(None)

# Method 1: While loop. This method has the same average value as PASCO timer, with 0.06ms of variations.

while CH1.value():	# Wait for CH1 to go low
    pass
time1=ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=ticks_us()	# Get time tick once CH2 goes low

# Method 2: Using two interrupt service routines. This method consistently reports 0.3ms shorter time periods than PASCO timer.
# @micropython.native
# def CH1_h(pin):
#     global time1
#     if not time2:
#         time1=ticks_us()
#     
# @micropython.native
# def CH2_h(pin):
#     global time2
#     if not time2:
#         time2=ticks_us()
# 
# CH1.irq(CH1_h, Pin.IRQ_FALLING, hard=True)
# CH2.irq(CH2_h, Pin.IRQ_FALLING, hard=True)
# while not time2:	# If time2 reads non-zero, time2 has been obtained. Time to print the result.
#     sleep(0.1)

# Making an updated predictions based on the actual launching speed just measured.
t=(time2-time1)/1000000	# Convert us to s
v0=d/t
vx=v0*cos(th)
vy=v0*sin(th)
#y=0=h+vy*tf-1/2*g*tf**2
tf=1/(-g)*(-vy-(vy**2+2*g*h)**.5)
x=tf*vx
print("Angle:", th*57.3, "Height:",h)
print("Time:",t,"Speed:",v0)
print("Updated predicted distance(m):",x)	# Print prediction.