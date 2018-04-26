import os
import sys


import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from affine import Affine


import smw_circle_geometry
import smw_triangle_geometry
import smw_rectangle_geometry
import smw_cross_geometry
import smw_diagonal_cross_geometry
import smw_shapefile_polygon_geometry


URL_TEMPLATE = "http://gds-ldb.nerc-lancaster.ac.uk/thredds/dodsC/PETDetail/chess_pet_wwg_{year:04d}{month:02d}.nc"
year = 2010
month = 5
url = URL_TEMPLATE.format(year=year, month=month)
print(url)


dataset = netCDF4.Dataset(url)  # open the dataset
# print(dataset)


show_plots = True


if show_plots:
	plt.figure(figsize=(6,7))
	plt.imshow(dataset['pet'][0,:,:], origin='lower')
	plt.colorbar()
	plt.xticks(np.arange(0, 800, 100))
	plt.yticks(np.arange(0, 1100, 100))
	plt.axis("equal")
	plt.grid(True)
	plt.show()


if show_plots:
	PET = dataset['pet'][:, 200, 500]
	plt.plot(np.arange(1, len(PET)+1), PET)
	plt.xlabel("Day of month")
	plt.ylabel("PET")
	plt.grid(True)
	plt.show()


x, y = 450000.0, 96000.0 # Isle of Wight
x, y = 200000.0, 800000.0 # West Scotland
# geometry = smw_circle_geometry.circle(x=x,
#                                       y=y,
#                                       radius=150000.0)
# geometry = smw_triangle_geometry.triangle(x=x,
#                                           y=y,
#                                           distance=150000.0)
# geometry = smw_rectangle_geometry.rectangle(x=x,
#                                             y=y,
#                                             length=225000.0,
#                                             height=125000.0)
# geometry = smw_cross_geometry.cross(x=x,
#                                     y=y,
#                                     distance=100000.0,
#                                     width=0.3)
# geometry = smw_diagonal_cross_geometry.diagonal_cross(x=x,
#                                                       y=y,
#                                                       distance=100000.0,
#                                                       width=0.4)
# shapefile_filepath = r'G:\endows\accessing-netcdf-data-by-coordinates\shapefiles\bedfordshire.shp'
shapefile_filepath = r'G:\endows\accessing-netcdf-data-by-coordinates\shapefiles\highland.shp'
geometry = smw_shapefile_polygon_geometry.polygon(shapefile=shapefile_filepath,
                                                  dissolve_item='COMMENT_')


# TODO - check out:  https://cambridgespark.com/content/tutorials/geopandas/index.html


