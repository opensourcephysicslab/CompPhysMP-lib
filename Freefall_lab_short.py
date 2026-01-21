# Define constants
freq_LED=100	# Hz
duty_u16=1024	# duty has the range of 0-65535 so 1024/65536=1.56% 
# Import MicroPython-only modules
from machine import PWM
# Initialize variables
pin_LED=26 
# Initialize hardware
pwm=PWM(pin_LED,freq=freq_LED)
pwm.duty_u16(duty_u16) # Turn on LED with a 1.56% duty cycle