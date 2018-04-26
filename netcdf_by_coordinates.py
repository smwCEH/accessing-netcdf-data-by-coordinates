import os
import sys
import timeit


import netCDF4


from naive_slow import Naive_slow
from naive_fast import Naive_fast
from tunnel_fast import Tunnel_fast
from kdtree_fast import Kdtree_fast


filename = r'../data/rtofs_glo_3dz_f006_6hrly_reg3.nc'


# print('\n\nNaive_slow...')
# ncfile = netCDF4.Dataset(filename, 'r')
# ns = Naive_slow(ncfile,'Latitude','Longitude')
# iy,ix = ns.query(50.0, -140.0)
# print('Closest lat lon:', ns.latvar[iy,ix], ns.lonvar[iy,ix])
# ncfile.close()
#
#
# print('\n\nNaive_fast...')
# ncfile = netCDF4.Dataset(filename, 'r')
# ns = Naive_fast(ncfile,'Latitude','Longitude')
# iy,ix = ns.query(50.0, -140.0)
# print('Closest lat lon:', ns.latvar[iy,ix], ns.lonvar[iy,ix])
# ncfile.close()
#
#
# print('\n\nTunnel_fast...')
# ncfile = netCDF4.Dataset(filename, 'r')
# ns = Tunnel_fast(ncfile,'Latitude','Longitude')
# iy,ix = ns.query(50.0, -140.0)
# print('Closest lat lon:', ns.latvar[iy,ix], ns.lonvar[iy,ix])
# ncfile.close()
#
#
# print('\n\nKdtree_fast...')
# ncfile = netCDF4.Dataset(filename, 'r')
# ns = Kdtree_fast(ncfile,'Latitude','Longitude')
# iy,ix = ns.query(50.0, -140.0)
# print('Closest lat lon:', ns.latvar[iy,ix], ns.lonvar[iy,ix])
# ncfile.close()


methods_dict = {}
methods_dict[1] = {'module': 'naive_slow',
                   'method': 'Naive_slow',
                   'object': 'ns'}
methods_dict[2] = {'module': 'naive_fast',
                   'method': 'Naive_fast',
                   'object': 'nf'}
methods_dict[3] = {'module': 'tunnel_fast',
                   'method': 'Tunnel_fast',
                   'object': 'tf'}
methods_dict[4] = {'module': 'kdtree_fast',
                   'method': 'Kdtree_fast',
                   'object': 'kf'}


for n in range(1, 5, 1):
	print('\n\n{0}...'.format(methods_dict[n]['method']))
	print('\tCreate {0}...'.format(methods_dict[n]['object']))
	setup = '''
import netCDF4
from {0} import {1}
ncfile = netCDF4.Dataset(\'{2}\', \'r\')
'''.format(methods_dict[n]['module'],
           methods_dict[n]['method'],
           filename)
	statement = '''
{0} = {1}(ncfile, \'Latitude\', \'Longitude\')
'''.format(methods_dict[n]['object'],
           methods_dict[n]['method'])
	t1 = timeit.timeit(stmt=statement,
	                   setup=setup,
	                   number=1)
	print('\t\t', t1)
	print('\tCreate {0} and do {0}.query()...'.format(methods_dict[n]['object']))
	setup = '''
import netCDF4
from {0} import {1}
ncfile = netCDF4.Dataset(\'{2}\', \'r\')
{3} = {1}(ncfile, \'Latitude\', \'Longitude\')
'''.format(methods_dict[n]['module'],
           methods_dict[n]['method'],
           filename,
           methods_dict[n]['object'])
	statement = '''
{0}.query(50.0, -140.0)
'''.format(methods_dict[n]['object'])
	t2 = timeit.timeit(stmt=statement,
	                   setup=setup,
	                   number=1)
	print('\t\t', t2)


sys.exit()


