# This script shows how to sense a digital HIGH/LOW sensor and time two events from two digital sensors with 0.1ms accuracy.
# Two PASCO photo gates are mounted in front of a PASCO projectile launcher. PASCO sells an adapter for this setup.
# Ihe script times the consecutive triggering of the two gates, while both gates are connected to and sensed by a PASCO photo gate smart timer.
# Wires were soldered to both photo gate signals and the ground on the back of the timer's circuit board and connected to an Adafruit KB2040 pins 0, 1, and GND.
# When PASCO photo gate smart timer is set to "time:two gates" mode and armed, both gates are turned on and read HIGH.
# When the ball passes through a gate, that gate momentarily outputs LOW, until the ball passes entirell through the gate, when the gate will return to HIGH.
# I think the timer turns off both gates after it senses the second gate goes LOW, possibly to conserve battery. I saw an exponential decay of gate 2's output.
# To time the duration of the projectile, first save the micrsecond tick to time1 when you sense a falling edge (HIGH->LOW) on gate 1 (ball passing gate 1).
# Then save the microsecond tick to time2 when you sense a falling edge (HIGH->LOW) on gate 2 (ball passing gate 2).
# Once you have both time1 and time2 values, subtract time1 from time2 to get the duration of the ball moving between the gates.#
# The distance between the gates is 10 cm based on my measurement.
# With the duration, calculate the speed of the ball: 10cm/duration

from machine import Pin
import time
CH1=Pin(0,Pin.IN)
CH2=Pin(1,Pin.IN)
time1=0
time2=0
# Two implementations are included.
# First one is to use interrupts. Each pin has its own interrupt routine to save the tick and then disable the interrupt to prevent overwriting the tick.
# Second one is to use a simple while loop to wait until CH1 turns LOW, save time1. Then wait until CH2 turns LOW and save time2.
# Using two interrupt service routines to save each microsecond tick. Based on measurements, this method consistently reports 0.3ms shorter time periods than PASCO timer.
def CH1_h(pin):
    global time1
    time1=time.ticks_us()
    CH1.irq(None)	# Disable this interrupt so we can preserve this time tick and won't be overwriting it with another falling edge.
    
def CH2_h(pin):
    global time2
    time2=time.ticks_us()
    CH2.irq(None)	# Disable this interrupt so we can preserve this time tick and won't be overwriting it with another falling edge.
    
CH1.irq(CH1_h, Pin.IRQ_FALLING, hard=True)
CH2.irq(CH2_h, Pin.IRQ_FALLING, hard=True)
while not time2:	# If time2 reads non-zero, time2 has been obtained. Time to print the result.
    time.sleep(1)
print((time2-time1)/1000)	# Print time duration in milliseconds.

# While loop method to save the microsecond ticks. Based on measurements, this method has the same average value as PASCO timer, with 0.06ms of variations.
'''
while CH1.value():	# Wait for CH1 to go low
    pass
time1=time.ticks_us()	# Get time tick once CH1 goes low
while CH2.value():	# Wait for CH2 to go low
    pass
time2=time.ticks_us()	# Get time tick once CH2 goes low
print((time2-time1)/1000000)	# Print time duration in seconds.
'''
