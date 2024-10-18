"""
Dr. John Liu 2024-10-06
BMP085/BMP180 temperature and pressure sensor driver for MicroPython
To test your BMP085 module, run this module by itself (such as in Thonny).
It will print out temperature and pressure, with default 7-bit address of 0x77.
It also assumes sda=12 scl=13 on an RP2040/Adafruit RP2040 STEMMA-QT system. Make appropriate changes to the test code if you are using a different system or pins.
2024-10-06 Updated with readfrom_mem() and tested with BMP180.
2024-09-30 Initial development for BMP085
"""
import struct
from time import sleep
_EEPROM_DATA_REG_ADDR = 0xAA
_TEMP_PRES_REG_ADDR = 0xF6 # 0xF7, and for high-res pressure 0xF8
class BMP085:
    defaultAddr=0x77 # default 7-bit address
    def __init__(self,i2c,addr=defaultAddr):
        self.i2c=i2c
        self.addr=addr
        #self.i2c.writeto(self.addr,b'\xAA') # Read calibration data (write EEPROM register address)
        cal=self.i2c.readfrom_mem(self.addr,_EEPROM_DATA_REG_ADDR,22) # Read calibration data (read 22 bytes of 11 16-bit integers)
        if cal:
            (self.AC1,self.AC2,self.AC3,self.AC4,self.AC5,self.AC6,self.B1,self.B2,self.MB,self.MC,self.MD)=struct.unpack('>hhhHHHhhhhh',cal) # Unpack data into short (h) and unsigned short (H) integers
            self.oss=3
            self.inited=True
        else:
            self.inited=False
    def read(self): # Block-read temperature and pressure. Return a tuple of (TC,p) in (DegC, Pa).
        self.i2c.writeto(self.addr,b'\xF4\x2E') # Read uncalibrated temperature (write to command register 0xF4, data 0x2E i.e. read temperature command.
        sleep(0.01) # 4.5ms conversion time
        #self.i2c.writeto(self.addr,b'\xF6')	# Read uncalibrated temperature (read from register 0xF6 (and 0xF7)
        UT=struct.unpack('>h',self.i2c.readfrom_mem(self.addr,_TEMP_PRES_REG_ADDR,2))[0] # Read uncalibrated temperature (2 bytes of data from registers 0xF6 and 0xF7) and unpack into integer UT
        X1=(UT-self.AC6)*self.AC5/32768 # Calculate temperature step 1/4
        X2=self.MC*2048/(X1+self.MD)
        B5=X1+X2
        TC=(B5+8)/16/10 #  # Calculate temperature step 4/4. Temperature in DegC

        sleep(0.01)
        #i2c.writeto(0x77,b'\xF4\x34') # Read uncalibrated pressure (write to command register 0xF4, data 0x34 i.e. read pressure command.
        self.i2c.writeto(self.addr,b'\xF4\xF4') # Read uncalibrated pressure (write to command register 0xF4, data 0xC0+0x34=0xF4 i.e. read pressure command with over sampling of 3.
        sleep(0.03) # 25.5ms conversion time for oss=3.
        #self.i2c.writeto(self.addr,b'\xF6')	# Read uncalibrated pressure (read from register 0xF6 (0xF7 and 0xF8)
        u=self.i2c.readfrom_mem(self.addr,_TEMP_PRES_REG_ADDR,3)	# Read uncalibrated pressure (3 bytes of data from registers 0xF6, 0xF7, and 0xF8)
        uu=b'\x00'+u # Pad with leading zero for big-endian value
        UP=struct.unpack('>i',uu)[0]>>(8-self.oss) # Unpack the uncalibrated pressure value
        B6=B5-4000 # Calculate pressure step 1/15
        X1=(self.B2*(B6*B6/4096))/2048
        X2=self.AC2*B6/2048
        X3=X1+X2
        B3=(((self.AC1*4+int(X3))<<self.oss)+2)/4
        X1=self.AC3*B6/8192
        X2=(self.B1*(B6*B6/4096))/65536
        X3=((X1+X2)+2)/4
        B4=self.AC4*(X3+32768)/32768
        B7=(UP-B3)*(50000>>self.oss)
        if (B7<0x80000000):
            p=(B7*2)/B4
        else:
            p=(B7/B4)*2
        X1=(p//256)**2
        X1=(X1*3038)//65536
        X2=(-7357*p)//65536
        p=p+(X1+X2+3791)//16 # Calculate pressure step 15/15
        return (TC,p)

if __name__ == '__main__':
    from machine import I2C, Pin
    i2c=I2C(id=0,sda=Pin(12),scl=Pin(13),freq=100000)
    sleep(0.01)
    bmp=BMP085(i2c)
    while(True):
        ret=bmp.read()
        print('T(DegC)={:.2f}\tP(Pa)={:.0f}'.format(ret[0],ret[1]))
        sleep(0.25)
