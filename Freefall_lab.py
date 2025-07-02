# This script is for a free fall lab with flashing falling LED and a camera.
# The script flashes the LED on the computational physics MicroPython board that is on pin 26 at a frequency of 1000 Hz so when the board is dropped, the camera set to a long exposure (0.75s) will capture the blinking dots.
# freq_LED : LED flashing frequency. Our apparatus drops the board for 2m. With 1000 Hz flashing, we can get about 50 dots on the photo.
# duty_u16 : how long the LED stays on during one cycle. Range is 0 to 65536 so 1024/65536=1.56%. Longer time results in brighter image but the dots may appear elongated vertically.
#
# Measured by the board:
# The board doesn't measure anything
# 
# Setup:
# We have a 2m-tall poll at the top of which an electromagnet is mounted. A small pin sticks out of the electromagnet that can hold the board through the hole behind the USB port.
# When we energize the electromagnet, the pin is pulled into the electromagnet, thus dropping the board from free.
# Simultaneously a camera's shutter is opened for 0.75 seconds, long enough to capture the entire descent.
# The flashing LED on the board causes a periodic exposure on the camera, resulting in a series of bright dots, separated by even time.
# Students may use the 2m stick in the background (next to the pole) to find the location of dots in order to analyze the free fall motion.
# To restart the measurement, hang the board and drop it again.
# This lab requires the dual-AA battery holder. I use 

# Define constants
freq_LED=100	# Hz
duty_u16=1024	# duty has the range of 0-65535 so 1024/65536=1.56% 

pin_LED=26 # Initialize variables

from machine import PWM # Import MicroPython-only modules

pwm=PWM(pin_LED,freq=freq_LED) # Initialize hardware

pwm.duty_u16(duty_u16) # Turn on LED with a 1.56% duty cycle

print("Free fall lab with flashing LED")
print(pwm.freq()) # Return frequency # pwm.freq(1000) # Update frequency. Duty cycle will not be changed.