'''
Dr. John Liu
This example code reads x,y,z acceleration values from LIS3DH and draws two rectangles on an SH1107 128*64 OLED that are always level using the 2D coordinate rotation matrix.
2025-02-10 Original code created. See full version with file name without the "slow". This trimmed-down version is supposed to be slower because it requires sine and cosine calculations but I guess the fast processor and slow display makes it hard to discern speed.

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
You can also calculate x-direction tilt angles with atan(ax/az) or atan2(ax,az).
To display on the OLED again, do display.poweron(), do some display.text() and then display.show(). Read the code for how to display texts.
Remember not to keep the display on unnecessarily to prevent burn-ins :)
'''
# Load libraries
from machine import I2C, Pin
from math import sin,cos,tan,atan,atan2
from time import sleep
from Driver_LiuDr_LIS3DH import LIS3DH
import sh1107

# Initialize hardware
i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=400000)
sleep(0.01)
lis=LIS3DH(i2c)
display = sh1107.SH1107_I2C(128, 64, i2c, address=60, rotate=0)
display.poweron()
l=20
w=12
# Read-calculate-display loop
try:
    while(True):
        ax,ay,az=lis.read_g() # ret is a tuple (ax,ay,az).
        tilt=atan2(ax,ay)
        s=sin(tilt)	# Only calculate sin and cos once and reuse the values instead of inline calculations
        c=cos(tilt)
        x1=int(16*c-10*s)
        y1=int(16*s+10*c)

        x2=int(-16*c-10*s)
        y2=int(-16*s+10*c)

        x3=int(16*c+10*s)
        y3=int(16*s-10*c)

        x4=int(-16*c+10*s)
        y4=int(-16*s-10*c)

        display.fill(0) # Effectively this erases the display's existing content
        display.line(64+x1,32+y1,64+x2,32+y2,1)
        display.line(64+x3,32+y3,64+x4,32+y4,1)
        display.line(64+x1,32+y1,64+x3,32+y3,1)
        display.line(64+x2,32+y2,64+x4,32+y4,1)

        display.line(64+2*x1,32+2*y1,64+2*x2,32+2*y2,1)	# A larger box just for fun
        display.line(64+2*x3,32+2*y3,64+2*x4,32+2*y4,1)
        display.line(64+2*x1,32+2*y1,64+2*x3,32+2*y3,1)
        display.line(64+2*x2,32+2*y2,64+2*x4,32+2*y4,1)
        
        display.show() # Call this to actually show all the content you buffered to the display so far.
        sleep(0.05)
except KeyboardInterrupt:
    print('Exiting loop...')
finally:
    display.poweroff() # It's a good idea to turn off the display to prevent burn-ins on an OLED.