# module = 'naive_slow'
# method = 'Naive_slow'
# object = 'ns'
# print('\n\n{0}...'.format(method))
# print('\tCreate {0}...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# '''.format(module, method, filename)
# statement = '''
# {0} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(object, method)
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('\tCreate {0} and do {0}.query()...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# {3} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(module, method, filename, object)
# statement = '''
# {0}.query(50.0, -140.0)
# '''.format(object)
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)
#
#
# module = 'naive_fast'
# method = 'Naive_fast'
# object = 'nf'
# print('\n\n{0}...'.format(method))
# print('\tCreate {0}...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# '''.format(module, method, filename)
# statement = '''
# {0} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(object, method)
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('\tCreate {0} and do {0}.query()...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# {3} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(module, method, filename, object)
# statement = '''
# {0}.query(50.0, -140.0)
# '''.format(object)
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)
#
#
# module = 'tunnel_fast'
# method = 'Tunnel_fast'
# object = 'tf'
# print('\n\n{0}...'.format(method))
# print('\tCreate {0}...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# '''.format(module, method, filename)
# statement = '''
# {0} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(object, method)
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('\tCreate {0} and do {0}.query()...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# {3} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(module, method, filename, object)
# statement = '''
# {0}.query(50.0, -140.0)
# '''.format(object)
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)
#
#
# module = 'kdtree_fast'
# method = 'Kdtree_fast'
# object = 'kf'
# print('\n\n{0}...'.format(method))
# print('\tCreate {0}...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# '''.format(module, method, filename)
# statement = '''
# {0} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(object, method)
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('\tCreate {0} and do {0}.query()...'.format(object))
# setup = '''
# import netCDF4
# from {0} import {1}
# ncfile = netCDF4.Dataset(\'{2}\', \'r\')
# {3} = {1}(ncfile, \'Latitude\', \'Longitude\')
# '''.format(module, method, filename, object)
# statement = '''
# {0}.query(50.0, -140.0)
# '''.format(object)
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)


# print('\n\nNaive_fast...')
# print('\tCreate nf...')
# setup = '''
# import netCDF4
# from naive_fast import Naive_fast
# ncfile = netCDF4.Dataset(\'{0}\', \'r\')
# '''.format(filename)
# statement = '''
# nf = Naive_fast(ncfile, \'Latitude\', \'Longitude\')
# '''
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('\tCreate nf and do nf.query()...')
# setup = '''
# import netCDF4
# from naive_fast import Naive_fast
# ncfile = netCDF4.Dataset(\'{0}\', \'r\')
# nf = Naive_fast(ncfile, \'Latitude\', \'Longitude\')
# '''.format(filename)
# statement = '''
# nf.query(50.0, -140.0)'''
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)
#
#
# print('\n\nTunnel_fast...')
# print('\tCreate tf...')
# setup = '''
# import netCDF4
# from tunnel_fast import Tunnel_fast
# ncfile = netCDF4.Dataset(\'{0}\', \'r\')
# '''.format(filename)
# statement = '''
# tf = Tunnel_fast(ncfile, \'Latitude\', \'Longitude\')
# '''
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('Create tf and do tf.query()...')
# setup = '''
# import netCDF4
# from tunnel_fast import Tunnel_fast
# ncfile = netCDF4.Dataset(\'{0}\', \'r\')
# tf = Tunnel_fast(ncfile, \'Latitude\', \'Longitude\')
# '''.format(filename)
# statement = '''
# tf.query(50.0, -140.0)'''
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)
#
#
# print('\n\nKdtree_fast...')
# print('\tCreate kf...')
# setup = '''
# import netCDF4
# from tunnel_fast import Tunnel_fast
# ncfile = netCDF4.Dataset(\'{0}\', \'r\')
# '''.format(filename)
# statement = '''
# kf = Tunnel_fast(ncfile, \'Latitude\', \'Longitude\')
# '''
# t1 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t1)
# print('Create kf and do kf.query()...')
# setup = '''
# import netCDF4
# from tunnel_fast import Tunnel_fast
# ncfile = netCDF4.Dataset(\'{0}\', \'r\')
# kf = Tunnel_fast(ncfile, \'Latitude\', \'Longitude\')
# '''.format(filename)
# statement = '''
# kf.query(50.0, -140.0)'''
# t2 = timeit.timeit(stmt=statement,
#                    setup=setup,
#                    number=1)
# print('\t\t', t2)
