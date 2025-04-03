# This script tests the projectile distance prediction. Make sure you have a correct formula before incorporating the formulas in your main script.
from math import sin,cos
g=9.8	# m/s/s
#t=(time2-time1)/1000000
d=0.1	# Distance between gates
#v0=d/t*1000
v0=4.6
h=1.17
th=30/57.3	# With 0 degrees, distance is about 2.2m. With 30 degrees, distance is 3.1 meters.
vx=v0*cos(th)
vy=v0*sin(th)
#y=0=h+vy*tf-1/2*g*tf**2
tf=1/(-g)*(-vy-(vy**2+2*g*h)**.5)
x=tf*vx
print("Time(s):",t, "Speed(m/s):",v0)	# Print results.
print("Predicted distance(m):",x)	# Print prediction.
print(x)