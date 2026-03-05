# Define constants
freq_LED=50	# Hz
duty_0deg=2150
duty_90deg=5433
def angle_to_duty(angle_deg):
    return int(angle_deg/90*(5433-2150)+2150) 
# Import MicroPython-only modules
from machine import PWM
# Initialize variables
pin_LED=0 
# Initialize hardware
pwm=PWM(pin_LED,freq=freq_LED)
pwm.duty_u16(angle_to_duty(90)) # Set the servo to point the laser straight down to avoid hitting the table.