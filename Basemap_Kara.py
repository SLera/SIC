# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:36:30 2017

@author: lselyuzh
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as col
import matplotlib.cm as cm
from matplotlib.patches import Polygon
from struct import unpack


FILENAME = 'bt_197811_n07_v02_n.bin'

ns = 448*304 #for reading data

f = open(FILENAME, 'rb')
data=f.read(2*ns)
f.close()
       
unpacked_bytes = unpack("<%sH" % ns, data)
ice_inf=np.array(unpacked_bytes).reshape(448,304)


#fig = plt.figure(1, figsize=(8, 14), frameon=False, dpi=100)
#fig.add_axes([0, 0, 1, 1])
plt.figure()

lats = np.load('D:\NIERSC\SIC\\lats25kmPStereo')
lons = np.load ('D:\NIERSC\SIC\\lons25kmPStereo')
#lats = lats[170:230,160:260]
#lons = lons[170:230,160:260]
#ice_inf = ice_inf[170:230,160:260]
#
#for i in np.arange(np.shape(lons)[0]):
#    for j in np.arange(np.shape(lons)[1]):
#        if lons[i,j]<0:
#            lons[i,j]=360-lons[i,j]
    
INDIR = 'D:\\GIS\\temp\\'
shpfile =INDIR + 'KaraSea_polygon_WGS84'
m = Basemap(resolution="i",
            projection='stere', lat_ts=70, lat_0=90., lon_0=315.,
            llcrnrlon= lons[447,0], llcrnrlat= lats[447,0] ,
            urcrnrlon= lons[0,303], urcrnrlat= lats[0,303],
            rsphere=(6378273,6356889.449))

m.imshow(ice_inf*100, origin = 'upper')
    
#m.drawcoastlines(color= 'w')
 
m.readshapefile(shpfile,'kara')
 

m.drawmeridians(np.arange(75.,76.,5.),labels=[1, 0, 0, 0])
#m.drawparallels(np.arange(60.,80.,5.),labels=[1, 0, 0, 0])
#m.drawrivers(linewidth=0.5, linestylonsle='solid', color='k', antialiased=1, ax=None, zorder=None)

plt.savefig('Kara_SIC-test.pdf', pad_inches=0.0, bbox_inches='tight')
plt.show()