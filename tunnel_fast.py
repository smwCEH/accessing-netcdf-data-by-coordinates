import numpy as np
import netCDF4
from math import pi
from numpy import cos, sin


class Tunnel_fast(object):
	def __init__(self, ncfile, latvarname, lonvarname):
		self.ncfile = ncfile
		self.latvar = self.ncfile.variables[latvarname]
		self.lonvar = self.ncfile.variables[lonvarname]
		# Read latitude and longitude from file into numpy arrays
		rad_factor = pi / 180.0  # for trignometry, need angles in radians
		self.latvals = self.latvar[:] * rad_factor
		self.lonvals = self.lonvar[:] * rad_factor
		self.shape = self.latvals.shape
		clat, clon, slon = cos(self.latvals), cos(self.lonvals), sin(self.lonvals)
		self.clat_clon = clat * clon
		self.clat_slon = clat * slon
		self.slat = sin(self.latvals)

	def query(self, lat0, lon0):
		# for trignometry, need angles in radians
		rad_factor = pi / 180.0
		lat0_rad = lat0 * rad_factor
		lon0_rad = lon0 * rad_factor
		delX = cos(lat0_rad) * cos(lon0_rad) - self.clat_clon
		delY = cos(lat0_rad) * sin(lon0_rad) - self.clat_slon
		delZ = sin(lat0_rad) - self.slat;
		dist_sq = delX ** 2 + delY ** 2 + delZ ** 2
		minindex_1d = dist_sq.argmin()  # 1D index
		iy_min, ix_min = np.unravel_index(minindex_1d, self.shape)  # 2D indexes
		return iy_min, ix_min
