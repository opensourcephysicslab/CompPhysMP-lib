'''
Dr. John Liu
This example code reads x,y,z acceleration values from LIS3DH and draws a polygon on an SH1107 128*64 OLED that are always level using the 2D coordinate rotation matrix.
2025-02-11 Original code created. Define the polygon in points, center in pt_ctr, and scale in scale. The polygon will be translated to pt_ctr and scaled.
The screen has its origin at the top left corner and y-axis pointing down. The x-axis points to the right. So you should create your polygon with the same coordinate system.
It is best to either trace a polygon on graphing paper with the same coordinate system or do it digitally however you like. 

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
# points= ((20,12),(20,-12),(-20,-12),(-20,12))	# These are the vertices of a rectangle
points=((8,15),(13.5,15),(12,12.8),(11.7,11.8),(12.3,10.3),(15,8),(9.3,6.6),(7,6.7))	# This is a 8-vertex trace of the state of Minnesota
pt_ctr=(10.3,11.8)	# Defines a center to translate
scale=6	# Defines a scale
points=[(-scale*(x-pt_ctr[0]),-scale*(y-pt_ctr[1])) for x,y in points]	# translate and scale the polygon
# Read-calculate-display loop
try:
    while(True):
        display.fill(0) # Effectively this erases the display's existing content
        ax,ay,az=lis.read_g() # ret is a tuple (ax,ay,az).
        tilt=atan2(ax,ay)
        s=sin(tilt)	# Only calculate sin and cos once and reuse the values instead of inline calculations
        c=cos(tilt)
        rot_points=[]
        for x0,y0 in points:	# Rotate each point and add to rot_points list
            x=int(x0*c-y0*s)
            y=int(x0*s+y0*c)
            rot_points.append((x,y))
        rot_points.append(rot_points[0])	# Add back the first point to make a closed shape
        last_point=None
        for x,y in rot_points:	# Draw lines between current and previous points to enclose the polygon
            if last_point is not None:	# The first point only goes into the last_point variable so a line can be drawn between the second point and the first.
                x0,y0=last_point
                display.line(64+x0,32+y0,64+x,32+y,1)
            last_point=x,y
        display.circle(64,32,2,1,f=True)	# Mark the center of the drawing for visual queue
        display.show() # Call this to actually show all the content you buffered to the display so far.
        sleep(0.05)
except KeyboardInterrupt:
    print('Exiting loop...')
finally:
    display.poweroff() # It's a good idea to turn off the display to prevent burn-ins on an OLED.
