import numpy as np
import netCDF4


class Naive_fast(object):
	def __init__(self, ncfile, latvarname, lonvarname):
		self.ncfile = ncfile
		self.latvar = self.ncfile.variables[latvarname]
		self.lonvar = self.ncfile.variables[lonvarname]
		# Read latitude and longitude from file into numpy arrays
		self.latvals = self.latvar[:]
		self.lonvals = self.lonvar[:]
		self.shape = self.latvals.shape

	def query(self, lat0, lon0):
		dist_sq = (self.latvals - lat0) ** 2 + (self.lonvals - lon0) ** 2
		minindex_flattened = dist_sq.argmin()  # 1D index
		iy_min, ix_min = np.unravel_index(minindex_flattened, self.shape)  # 2D indexes
		return iy_min, ix_min
