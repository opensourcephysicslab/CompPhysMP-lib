#points=((5,5),(10,5),(16,4),(21,7),(15,12),(4,8))	# This is a trace of a dinasaur head
#pt_ctr=(12,7)	# Defines a center to translate
#scale=6	# Defines a scale
#points=[(-scale*(x-pt_ctr[0]),-scale*(y-pt_ctr[1])) for x,y in points]	# translate and scale the polygon

points=((6,10),(6,18),(9,18),(14,18),(14,12),(14,8),(9,8),(6,10),(9,12),(14,12),(14,18),(9,18),(9,12),(9,8))	# This is a trace of a house
pt_ctr=(11,13)	# Defines a center to translate
scale=6	# Defines a scale
points=[(-scale*(x-pt_ctr[0]),-scale*(y-pt_ctr[1])) for x,y in points]	# translate and scale the polygon
points=[(y,x) for x,y in points] # This image was read out sideways so need rotation by 90 degrees and flipped left-right.
