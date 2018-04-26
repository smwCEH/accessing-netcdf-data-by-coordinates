from shapely.geometry import Polygon


def diagonal_cross(x, y, distance, width):
	diagonal_cross = Polygon(shell=[(x - distance, y - distance + (distance * width)),
	                                (x - (distance * width), y),
	                                (x - distance, y + distance - (distance * width)),
	                                (x - distance, y + distance),
	                                (x - distance + (distance * width), y + distance),
	                                (x, y + (distance * width)),
	                                (x + distance - (distance * width), y + distance),
	                                (x + distance, y + distance),
	                                (x + distance, y + distance - (distance * width)),
	                                (x + (distance * width), y),
	                                (x + distance, y - distance + (distance * width)),
	                                (x + distance, y - distance),
	                                (x + distance - (distance * width), y - distance),
	                                (x, y - (distance * width)),
	                                (x - distance + (distance * width), y - distance),
	                                (x - distance, y - distance)],
	                         holes=None)
	return diagonal_cross
