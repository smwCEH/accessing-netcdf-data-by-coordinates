import numpy as np
import netCDF4


class Naive_slow(object):
    def __init__(self, ncfile, latvarname, lonvarname):
        self.ncfile = ncfile
        self.latvar = self.ncfile.variables[latvarname]
        self.lonvar = self.ncfile.variables[lonvarname]
        # Read latitude and longitude from file into numpy arrays
        self.latvals = self.latvar[:]
        self.lonvals = self.lonvar[:]
        self.shape = self.latvals.shape

    def query(self, lat0, lon0):
        ny,nx = self.shape
        dist_sq_min = 1.0e30
        for iy in range(ny):
            for ix in range(nx):
                latval = self.latvals[iy, ix]
                lonval = self.lonvals[iy, ix]
                dist_sq = (latval - lat0)**2 + (lonval - lon0)**2
                if dist_sq < dist_sq_min:
                    iy_min, ix_min, dist_sq_min = iy, ix, dist_sq
        return iy_min,ix_min
