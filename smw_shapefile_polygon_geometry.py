import geopandas


def polygon(shapefile, dissolve_item):
	shape = geopandas.read_file(shapefile)
	shape_dissolved = shape.dissolve(by=dissolve_item)
	return shape_dissolved.ix[0].geometry
