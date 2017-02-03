# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 11:38:13 2013

@author: lselyuzh
"""
from pyproj import Proj
import numpy as np

def create_grid_SIC_25km(): 
    #define projection
    #proj4_args = "+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +a=6378273 +b=6356889.449 +units=m +no_defs"
    proj4_args = "+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +a=6378273 +b=6356889.449 +units=m +no_defs"
    pr = Proj(proj4_args)
    #grid cell in m
    a = 25000
    x = np.arange(-3850000,3750000,a)
    y = np.arange(5850000,-5350000,-a)
    xx,yy = np.meshgrid(x,y)
    lats=[]
    lons=[]
    for i in range(len(xx)):
        print i
        lon,lat = pr(xx[i],yy[i],inverse=True)
        lats.append(lat)
        lons.append(lon)
    lats = np.array(lats)
    lons = np.array(lons)
    return lats, lons, pr, xx, yy
    
#lats.dump('lats25kmPStereo')
#lons.dump('lons25kmPStereo')
