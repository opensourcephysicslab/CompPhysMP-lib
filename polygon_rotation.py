'''
Dr. John Liu
The basics of polygon rotation featured in the LIS3DH_SH1107_display_ploygon.py and demo videos
You can run this snippet in PC python environment without any electronics.

10-second demos:
https://youtube.com/shorts/5CKIizC1Buo?feature=share
https://youtu.be/bdLr1pY41OM
'''
from math import sin,cos,tan,atan,atan2
# Define a set of points as the polygon's vertices.
points=((8,15),(13.5,15),(12,12.8),(11.7,11.8),(12.3,10.3),(15,8),(9.3,6.6),(7,6.7))	# This is a 8-vertex trace of the state of Minnesota
# Define a center to rotate around
pt_ctr=(10.3,11.8)
# Define a scale to magnify the image because the screen has 128*32 pixels while the graph paper has 15cm*25cm grid.
scale=6
# translate and scale the polygon using list comprehension.
points=[(-scale*(x-pt_ctr[0]),-scale*(y-pt_ctr[1])) for x,y in points]
# Define an angle to rotate the polygon
angle=10/57.3# Example angle to rotate
s=sin(angle)	# Only calculate sin and cos once and reuse the values instead of inline calculations
c=cos(angle)
# Rotate the polygon by rotating each point by the angle and make a new list using list comprehension. Round to integer for display coordinates.
rot_points=[(int(x*c-y*s+0.5),int(x*s+y*c+0.5)) for x,y in points]