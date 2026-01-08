'''
Dr. John Liu
This example code reads and prints x,y,z acceleration values and an x-axis tilt angle in the console.
2026-01-07 Simplified the LIS3DH_SH1107_display code to only print to console.

Parts list:
Breadboard:				https://www.adafruit.com/product/239
KB2040 dev board:		https://www.adafruit.com/product/5302​
USB-A to USB-C cable:	https://www.adafruit.com/product/5153
LIS3DH accelerometer:	https://www.adafruit.com/product/2809​
Other compatible accelerometers:
ADXL343				:	https://www.adafruit.com/product/4097
ADXL345				:	https://www.adafruit.com/product/1231

Library list:
Driver_LiuDr_LIS3DH:	copy Driver_LiuDr_LIS3DH.py to /lib folder. This works with LIS3DH.
Driver_LiuDr_ADXL345:	copy Driver_LiuDr_ADXL345.py to /lib folder. This works with ADXL343 and ADXL345.

Ctrl-C to stop the program and start exploring the accelerometer on your own (fun)!
Once the code stops, you can manually read the accelerometer with lis.read_g() for (ax,ay,az) in units of g, or lis.read_mss() for (ax,ay,az) in units of m/s/s.
You can also calculate x-direction tilt angles with atan(ax/az) or other tilt angles.
'''
# Load libraries
from machine import I2C, Pin
from math import atan2
from time import sleep
from Driver_LiuDr_LIS3DH import LIS3DH
from Driver_LiuDr_ADXL345 import ADXL345

# Initialize hardware
# i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=400000) # Using STEMMA QT connector on KB2040
i2c=I2C(id=1,sda=Pin(2),scl=Pin(3),freq=400000) # Using CompPhysMP board or STEMMA QT connector on RP2040
sleep(0.01)
#sensor=LIS3DH(i2c)
sensor=ADXL345(i2c)

# Read-calculate-display loop
try:
    while(True):
        ax,ay,az=sensor.read_g() # ret is a tuple (ax,ay,az).
        tilt_deg=atan2(ax,az)*57.3
        print(f'ax={ax:.3f}g\tay={ay:.3f}g\taz={az:.3f}g\ttilt={-tilt_deg:.1f}deg')
        sleep(0.1)
except KeyboardInterrupt:
    print('Exiting loop...')
