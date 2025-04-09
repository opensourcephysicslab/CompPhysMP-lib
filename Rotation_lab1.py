# This script measures the angular speed of a spinning pulley with the following required information.
# spokes	: Number of spokes on the pulley
# v0: projectile speed (from previous measurements)
#
# Measured by the board:
# w1: pulley angular speed in rad/s on photogate 1
# w2: pulley angular speed in rad/s on photogate 2
#
# Setup:
# Up to two PASCO photogates and PASCO super pulleys.
# The script keeps track of the triggering of the two gates.
# Both photo gate signals are connected to an Adafruit KB2040 pins 28(A2) and 29(A3).
# After each update period, the script prints out the average angular speed for the update period (default is 1s).

# Define constants
spokes=10	# Number of spokes on the pulley

# Initialize variables
time1=0
time2=0
timestamps1=[]
timestamps2=[]
update_period_us=1000000	# us Time for updating rotational speed
update_period=1	# s Time for updating rotational speed
# Import generic Python/MicroPython modules
from math import pi
from time import sleep,ticks_us
# Import MicroPython-only modules
from machine import Pin, I2C
# Import compphysmp-only modules
# from Driver_LiuDr_LIS3DH import LIS3DH
# import sh1107

# Initialize hardware
CH1=Pin(28,Pin.IN)
CH2=Pin(29,Pin.IN)
# i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=400000)	# If using the QT connector on a KB2040
# i2c=I2C(id=1,sda=Pin(2),scl=Pin(3),freq=400000)	# If using the CompPhysMP board without QT wire or Feather 2040.
# sleep(0.01)
# lis=LIS3DH(i2c)
# display = sh1107.SH1107_I2C(128, 64, i2c, address=60, rotate=0)
# display.poweron()

print("Ready to measure angular speed (rad/s)...")

# Two methods to sense the photogates are included.
# Method 1: use interrupts. Each pin has its own interrupt routine to save the tick and then disable the interrupt to prevent overwriting the tick.
# You can disable an interrupt by passing None to it: CH2.irq(None)
# Method 2: use a while loop to wait until CH1 turns LOW, save time1. Then wait until CH2 turns LOW and save time2.

# Method 1: Using two interrupt service routines. This method consistently reports 0.3ms shorter time periods than PASCO timer.
@micropython.native
def CH1_h(pin):
    global time1, timestamps1
    if time1:
        timestamps1.append(ticks_us())
    
@micropython.native
def CH2_h(pin):
    global time2, timestamps2
    if time2:
        timestamps2.append(ticks_us())

# CH1.irq(CH1_h, Pin.IRQ_FALLING, hard=True)
# CH2.irq(CH2_h, Pin.IRQ_FALLING, hard=True)
# Initialize start time for both channels
time1=ticks_us()
time2=1

# Method 2: While loop.

CH1_old=CH1.value()
CH2_old=CH2.value()

while True:
    t=ticks_us()
    CH1_new=CH1.value()
    CH2_new=CH2.value()
    if CH1_old:
        if (not CH1_new):
            timestamps1.append(t)
    CH1_old=CH1_new
    if CH2_old:
        if (not CH2_new):
            timestamps2.append(t)
    CH2_old=CH2_new
    if ticks_us()-time1>=update_period_us:
        if len(timestamps1)>1:
            # print(len(timestamps1), timestamps1)
            w1=1000000*2*pi/spokes/((timestamps1[-1]-timestamps1[0])/(len(timestamps1)-1))
            timestamps1=[]
        else:
            w1=0

        if len(timestamps2)>1:
            # print(len(timestamps2), timestamps2)
            w2=1000000*2*pi/spokes/((timestamps2[-1]-timestamps2[0])/(len(timestamps2)-1))
            timestamps2=[]
        else:
            w2=0
        print("W1=%4.2f\tW2=%4.2f" %(w1,w2))
        time1=ticks_us()
while True:
    sleep(1)
    if len(timestamps1)>1:
        time1=0
        print(len(timestamps1))
        w1=1000000*2*pi/spokes/((timestamps1[-1]-timestamps1[0])/(len(timestamps1)-1))
        print("W1=",w1)
        timestamps1=[]
        time1=1

    if len(timestamps2)>1:
        time2=0
        print(len(timestamps2))
        w2=1000000*2*pi/spokes/((timestamps2[-1]-timestamps2[0])/(len(timestamps2)-1))
        print("W2=",w2)
        timestamps2=[]
        time2=1
    
