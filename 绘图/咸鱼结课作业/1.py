import pandas
import numpy as np
import datetime as datetime
from matplotlib import pyplot as plt


data = pandas.read_csv('/Users/yanyuchen/咸鱼结课作业/1/slow_data1(1).csv', skiprows=[1], header=0, parse_dates=["TIMESTAMP"], low_memory=False)
ndata = data.shape[0]
ndays = 365
SWD = np.zeros([ndays, 48])

dstart = data.TIMESTAMP[0]
for n in np.arange(0, ndays):
    dend = dstart + pandas.Timedelta(days=1)
    # print(dstart, dend)

    # Make a mask for the 24 hour period between dstart and dend
    mask = (data['TIMESTAMP'] > dstart) & (data['TIMESTAMP'] <= dend)

    # Get the data over the masked period
    data_day = data.loc[mask]

    dtmp = data_day.Rain

    # Put it into your array
    SWD[n, :] = dtmp
    dstart = dend

    print(np.shape(SWD))

    # Average over all days
SWD_mean = np.nanmean(SWD, 0)


fig = plt.figure(figsize=(20,20))
plt.plot(np.arange(0,48), np.transpose(SWD))
plt.plot(np.arange(0,48), SWD_mean, 'k', linewidth=5)
plt.xlabel('Local Time')
plt.ylabel('Rain')
plt.savefig('rain_time')
plt.show()