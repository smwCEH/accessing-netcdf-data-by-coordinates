from shapely.geometry import Polygon


def triangle(x, y, distance):
	triangle = Polygon(shell=[(x - distance, y - distance),
	                          (x, y + distance),
	                          (x + distance, y - distance)],
	                   holes=None)  # Triangle
	return triangle
