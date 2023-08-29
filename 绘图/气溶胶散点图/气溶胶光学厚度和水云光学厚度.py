import os
import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import netCDF4

def get_monthly_mean_aod_ctt(aod_filename, ctt_filename):

    aod_file = SD(aod_filename, SDC.READ)
    aod_data = aod_file.select('DUEXTTAU')[:]
    aod_mean = np.mean(aod_data)
    aod_file.end()


    ctt_file = netCDF4.Dataset(ctt_filename, 'r')
    ctt_data = ctt_file.variables['cot_liq'][:]
    ctt_mean = np.mean(ctt_data)
    ctt_file.close()

    return aod_mean, ctt_mean

aod_folder = '/Users/yanyuchen/气溶胶散点图/Merry-2'  #你的路径
ctt_folder = '/Users/yanyuchen/气溶胶散点图/LWP'      #

aod_files = sorted(os.listdir(aod_folder))
print(aod_files)
ctt_files = sorted(os.listdir(ctt_folder))
print(ctt_files)


aod_means = []
ctt_means = []
for aod_file, ctt_file in zip(aod_files, ctt_files):
    aod_filename = os.path.join(aod_folder, aod_file)
    ctt_filename = os.path.join(ctt_folder, ctt_file)

    aod_mean, ctt_mean = get_monthly_mean_aod_ctt(aod_filename, ctt_filename)
    aod_means.append(aod_mean)
    ctt_means.append(ctt_mean)

# 画散点图
plt.scatter(aod_means, ctt_means, s=20)
plt.xlabel('Aerosol Optical Depth (AOD)')
plt.ylabel('Water Cloud Optical Thickness (cot_liq)')
plt.title('Monthly Mean AOD and cot_liq Scatter Plot')



z = np.polyfit(aod_means, ctt_means, 1) #
p = np.poly1d(z) # 生成函数方程


plt.plot(aod_means, p(aod_means), "r")
plt.annotate('y = {:.2f}x + {:.2f}'.format(z[0],z[1]), (0.95, 0.95), xycoords='axes fraction', ha='right', va='top')

path = 'aod cot_liq.png'  #改成你的保存路径
plt.savefig(path, dpi=300)

# Show the scatter plot
plt.show()
