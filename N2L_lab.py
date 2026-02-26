# This script detects two HI->LO transitions and prints out the time stamps
#
# Setup:
# Two PASCO photo gates are placed on their stands along an air track. A glider has an attachment with two leading edges 1cm apart to trigger a gate twice so speed can be detected.
# The script times HI->LO transitions and prints them all out
# Both photo gate signals are connected to an Adafruit KB2040 pins GPIO6 and GPIO7.
# When a photo gate is powered, the output is HIGH. When the gate is blocked, it reads LOW.
# This script prints out the time ticks (us), calculated speeds, time, and acceleration.
# To stop, ctrl-c
#
# __        __      |---1cm---|
#|  |      |  |      ___       ___ 
#|  |      |  |     |   |     |   |
#|G2|      |G1| <<< | A |     | B |      Stations facing away from the white board
#|  |      |  | ____|   |_____|   |____
#|  |      |  ||        Glider         |
#|__|______|__||_______________________|

#         |---1cm---|      __        __
#      ___       ___      |  |      |  |
#     |   |     |   |     |  |      |  |
#     | A |     | B | >>> |G1|      |G2| Stations facing the white board
# ____|   |_____|   |____ |  |      |  |
#|        Glider         ||  |      |  |
#|_______________________||__|______|__|

# Define constants
d=0.01	# m Distance between edges on the glider attachment

# Initialize variables
t1=0;t2=0;t3=0;t4=0

# Import generic Python/MicroPython modules
from time import ticks_us
from machine import Pin

# Import compphysmp-only modules

# Initialize hardware
CH1=Pin(6,Pin.IN)	# CH1=Pin(28,Pin.IN)	# PCB version 1.0.1 uses pin 28. PCB version 1.0.2 uses pin 6
CH2=Pin(7,Pin.IN)	# CH2=Pin(29,Pin.IN)	# PCB version 1.0.1 uses pin 29. PCB version 1.0.2 uses pin 7

print("Release glider when ready...")

#Gate 1
while CH1.value():	# Gate 1 reads HIGH when nothing is blocking it. Wait until value=LOW, i.e. glider attachment entering the gate
    pass
t1=ticks_us()

while not CH1.value():	# Now that the glider attachment enters the gate, the gate reads LOW until tooth B passes through the gate. Wait out the LOW period, i.e. wait until value=HIGH
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

# Calculate values and print out
v12=d/(t2-t1)*1e6
v34=d/(t4-t3)*1e6
del_t=((t4+t3)/2-(t2+t1)/2)/1e6
a=(v34-v12)/del_t
print(f"t1(us)={t1}\t t2(us)={t2}\t t3(us)={t3}\t t4(us)={t4}")
print(f"v12(m/s)={v12}\t v34(m/s)={v34}\t del_t(s)={del_t}\t a(m/s/s)={a}")