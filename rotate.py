import math

def rotate_about_origin(x, y, delta_theta, cy):
	#print(r)
	#theta = math.acos((((x/r)+1)%2)-1)
	#x_new = r*math.cos(theta+delta_theta)
	#y_new = r*math.sin(theta+delta_theta)
	y-=cy
	x_new = (x*math.cos(delta_theta))-(y*math.sin(delta_theta))
	y_new = (x*math.sin(delta_theta))+(y*math.cos(delta_theta))
	y_new+=cy
	return (x_new, y_new)