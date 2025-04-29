from ads1x15 import *
from machine import Pin, I2C
from time import sleep
ADS1115_ADDR = 72
i2c = I2C(id=0,scl=Pin(13), sda=Pin(12), freq=400000)
ads = ADS1115(i2c, ADS1115_ADDR, 0)
while True:
    for ch in range(0,4):
        print(ads.auto(ch))
    sleep(0.25)
    print("----------")