# find it's bounding box in array coordinates
index = lambda x,y: (int(x // 1000), int(y // 1000))
# bounds = circle.bounds
bounds = geometry.bounds
print('\n\nbounds:\t\t{0}'.format(bounds))
ll = index(*bounds[0:2])  # lower left
ur = index(*bounds[2:4])  # upper right


# extract a box of data
data = dataset['pet'][0, ll[1]:ur[1],ll[0]:ur[0]]


print('\n\ndata.shape:\t\t{0}'.format(data.shape))
print('data.min():\t\t{0}'.format(data.min()))
print('data.max():\t\t{0}'.format(data.max()))
print('data.mean():\t\t{0}'.format(data.mean()))


# offset for the subset of data
xoff = ll[0]
yoff = ll[1]


# affine transformation from pixel coordinates to geographic coordinates
# 1 pixel = 1000m x 1000m
# the offset is needed because we're masking a subset of the dataset
a = 1000        # change in x with x
b = 0           # change in y with x
c = xoff * 1000 # x offset
d = 0           # change in y with x
e = 1000        # change in y with y
f = yoff * 1000 # y offset


# print('\n\na:\t\t{0}\nb:\t\t{1}\nc:\t\t{2}\nd:\t\t{3}\ne:\t\t{4}\nf:\t\t{5}'.format(a, b, c, d, e, f))
shifted_affine = Affine(a, b, c, d, e, f)
# print('\n\nshifted_affine:\n{0}'.format(shifted_affine))


# create a mask using the geometry
# if we needed more than one day of data we could re-use this mask
# anything the geometry touches with be 0, otherwise 1
import rasterio.features
mask = rasterio.features.rasterize(shapes=[(geometry, 0)],
                                   out_shape=data.shape,
                                   fill=1,
                                   transform=shifted_affine,
                                   all_touched=True,
                                   default_value=99,
                                   dtype=np.uint8)


# make sure the data is a masked array
data = np.ma.array(data)


# apply the mask to the data (bitwise OR)
data.mask = data.mask | mask


show_plots = True


# plot the result
if show_plots:
	plt.figure(figsize=(6, 6))
	plt.imshow(data, origin='lower', interpolation='nearest')
	plt.colorbar()
	plt.grid(True)
	plt.axis("equal")
	extend = 10
	plt.xlim(0 - extend, data.shape[0] + extend)
	plt.ylim(0 - extend, data.shape[0] + extend)
	plt.show()


print('\n\n\n\n\nData cube...')
print('dataset.variables[\'pet\']:')
print(dataset.variables['pet'])
print('dataset[\'pet\'].shape:\t\t{0}'.format(dataset['pet'].shape))
print('data.shape:\t\t{0}'.format(data.shape))
print('\n\nmask.shape:\t\t{0}'.format(mask.shape))
print('np.sum(mask):\t\t{0}'.format(np.sum(mask)))


# field3d = np.random.rand(dataset['pet'].shape[0], data.shape[0], data.shape[1])
field3d = np.zeros(shape=(dataset['pet'].shape[0], data.shape[0], data.shape[1]),
                   dtype=np.float32)
print('\n\nfield3d.shape:\t\t{0}'.format(field3d.shape))
print('np.sum(field3d):\t\t{0}'.format(np.sum(field3d)))


field3d_mask = np.broadcast_to(mask, field3d.shape)
print('\n\nfield3d_mask.shape:\t\t{0}'.format(field3d_mask.shape))
print('np.sum(field3d_mask):\t\t{0}'.format(np.sum(field3d_mask)))


print(ll, ur)


data3d = dataset['pet'][:, ll[1]:ur[1],ll[0]:ur[0]]
print('\n\ntype(data3d):\t\t{0}'.format(type(data3d)))
print('data3d.shape:\t\t{0}'.format(data3d.shape))
print('np.min(data3d):\t\t{0}'.format(np.min(data3d)))
print('np.max(data3d):\t\t{0}'.format(np.max(data3d)))
print('np.mean(data3d):\t\t{0}'.format(np.mean(data3d)))
data3d = np.ma.array(data3d)
print('\n\ntype(data3d):\t\t{0}'.format(type(data3d)))
print('data3d.shape:\t\t{0}'.format(data3d.shape))
print('np.ma.min(data3d):\t\t{0}'.format(np.ma.min(data3d)))
print('np.ma.max(data3d):\t\t{0}'.format(np.ma.max(data3d)))
print('np.ma.mean(data3d):\t\t{0}'.format(np.ma.mean(data3d)))


show_plots = True
# plot the result
if show_plots:
	plt.figure(figsize=(6, 6))
	plt.imshow(data3d[0], origin='lower', interpolation='nearest')
	plt.colorbar()
	plt.grid(True)
	plt.axis("equal")
	extend = 10
	# plt.xlim(0 - extend, data3d.shape[1] + extend)
	# plt.ylim(0 - extend, data3d.shape[2] + extend)
	plt.show()


data3d.mask = data3d.mask | field3d_mask
print('\n\ntype(data3d):\t\t{0}'.format(type(data3d)))
print('data3d.shape:\t\t{0}'.format(data3d.shape))
print('np.ma.min(data3d):\t\t{0}'.format(np.ma.min(data3d)))
print('np.ma.max(data3d):\t\t{0}'.format(np.ma.max(data3d)))
print('np.ma.mean(data3d):\t\t{0}'.format(np.ma.mean(data3d)))


# if show_plots:
# 	for n in range(data3d.shape[0]):
# 		plt.figure(figsize=(6, 6))
# 		plt.imshow(data3d[n], origin='lower', interpolation='nearest')
# 		plt.colorbar()
# 		plt.grid(True)
# 		plt.axis("equal")
# 		extend = 10
# 		# plt.xlim(0 - extend, data3d.shape[1] + extend)
# 		# plt.ylim(0 - extend, data3d.shape[2] + extend)
# 		plt.show()


if show_plots:
	fig = plt.figure(figsize=(12, 9))
	for n in range(data3d.shape[0]):
		ax = fig.add_subplot(7, 5, n + 1)
		ax.imshow(data3d[n], origin='lower', interpolation='nearest')
		# plt.colorbar()
		ax.grid(True)
		# ax.axis("equal")
		# extend = 10
		# plt.xlim(0 - extend, data3d.shape[1] + extend)
		# plt.ylim(0 - extend, data3d.shape[2] + extend)
	plt.show()


dataset.close()
