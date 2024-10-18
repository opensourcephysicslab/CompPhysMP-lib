"""
Dr. John Liu 2024-10-01
ADXL345 3-axis accelerometer driver for MicroPython
Fixed 100Hz +-16g full resolution mode.
To test your module, run this module by itself (such as in Thonny).
It will print out its measurements, with default 7-bit address of 0x53.
It also assumes sda=12 scl=13 on an RP2040/Adafruit RP2040 STEMMA-QT system. Make appropriate changes to the test code if you are using a different system or pins.
"""
from struct import unpack
from time import sleep

_POWER_CTL_REG_ADDR=0x2D
_POWER_CTL_MEAS=0x08
_DATA_FORMAT_REG_ADDR=0x31
_DATA_FORMAT_FULL_RES_16g=0x0B
_DATAX0_REG_ADDR=0x32
_LSB_per_g=256 # LSB per acceleration in g
_LSB_per_mss=26.1 # LSB per acceleration in m/s/s
class ADXL345:
    defaultAddr=0x53 # default 7-bit address (pull SDO/ALT to GND)
    def __init__(self,i2c,addr=defaultAddr):
        self.i2c=i2c
        self.addr=addr
        self.i2c.writeto_mem(self.addr, _POWER_CTL_REG_ADDR, bytearray([_POWER_CTL_MEAS])) # power on and start measurements.
        self.i2c.writeto_mem(self.addr, _DATA_FORMAT_REG_ADDR, bytearray([_DATA_FORMAT_FULL_RES_16g])) # full resolution mode, +-16g range
    def read(self): # Read and return a tuple of (x,y,z) in bits, each LSB=3.906mg or 256LSB/g
        data = self.i2c.readfrom_mem(self.addr,_DATAX0_REG_ADDR, 6)
        (x,y,z)=unpack('<hhh',data)
        return (x, y, z)
    
    def read_mss(self): # Returns acceleration tuple in m/s/s units.
        lsb=self.read()
        return (lsb[0]/_LSB_per_mss,lsb[1]/_LSB_per_mss,lsb[2]/_LSB_per_mss)
    def read_g(self): # Returns acceleration tuple in g.
        lsb=self.read()
        return (lsb[0]/_LSB_per_g,lsb[1]/_LSB_per_g,lsb[2]/_LSB_per_g)

if __name__ == '__main__':
    from machine import I2C, Pin
    from math import atan
    i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=100000)
    sleep(0.01)
    adxl=ADXL345(i2c)
    while(True):
        ret=adxl.read_g()
        if ret[2]!=0:
            tilt_deg=atan(ret[0]/ret[2])*57.3
        else:
            tilt_deg=90.0
        print('ax(g)={:.3f}\tay(g)={:.3f}\taz(g)={:.3f}\tx_tilt(deg)={:.1f}'.format(ret[0],ret[1],ret[2],tilt_deg))
        sleep(0.25)

