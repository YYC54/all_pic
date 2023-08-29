import os
import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import netCDF4

def get_monthly_mean_aod_ctt(aod_filename, ctt_filename):

    aod_file = SD(aod_filename, SDC.READ)
    aod_data = aod_file.select('DUEXTTAU')[:]
    aod_data[aod_data == 9.9999999E14] = np.nan
    aod_data = np.nan_to_num(aod_data, nan=0)
    aod_mean = np.mean(aod_data)
    aod_file.end()


    ctt_file = netCDF4.Dataset(ctt_filename, 'r')
    ctt_data = ctt_file.variables['ref_liq'][:]
    # Clean up the data
    ctt_data[ctt_data == -999] = np.nan
    ctt_data = np.nan_to_num(ctt_data, nan=0)

    ctt_mean = np.mean(ctt_data)
    ctt_file.close()

    return aod_mean, ctt_mean

aod_folder = '/Users/yanyuchen/气溶胶散点图/Merry-2'  #
ctt_folder = '/Users/yanyuchen/气溶胶散点图/LWP'      #你的路径

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
    #print(np.isnan(aod_means))
# 画散点图
plt.scatter(aod_means, ctt_means, s=20)
plt.xlabel('Aerosol Optical Depth (AOD)')
plt.ylabel('Effective Radius of Liquid Droplets (ref_liq)')
plt.title('Monthly Mean AOD and ref_liq Scatter Plot')



z = np.polyfit(aod_means, ctt_means, 1) #3代表3次拟合，这个图1次拟合没有效果，当然也有可能数据太少了，你可以用你的数据改成1试试
print(z[0])
p = np.poly1d(z) # 生成函数方程
print(p)

plt.plot(aod_means, p(aod_means), "r")
plt.annotate('y = {:.2e}x + {:.2e}'.format(z[0],z[1]), (0.95, 0.95), xycoords='axes fraction', ha='right', va='top')

path = 'aod_ref_liq.png'  #改成你的保存路径
plt.savefig(path, dpi=300)

# Show the scatter plot
plt.show()
