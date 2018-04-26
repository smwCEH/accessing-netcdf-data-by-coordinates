import shapely
from shapely.geometry import Polygon

print(shapely.__version__)


thing1 = Polygon(shell=[(0, 0), (1, 0), (1, 1)], holes=None)


print(type(thing1))
print(thing1.area)
print(thing1.length)


