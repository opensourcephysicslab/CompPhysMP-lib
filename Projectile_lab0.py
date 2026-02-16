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
CH1=Pin(6,Pin.IN)	# CH1=Pin(28,Pin.IN)	# PCB version 1.0.1 uses pin 28. PCB version 1.0.2 uses pin 6
CH2=Pin(7,Pin.IN)	# CH2=Pin(29,Pin.IN)	# PCB version 1.0.1 uses pin 29. PCB version 1.0.2 uses pin 7

print("Launch when ready...")

while CH1.value():	# Wait for CH1 to go low
    pass
time1=ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=ticks_us()	# Get time tick once CH2 goes low

print(f"Times:{time1}, {time2}")
print(f"Speed(m/s)={d*1e6/(time2-time1)}")