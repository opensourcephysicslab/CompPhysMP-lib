'''
Dr. John Liu
This example code reads and prints x,y,z acceleration values and an x-axis tilt angle in the console and displays the tilt angle on an SH1107 128*64 OLED.
2024-10-17 Original code created
2025-02-10 Updated the code to unpack returned acceleration tuple instead of using a list like an old C programmer! Also using atan2() instead of atan() to extend returned angle to full circle.

Parts list:
Breadboard:				https://www.adafruit.com/product/239
KB2040 dev board:		https://www.adafruit.com/product/5302​
LIS3DH accelerometer:	https://www.adafruit.com/product/2809​
128*64 OLED:			https://www.adafruit.com/product/4650​
QT cable (2 pcs):		https://www.adafruit.com/product/4399
USB-A to USB-C cable:	https://www.adafruit.com/product/5153
Battery pack:			https://www.amazon.com/dp/B01M7Z9Z1N/

Library list:
SH1107:					copy sh1107.py to /lib folder
framebuf2:				copy framebuf2.py to /lib folder
Driver_LiuDr_LIS3DH:	copy Driver_LiuDr_LIS3DH.py to /lib folder

Ctrl-C to stop the program and start exploring the accelerometer on your own (fun)!
Once the code stops, you can manually read the accelerometer with lis.read_g() for (ax,ay,az) in units of g, or lis.read_mss() for (ax,ay,az) in units of m/s/s.
You can also calculate x-direction tilt angles with atan(ax/az) or other tilt angles.
To display on the OLED again, do display.poweron(), do some display.text() and then display.show(). Read the code for how to display texts.
Remember not to keep the display on unnecessarily to prevent burn-ins :)
'''
# Load libraries
from machine import I2C, Pin
from math import atan2
from time import sleep
from Driver_LiuDr_LIS3DH import LIS3DH
import sh1107

# Initialize hardware
i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=400000)
sleep(0.01)
lis=LIS3DH(i2c)
display = sh1107.SH1107_I2C(128, 64, i2c, address=60, rotate=0)
display.poweron()

# Read-calculate-display loop
try:
    while(True):
        ax,ay,az=lis.read_g() # ret is a tuple (ax,ay,az).
        if (ax**2+ay**2+az**2)**.5<0.25: # In case the set up is dropped accidentally (magnitude of total acceleration is small), display a surprised smily :o on the OLED.
            display.fill(1) # Fill with color
            display.large_text('Free!',0,0,3,0) # (text,x,y,font size, color)
            display.large_text('!Fall',0,32,3,0)
            sleep(2) # Otherwise people can't see the printout!
        else:
            tilt_deg=atan2(ax,az)*57.3
            outStr='ax={:.2f}g\tay={:.2f}g\taz={:.2f}g\ttilt={:.1f}deg'.format(ax,ay,az,-tilt_deg)
            print(outStr)
            display.fill(0) # Effectively this erases the display's existing content
            #display.text('Accelerometer', 0, 0, 1) # These commented lines print full details on the OLED for those who want everything on screen. text(text,x,y,color)
            #display.text('Demonstration', 0, 8, 1)
            #display.text('ax={:.2f}g'.format(ax),0,16,1)
            #display.text('ay={:.2f}g'.format(ay),0,24,1)
            #display.text('az={:.2f}g'.format(az),0,32,1)
            #display.large_text('x tilt',0,0,2,1)
            display.large_text('{:3d}'.format(-int(tilt_deg+0.5)),0,8,4,1) # Uncommented lines will display angle in very large font for easy reading
            display.large_text('Deg',40,48,2) # And as a physicist we need units, always!
        display.show() # Call this to actually show all the content you buffered to the display so far.
        sleep(0.1)
except KeyboardInterrupt:
    print('Exiting loop...')
finally:
    display.poweroff() # It's a good idea to turn off the display to prevent burn-ins on an OLED.


