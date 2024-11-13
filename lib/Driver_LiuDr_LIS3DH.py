"""
Dr. John Liu 2024-11-13
LIS3DH 3-axis accelerometer driver for MicroPython
Fixed 400Hz +-2g mode
LIS3DH(i2c) uses default address while LIS3DH(i2c,False) uses alternate address
To test your module, run this module by itself (such as in Thonny).
It will print out its measurements, with default 7-bit address of 0x18.
The sample code assumes sda=12 scl=13 on an Adafruit KB2040 board STEMMA-QT connector. Make appropriate changes to the test code if you are using a different system or pins.
"""
from struct import unpack
from time import sleep

_REG_TEMPCFG_ADDR=0x1F
_TEMP_EN=0x80
_REG1_ADDR=0x20
_400Hz_xyz=0x77
_REG4_ADDR=0x23
_BDU_2g_HR=0x88
_REG5_ADDR=0x24
_FIFO_EN=0x80
_LIR_INT1=0x08
_OUT_X_L_REG_ADDR=0x28

_DATA_FORMAT_REG_ADDR=0x31
_DATA_FORMAT_FULL_RES_16g=0x0B
_LSB_per_g_2g=16380 # LSB per acceleration in g in +-2g range and high resolution
_LSB_per_mss_2g=1669.7 # LSB per acceleration in m/s/s in +-2g range and high resolution
class LIS3DH:
    defaultAddr=0x18 # default 7-bit address (pull SDO/SA0 to GND)
    alternateAddr=0x19 # alternate 7-bit address (pull SDO/SA0 to VCC or leave unconnected)
    def __init__(self,i2c,useDefaultAddr=True):
        self.i2c=i2c
        self.addr=LIS3DH.defaultAddr if useDefaultAddr else LIS3DH.alternateAddr
        self.i2c.writeto_mem(self.addr, _REG5_ADDR, bytearray([_FIFO_EN])) # Enable FIFO
        self.i2c.writeto_mem(self.addr, _REG1_ADDR, bytearray([_400Hz_xyz])) # Enable x,y,z and set 400Hz
        self.i2c.writeto_mem(self.addr, _REG4_ADDR, bytearray([_BDU_2g_HR])) # Enable block data update, +-2g, and high resolution
        self.i2c.writeto_mem(self.addr, _REG_TEMPCFG_ADDR, bytearray([_TEMP_EN])) # Enable temperature sensor
        self.i2c.writeto_mem(self.addr, _REG5_ADDR, bytearray([_LIR_INT1])) # Latch interrupt request on INT1_SRC.
        
    def read(self): # Read and return a tuple of (x,y,z) in bits
        data = self.i2c.readfrom_mem(self.addr,(_OUT_X_L_REG_ADDR| 0x80), 6) # For LIS3DH, to read multiple registers, the register address must have its MSB set (REG_ADDR|0x80) otherwise the same register is read multiple times. This is not what "memory device" is expected to behave.
        x, y, z = unpack('<hhh', data)
        return (x, y, z)
    
    def read_mss(self): # Returns acceleration tuple in m/s/s units.
        lsb=self.read()
        return (lsb[0]/_LSB_per_mss_2g,lsb[1]/_LSB_per_mss_2g,lsb[2]/_LSB_per_mss_2g)
    def read_g(self): # Returns acceleration tuple in g.
        lsb=self.read()
        return (lsb[0]/_LSB_per_g_2g,lsb[1]/_LSB_per_g_2g,lsb[2]/_LSB_per_g_2g)

if __name__ == '__main__':
    from machine import I2C, Pin
    from math import atan
    i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=100000) # Adafruit KB2040 board STEMMA-QT connector # i2c=I2C(id=1,sda=Pin(2),scl=Pin(3),freq=100000) # Adafruit Feather RP2040 board STEMMA-QT connector
    sleep(0.01)
    lis=LIS3DH(i2c)
    while(True):
        ret=lis.read_g()
        if ret[2]!=0:
            tilt_deg=atan(ret[0]/ret[2])*57.3
        else:
            tilt_deg=90.0
        print('ax(g)={:.3f}\tay(g)={:.3f}\taz(g)={:.3f}\tx_tilt(deg)={:.1f}'.format(ret[0],ret[1],ret[2],tilt_deg))
        sleep(0.25)


