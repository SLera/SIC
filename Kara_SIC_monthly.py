# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 16:48:44 2017

@author: lselyuzh
"""

from struct import unpack
import ogr, os, sys
import numpy as np

#import matplotlib
#matplotlib.use('qt5agg')

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
    y = np.arange(5850000,-5350000,-a)
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

def SIC_KARA(FILENAME, xx,yy):
    arctic_sic = SIC_grid(FILENAME)
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
    kara_sic = np.zeros((448,304))
    kara_sic.fill(1500)
    ind_kara_x= np.load('ind_kara_x')
    ind_kara_y= np.load('ind_kara_y')
    for i in range(len(ind_kara_x)):
        k = ind_kara_x[i]
        n = ind_kara_y[i]
        c = path.contains_point((xx[k,n],yy[k,n]))
        if c == 1:
            kara_sic[k,n]=arctic_sic[k,n]
    return kara_sic/10
    
     


lats, lons, pr, xx, yy = create_grid_SIC_25km()

#filename =  'bt_197811_n07_v02_n.bin'

INDIR = 'D:\\DATA\\SeaIceConcentration\\nsidc0079_gsfc_bootstrap_seaice\\monthly\\'
months = np.array([11,12,1,2,3])
filelist = []
data = []

for root, dirs, files in os.walk(INDIR):
    for file in files:
        filelist.append(os.path.join(root, file))
        
for i in range(len(filelist)):
    year = np.int(filelist[i][-20:-16])
    print year
    month = np.int(filelist[i][-16:-14])   
    
    if month in months:  
        #print month          
        sic = SIC_KARA(filelist[i], xx,yy)
        
        pix_area = 25 #pix area in km
        
        ind_aoi = np.where(sic<=100)
        ind_extent = np.where((sic>0)&(sic<=100))
        
        
        sic_extent = np.shape(ind_extent)[1]*pix_area**2
        sic_mean = sic[ind_extent].mean()
        
        data.append(np.array([year,month,sic_extent, sic_mean], dtype = int))

np.savetxt('Kara_SIC_monthly_1978-2015',data,fmt='%1.0f')