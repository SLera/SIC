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

#plot extent
fig, ax = plt.subplots()
ax.set_title('Sea Ice Extent')
ax.plot(dates, e, 'r-')
ax.plot(dates, e, 'ro', label = 'Kara Sea')

ax.plot(dates, eW, 'b-')
ax.plot(dates, eW, 'bo', label = 'Western Kara Sea')

ax.plot(dates, eE, 'g-')
ax.plot(dates, eE, 'go', label = 'Eastern Kara Sea')

ax.set_ylabel(u"km^2$")
# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

fig.autofmt_xdate()
plt.grid()
plt.legend()
plt.show()
plt.savefig('Kara_SIE')


#plot concentration
fig, ax = plt.subplots()
ax.set_title('Sea Ice Concentration')
ax.plot(dates, c, 'r-')
ax.plot(dates, c, 'ro', label = 'Kara Sea')

ax.plot(dates, cW, 'b-')
ax.plot(dates, cW, 'bo', label = 'Western Kara Sea')

ax.plot(dates, cE, 'g-')
ax.plot(dates, cE, 'go', label = 'Eastern Kara Sea')

ax.set_ylabel(u"%")
# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

fig.autofmt_xdate()
plt.grid()
plt.legend()
plt.show()

plt.savefig('Kara_SIC')