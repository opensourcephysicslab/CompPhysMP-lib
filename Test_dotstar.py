from micropython_dotstar import DotStar
from machine import SPI
from time import sleep_ms

spi = SPI(id=0, sck=18, mosi=19) # Configure SPI
dotstar = DotStar(spi, 144,auto_write=False)        # Setup one DotStar

RED =     (0x3f,0,0)
YELLOW =  (0x3f,0x3f,0)
GREEN =   (0,0x3f,0)
BLUE =    (0,0,0x3f)
BLACK =   (0,0,0)

def location2DotStar(strip, loc_m, start_m, stop_m, total_LEDs):
  pixel=0
  color=BLACK
  if (loc_m>=stop_m):
    pixel=total_LEDs-1
    color=RED
  elif (loc_m<=start_m):
    pixel=0
    color=BLUE
  else:
    pixel=int((loc_m-start_m)/(stop_m-start_m)*total_LEDs+0.5);
    color=YELLOW;
  strip.fill(BLACK)
  strip[pixel]=color
  strip.show()

location2DotStar(dotstar,1.5,1.0,1.995,144)

for i in range(900,2101):
    location2DotStar(dotstar,i/1000.0,1.0,1.995,144);
    sleep_ms(10)

#dotstar[0] = (128, 0, 0)         # Red
#dotstar[0] = (128, 0, 0, 0.5)    # Red, half brightness
#dotstar.fill((0,0,128))          # Blue