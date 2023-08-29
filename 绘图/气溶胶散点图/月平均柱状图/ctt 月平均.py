import os
import re
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import geopandas as gpd
def read_ctt(filename, path ):
    ctt_file = Dataset(filename, "r")
    ctt_data = ctt_file.variables['ctt'][:]
    ctt_data = ctt_data[0]
    ctt_lats = ctt_file.variables['lat'][:]
    ctt_lons = ctt_file.variables['lon'][:]
    ctt_file.close()
    lat_min, lat_max = 35, 45
    lon_min, lon_max = 70, 90
    boundary_gdf = gpd.read_file(path).iloc[0]['geometry']
    lat_indices = np.where((ctt_lats >= lat_min) & (ctt_lats <= lat_max))
    lon_indices = np.where((ctt_lons >= lon_min) & (ctt_lons <= lon_max))
    tarim_ctt_data = ctt_data[np.ix_(lat_indices[0], lon_indices[0])]
    mean_ctt = np.mean(tarim_ctt_data)

    return mean_ctt

folder_path = '/Users/yanyuchen/气溶胶散点图/CTO'        #文件夹路径
path = '/Users/yanyuchen/气溶胶散点图/tarim_region.shp'  #shp文件路径


pattern = re.compile(r'CTOmm(\d{4})(\d{2})\d{11}AVPOS01GL\.nc')
monthly_files = {}
for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        file_path = os.path.join(folder_path, filename)
        if month in monthly_files:
            monthly_files[month].append(file_path)
        else:
            monthly_files[month] = [file_path]

monthly_mean_ctts = {}
for month, file_paths in monthly_files.items():
    month_ctts = []
    for file_path in file_paths:
        mean_ctt = read_ctt(file_path,path)
        month_ctts.append(mean_ctt)

    monthly_mean_ctts[month] = np.mean(month_ctts)
months = []
mean_ctts = []
for month, mean_ctt in monthly_mean_ctts.items():
    months.append(int(month))
    mean_ctts.append(mean_ctt)

# 绘制直方图
plt.bar(months, mean_ctts)

plt.xlabel('Month')
plt.ylabel('Mean CTT')

plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# 设置图表标题
plt.title('Mean CTT by Month')
plt.savefig('mean_ctt_month')  #保存路径
plt.show()
