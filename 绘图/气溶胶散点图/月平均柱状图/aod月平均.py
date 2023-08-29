import os
import re
import numpy as np
from pyhdf.SD import SD, SDC
import matplotlib.pyplot as plt
import geopandas as gpd

def read_aod(filename,path ):
    aod_file = SD(filename, SDC.READ)
    aod_data = aod_file.select('DUEXTTAU')[:]

    aod_data = aod_data[0]

    ydim_data = aod_file.select('YDim:EOSGRID')[:]
    xdim_data = aod_file.select('XDim:EOSGRID')[:]

    aod_lats = np.linspace(-90, 90, len(ydim_data))
    aod_lons = np.linspace(-180, 180, len(xdim_data))

    aod_file.end()
    boundary_gdf = gpd.read_file(path).iloc[0]['geometry']
    lat_min, lat_max = 35, 45
    lon_min, lon_max = 70, 90
    lat_indices = np.where((aod_lats >= lat_min) & (aod_lats <= lat_max))
    lon_indices = np.where((aod_lons >= lon_min) & (aod_lons <= lon_max))
    tarim_aod_data = aod_data[np.ix_(lat_indices[0], lon_indices[0])]
    mean_aod = np.mean(tarim_aod_data)

    return mean_aod





path = '/Users/yanyuchen/气溶胶散点图/tarim_region.shp'  #shp文件路径
folder_path = '/Users/yanyuchen/气溶胶散点图/Merry-2'  #文件夹路径


pattern = re.compile(r'MERRA2_100\.tavgM_2d_aer_Nx\.(\d{6})\.SUB\.hdf')
monthly_files = {}
for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        year_month = match.group(1)
        month = year_month[-2:]
        file_path = os.path.join(folder_path, filename)
        if month in monthly_files:
            monthly_files[month].append(file_path)
        else:
            monthly_files[month] = [file_path]

monthly_mean_aods = {}

for month, file_paths in monthly_files.items():
    month_aods = []
    for file_path in file_paths:
        mean_aod = read_aod(file_path, path)
        month_aods.append(mean_aod)

    monthly_mean_aods[month] = np.mean(month_aods)
months = []
mean_aods = []
for month, mean_aod in monthly_mean_aods.items():
    months.append(int(month))
    mean_aods.append(mean_aod)

# 绘制直方图
plt.bar(months, mean_aods)

plt.xlabel('Month')
plt.ylabel('Mean AOD')

plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# 设置图表标题
plt.title('Mean AOD by Month')
plt.savefig('mean_aod_month')  #保存路径
plt.show()