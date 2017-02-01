# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 18:08:04 2017

@author: lselyuzh
"""
from struct import unpack
import ogr, os, sys
import numpy as np

import matplotlib
matplotlib.use('qt5agg')

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
#import matplotlib.nxutils as nx
import pyproj


def read_Kara_polygon(FILENAME):
    fn = FILENAME
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(fn, 0)
    # Get Layer
    #print 'The file contains ', dataSource.GetLayerCount(), ' Layers'
    layer = dataSource.GetLayer(0)
    ref = layer.GetSpatialRef()
    projection = ref.ExportToProj4()
    # Get all Features in the Layer
    #print layer.GetName(), ' contains ', layer.GetFeatureCount(), ' features'
    all_verts = []       
    for feature in layer:
            # Get Geometry
            geometry = feature.GetGeometryRef()  
            # Get Geometry inside Geometry
            verts = []
            #for r in range(geometry.GetGeometryCount()):
            for r in range(1):
                ring = geometry.GetGeometryRef(r)
                ring = geometry.GetGeometryRef(r)
                ##Get vetrex of polygons
                numpoints = ring.GetPointCount()
                for j in range(numpoints):
                    verts.append(ring.GetPoint(j))
            verts = np.array(verts)[:,0:-1]
            
            all_verts.append(verts)
    return all_verts, projection

def create_grid_SIC_25km(): 
    #define projection
    #proj4_args = "+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +a=6378273 +b=6356889.449 +units=m +no_defs"
    proj4_args = "+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +a=6378273 +b=6356889.449 +units=m +no_defs"
    pr = pyproj.Proj(proj4_args)
    #grid cell in m
    a = 25000
    x = np.arange(-3850000,3750000,a)
    y = np.arange(-5350000,5850000,a)
    xx,yy = np.meshgrid(x,y)
    lats=[]
    lons=[]
    for i in range(len(xx)):
        lon,lat = pr(xx[i],yy[i],inverse=True)
        lats.append(lat)
        lons.append(lon)
    lats = np.array(lats)
    lons = np.array(lons)
    return lats, lons, pr, xx, yy       

def SIC_grid(FILENAME):
    ns = 448 * 304  # for reading data
    f = open(FILENAME, 'rb')
    data = f.read(2 * ns)
    f.close()
    unpacked_bytes = unpack("<%sH" % ns, data)
    ice_inf = np.array(unpacked_bytes).reshape(448, 304)
    return ice_inf
     
filename =  'bt_197811_n07_v02_n.bin'

lats, lons, pr, xx, yy = create_grid_SIC_25km()
arctic_sic = SIC_grid(filename)
arctic_sic_fl = arctic_sic.flatten()
     
#def SIC_grid(FILENAME, xx,yy):
x = xx.flatten()
y = yy.flatten()
points = np.vstack((x,y)).T #coords of grid in SIC projection

all_verts, p = read_Kara_polygon('KaraSea_polygon_WGS84.shp')
#transform lats, lons to sic projection to compare
pSIC = pyproj.Proj("+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +a=6378273 +b=6356889.449 +units=m +no_defs")
pSHP=pyproj.Proj(p)
#create Path instance for Kara shape polygon
pol = all_verts[0]
path_pol = []
codes = []
for i in range(len(pol)):
    a = (pol[i][0], pol[i][1])
    a = pyproj.transform(pSHP,pSIC,pol[i][0],pol[i][1])
    path_pol.append(a)
    codes.append(mpath.Path.LINETO)
codes[0] =  mpath.Path.MOVETO
codes[-1] =  mpath.Path.CLOSEPOLY

path = mpath.Path(path_pol, codes)

kara_sic = np.zeros(448*304)

c = path.contains_point((points[76200][0],points[76200][1]))

for i in range(len(points)):
#76200 in range(len(points))
#for i in np.array([76200,76201,76202]):
    c = path.contains_point((points[i][0],points[i][1]))
    if c == 1:
        print 'IN'
        kara_sic[i]=arctic_sic_fl[i]
kara_sic = kara_sic.reshape(448,304)

plt.figure()
plt.imshow(kara_sic)
plt.show()
          
#for i in range(len(all_verts)):
#    #print i
#    for j in range(int(len(points)-1)):
#        grid_point = points[j]
#        print grid_point
#        
#        c = nx.pnpoly(grid_point[0],grid_point[1], all_verts[i])
#        if c == 1:
#            kara_sic[j]=kara_sic[j]
#
#kara_sic = kara_sic.reshape(448,304)
#    
#    #return kara_sic
#    
##filename =  'bt_197811_n07_v02_n.bin'
##
##lats, lons, pr, xx, yy = create_grid_SIC_25km()
#
##kara_sic = SIC_grid(filename, xx,yy)
#
#pol = all_verts[0]
#path_pol = []
#codes = []
#for i in range(len(pol)):
#    a = (pol[i][0], pol[i][1])
#    a = pyproj.transform(pSHP,pSIC,pol[i][0],pol[i][1])
#    path_pol.append(a)
#    codes.append(mpath.Path.LINETO)
#codes[0] =  mpath.Path.MOVETO
#codes[-1] =  mpath.Path.CLOSEPOLY
#
#path = mpath.Path(path_pol, codes)
#
import matplotlib.patches as patches
fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor='orange', lw=2)
ax.add_patch(patch)
ax.set_xlim(0,2500000)
ax.set_ylim(0,2500000)
plt.show()


LIMIT_Kara = [70.,56.,78.,88.]
la_reg = np.where((lats>LIMIT_Kara[0])&(lats<LIMIT_Kara[2]))
lo_reg = np.where((lons>LIMIT_Kara[1])&(lons<LIMIT_Kara[3]))
