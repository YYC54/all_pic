import os
import re
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import geopandas as gpd
def read(filename, path ):
    ref_liq_file = Dataset(filename, "r")
    ref_liq_data = ref_liq_file.variables['ref_liq'][:]
    ref_liq_data = ref_liq_data[0]
    ref_liq_lats = ref_liq_file.variables['lat'][:]
    ref_liq_lons = ref_liq_file.variables['lon'][:]
    ref_liq_file.close()
    lat_min, lat_max = 35, 45
    lon_min, lon_max = 70, 90
    boundary_gdf = gpd.read_file(path).iloc[0]['geometry']
    lat_indices = np.where((ref_liq_lats >= lat_min) & (ref_liq_lats <= lat_max))
    lon_indices = np.where((ref_liq_lons >= lon_min) & (ref_liq_lons <= lon_max))
    tarim_ref_liq_data = ref_liq_data[np.ix_(lat_indices[0], lon_indices[0])]
    mean_ref_liq = np.mean(tarim_ref_liq_data)

    return mean_ref_liq

folder_path = '/Users/yanyuchen/气溶胶散点图/LWP'        #文件夹路径
path = '/Users/yanyuchen/气溶胶散点图/tarim_region.shp'  #shp文件路径


pattern = re.compile(r'LWPmm(\d{4})(\d{2})\d{11}AVPOS01GL\.nc')
monthly_files = {}
for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        year = match.group(1)
        month = match.group(2)
        print(year)
        file_path = os.path.join(folder_path, filename)
        if month in monthly_files:
            monthly_files[month].append(file_path)
        else:
            monthly_files[month] = [file_path]

monthly_mean_ref_liqs = {}
for month, file_paths in monthly_files.items():
    month_ctts = []
    for file_path in file_paths:
        mean_ctt = read(file_path,path)
        month_ctts.append(mean_ctt)

    monthly_mean_ref_liqs[month] = np.mean(month_ctts)
months = []
mean_ctts = []
for month, mean_ctt in monthly_mean_ref_liqs.items():
    months.append(int(month))
    mean_ctts.append(mean_ctt)

# 绘制直方图
plt.bar(months, mean_ctts)

plt.xlabel('Month')
plt.ylabel('Mean Ref_liq')

plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# 设置图表标题
plt.title('Mean Ref_liq by Month')
plt.savefig('mean_ref_liq_month')  #保存路径
plt.show()
