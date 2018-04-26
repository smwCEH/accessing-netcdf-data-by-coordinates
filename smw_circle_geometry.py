from shapely.geometry import Point


def circle(x, y, radius):
	p = Point(x, y)
	circle = p.buffer(radius)
	return circle