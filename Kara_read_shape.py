# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 17:50:55 2017

@author: lselyuzh
"""
from struct import unpack
import ogr, os, sys
import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.nxutils as nx
import pyproj


# Open Shapefile

INDIR = 'D:\\GIS\\temp\\'
shpfile =INDIR + 'KaraSea_polygon_WGS84.shp'

FILENAME = shpfile
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

