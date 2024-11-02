from time import sleep
from machine import ADC, Pin
adc0=ADC(Pin(29))
adc1=ADC(Pin(28))
adc2=ADC(Pin(27))
adc3=ADC(Pin(26))
u16_to_volts=3.3/65536 # Converts read_u16() into voltage in volts
while True:
    v0=adc0.read_u16()*u16_to_volts
    v1=adc1.read_u16()*u16_to_volts
    v2=adc2.read_u16()*u16_to_volts
    v3=adc3.read_u16()*u16_to_volts
    print(f'V0={v0:5.3f} V1={v1:5.3f} V2={v2:5.3f} V3={v3:5.3f} ')
    sleep(0.1)