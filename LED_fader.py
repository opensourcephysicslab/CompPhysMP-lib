'''
Dr. John Liu
This example code fades in and out the on-board LED. 

10-second demo:
NA

Parts list:
KB2040 dev board:		https://www.adafruit.com/product/5302​
USB-A to USB-C cable:	https://www.adafruit.com/product/5153

Library list:
NA

Ctrl-C to stop the program and you can still change the duty cycle using pwm.duty_u16(value) where value is within 0-65535.
'''
# Define constants
freq_LED=100	# Hz
delay_s=0.01	# delay between duty cycle changes
duty_step=100	# step size of duty cycle increase and decrease
# Import MicroPython-only modules
from machine import PWM
from time import sleep
# Initialize variables
pin_LED=26 
# Initialize hardware
pwm=PWM(pin_LED,freq=freq_LED)
while (True):
    for i in range(0,65536,duty_step):	# Fade in
        pwm.duty_u16(i) # update duty cycle
        sleep(delay_s)	# pause
    
    for i in range(0,65536,duty_step):	# Fade out
        pwm.duty_u16(65536-i) # update duty cycle
        sleep(delay_s)	# pause
