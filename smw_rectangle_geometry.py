from shapely.geometry import Polygon


def rectangle(x, y, length, height):
	rectangle = Polygon(shell=[(x - (length * 0.5), y - (height * 0.5)),
	                           (x - (length * 0.5), y + (height * 0.5)),
	                           (x + (length * 0.5), y + (height * 0.5)),
	                           (x + (length * 0.5), y - (height * 0.5))],
	                    holes=None)
	return rectangle