from shapely.geometry import Polygon


def cross(x, y, distance, width):
	cross = Polygon(shell=[(x - distance, y - (distance * width)),
	                       (x - distance, y + (distance * width)),
	                       (x - (distance * width), y + (distance * width)),
	                       (x - (distance * width), y + distance),
	                       (x + (distance * width), y + distance),
	                       (x + (distance * width), y + (distance * width)),
	                       (x + distance, y + (distance * width)),
	                       (x + distance, y - (distance * width)),
	                       (x + (distance * width), y - (distance * width)),
	                       (x + (distance * width), y - distance),
	                       (x - (distance * width), y - distance),
	                       (x - (distance * width), y - (distance * width))],
	                holes=None)
	return cross
