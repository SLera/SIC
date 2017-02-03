# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 19:29:30 2017

@author: lselyuzh
"""
from struct import unpack
import numpy as np
import pyproj

#import matplotlib
#matplotlib.use('qt5agg')

import matplotlib.pyplot as plt

#read bootstrap sic

#FOLDER_ICECONC  = r'D:\\DATA\\SeaIceConcentration\\nsidc0079_gsfc_bootstrap_seaice\\monthly\\'

#FILENAME = FOLDER_ICECONC+'bt_197811_n07_v02_n.bin'
#def read_sic_bootstrap_Kara(FILENAME):
FILENAME = 'bt_197811_n07_v02_n.bin'

ns = 448*304 #for reading data

f = open(FILENAME, 'rb')
data=f.read(2*ns)
f.close()
       
unpacked_bytes = unpack("<%sH" % ns, data)
ice_inf=np.array(unpacked_bytes).reshape(448,304)

plt.figure()
plt.imshow(ice_inf)
plt.show()



