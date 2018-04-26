import os
import sys
import datetime
import itertools


import numpy as np
import netCDF4 as nc
import pyproj


def array_corner_values(array):
	'''
	Function to display values in the extreme corners of a multi-dimensional array.
	Works with arrays with dimensions from 1 to N

	:param array:
	:return:
	'''
	print('array_corner_values():')
	print('\tarray has {0} dimension{1}'.format(array.ndim,
	                                            '' if array.ndim == 1 else 's'))
	for coordinates in list(itertools.product([0, -1], repeat=array.ndim)):
		print('\t\tcoordinate {0:<32}:\t\t{1:>10}'.format(str(coordinates),
		                                                  array[coordinates]))


# # Test array_corner_values() function with array size of 3 and 1-5 dimensions
# size = 3
# shape_list = []
# for dimension in np.arange(1, 6):
# 	print('\n\ndimension:\t\t{0}'.format(dimension))
# 	shape_list.append(size)
# 	print(shape_list)
# 	array = np.reshape(np.arange(size ** dimension), newshape=(tuple(shape_list)))
# 	# print('array:\t\t{0}'.format(array))
# 	pprint.pprint(array)
# 	array_corner_values(array)


datetime_format = '%H:%M:%S %Y-%m-%d'


# start = datetime.datetime.now()
# print('\n\nStarted at:\t\t{0}'.format(start.strftime(datetime_format)))


northings_min = 0.0
northings_max = 1300000.0
eastings_min = 0.0
eastings_max = 700000.0


resolution = 1000.0


wgs84 = pyproj.Proj('+init=EPSG:4326')
osgb36 = pyproj.Proj('+init=EPSG:27700')


northings = np.arange(start=(northings_max - (resolution * 0.5)),
                      stop=northings_min,
                      step=-resolution,
                      dtype=np.float32)
eastings = np.arange(start=(eastings_min + (resolution * 0.5)),
                     stop=eastings_max,
                     step=resolution,
                     dtype=np.float32)


print('\n\nNested loops...')
start = datetime.datetime.now()
print('Started at:\t\t\t{0}'.format(start.strftime(datetime_format)))
latitude = np.zeros((len(northings), len(eastings)), dtype=np.float32)
longitude = np.zeros((len(northings), len(eastings)), dtype=np.float32)
# print(latitude.shape)
# print(longitude.shape)
y = 0
for northing in northings:
	x = 0
	for easting in eastings:
		# print(pyproj.transform(osgb36, wgs84, lon, lat))
		longitude[y, x], latitude[y, x] = pyproj.transform(osgb36, wgs84, easting, northing)
		x += 1
	y += 1
# Get finish time
finish = datetime.datetime.now()
print('Finished at:\t\t{0}'.format(finish.strftime(datetime_format)))
# Calculate and display elapsed time (time for script to complete)
elapsed = finish - start
hours, remainder = divmod(elapsed.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
print('Elapsed time:\t\t{0}:{1}:{2:04.1f} seconds'.format(str(int(hours)).zfill(2), str(int(minutes)).zfill(2), seconds))
print('latitude:')
array_corner_values(latitude)
print('longitude')
array_corner_values(longitude)


print('\n\nNumPy ndenumerate()...')
start = datetime.datetime.now()
print('Started at:\t\t\t{0}'.format(start.strftime(datetime_format)))
latitude = np.zeros((len(northings), len(eastings)), dtype=np.float32)
longitude = np.zeros((len(northings), len(eastings)), dtype=np.float32)
# print(latitude.shape)
# print(longitude.shape)
for y, northing in np.ndenumerate(northings):
	# print(y, northing)
	for x, easting in np.ndenumerate(eastings):
		# print(x, easting)
		longitude[y[0], x[0]], latitude[y[0], x[0]] = pyproj.transform(osgb36, wgs84, easting, northing)
# Get finish time
finish = datetime.datetime.now()
print('Finished at:\t\t{0}'.format(finish.strftime(datetime_format)))
# Calculate and display elapsed time (time for script to complete)
elapsed = finish - start
hours, remainder = divmod(elapsed.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
print('Elapsed time:\t\t{0}:{1}:{2:04.1f} seconds'.format(str(int(hours)).zfill(2), str(int(minutes)).zfill(2), seconds))
print('latitude:')
array_corner_values(latitude)
print('longitude')
array_corner_values(longitude)


print('\n\nNumPy meshgrid() and NumPy function...')
start = datetime.datetime.now()
print('Started at:\t\t\t{0}'.format(start.strftime(datetime_format)))
xv, yv = np.meshgrid(eastings, northings)
longitude, latitude = pyproj.transform(osgb36, wgs84, xv, yv)
# Get finish time
finish = datetime.datetime.now()
print('Finished at:\t\t{0}'.format(finish.strftime(datetime_format)))
# Calculate and display elapsed time (time for script to complete)
elapsed = finish - start
hours, remainder = divmod(elapsed.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
print('Elapsed time:\t\t{0}:{1}:{2:04.1f} seconds'.format(str(int(hours)).zfill(2), str(int(minutes)).zfill(2), seconds))
print('latitude:')
array_corner_values(latitude)
print('longitude')
array_corner_values(longitude)







# print('\n\nDone.')
# # Get finish time
# finish = datetime.datetime.now()
# print('\n\nFinished at:\t\t{0}'.format(finish.strftime(datetime_format)))
# # Calculate and display elapsed time (time for script to complete)
# elapsed = finish - start
# hours, remainder = divmod(elapsed.total_seconds(), 3600)
# minutes, seconds = divmod(remainder, 60)
# print('\n\nElapsed time:\t\t{0}:{1}:{2:04.1f} seconds\n'.format(str(int(hours)).zfill(2), str(int(minutes)).zfill(2), seconds))


