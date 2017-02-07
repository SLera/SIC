# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 18:21:16 2017

@author: lselyuzh
"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

y,m,e,c = np.loadtxt('Kara_SIC_monthly_1978-2015.txt',dtype = int,skiprows=1, unpack=True)
yW,mW,eW,cW = np.loadtxt('WKara_SIC_monthly_1978-2015.txt',skiprows=1,unpack=True)
yE,mE,eE,cE = np.loadtxt('EKara_SIC_monthly_1978-2015.txt',skiprows=1,unpack=True)

dates = [datetime.date(y[i],m[i],1) for i in range(len(y))]

years = np.arange(1978,2016)

data = []
dataW = []
dataE = []

for i in range(len(y)):
    for j in range(len(m)):
        if m[i]<6:
            m[i]=m[i]+12
            y[i]=y[i]-1
print y, m            
for i in range(len(years)):
    data_y = []
    dataW_y = []
    dataE_y = []
      
    ind_y = np.where(y==years[i])
   
    mean_e = e[ind_y].mean()
    mean_c = c[ind_y].mean()
    
    mean_eE = eE[ind_y].mean()
    mean_cE = cE[ind_y].mean()
    
    mean_eW = eW[ind_y].mean()
    mean_cW = cW[ind_y].mean()
    
    dataW.append(np.array([years[i],mean_eW, mean_cW], dtype = int))
    dataE.append(np.array([years[i],mean_eE, mean_cE], dtype = int))
    data.append(np.array([years[i],mean_e, mean_c], dtype = int))

dataW = np.array(dataW)
dataE = np.array(dataE)
data = np.array(data)
np.savetxt('WKara_SIC_Nov_Mar_1978-2015.txt',dataE,fmt='%1.0f')
np.savetxt('EKara_SIC_Nov_Mar_1978-2015.txt',dataE,fmt='%1.0f')
np.savetxt('Kara_SIC_Nov_Mar_1978-2015.txt',data,fmt='%1.0f')
    
#plot extent
fig, ax = plt.subplots()
ax.set_title('Sea Ice Extent')
ax.plot(years, data[:,1], 'r-')
ax.plot(years, data[:,1], 'ro', label = 'Kara Sea')

ax.plot(years, dataW[:,1], 'b-')
ax.plot(years, dataW[:,1], 'bo', label = 'Western Kara Sea')

ax.plot(years, dataE[:,1], 'g-')
ax.plot(years, dataE[:,1], 'go', label = 'Eastern Kara Sea')

ax.set_ylabel(u"km^2$")
## format the ticks
#ax.xaxis.set_major_locator(years)
#ax.xaxis.set_major_formatter(yearsFmt)
#ax.xaxis.set_minor_locator(months)

#fig.autofmt_xdate()
plt.grid()
plt.legend()
plt.show()
plt.savefig('Kara_SIE')


#plot concentration
fig, ax = plt.subplots()
ax.set_title('Sea Ice Concentration')
ax.plot(years, data[:,2], 'r-')
ax.plot(years, data[:,2], 'ro', label = 'Kara Sea')

ax.plot(years, dataW[:,2], 'b-')
ax.plot(years, dataW[:,2], 'bo', label = 'Western Kara Sea')

ax.plot(years, dataE[:,2], 'g-')
ax.plot(years, dataE[:,2], 'go', label = 'Eastern Kara Sea')

ax.set_ylabel(u"%")
# format the ticks
#ax.xaxis.set_major_locator(years)
#ax.xaxis.set_major_formatter(yearsFmt)
#ax.xaxis.set_minor_locator(months)

#fig.autofmt_xdate()
plt.grid()
plt.legend()
plt.show()

plt.savefig('Kara_SIC')