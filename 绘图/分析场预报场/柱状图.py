import os
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

def get_files(folder):
    files = []
    for file in os.listdir(folder):
        files.append(os.path.join(folder, file))
    print(sorted(files))
    return sorted(files)

folder = '/Users/yanyuchen/绘图/分析场预报场/降水'
file_list = get_files(folder)
lat_range = [29.55, 29.65]
lon_range = [91.05, 91.15]

rain_means = []

for file in file_list:
    with nc.Dataset(file, 'r') as ds:
        lats = ds.variables['lat'][:]
        lons = ds.variables['lon'][:]
        rain = ds.variables['rain'][:]

        lat_idx = np.where((lats >= lat_range[0]) & (lats <= lat_range[1]))[0]
        lon_idx = np.where((lons >= lon_range[0]) & (lons <= lon_range[1]))[0]

        subset_rain = rain[np.ix_(lat_idx, lon_idx)]
        rain_means.append(np.mean(subset_rain))

# 计算每小时降水量与前一个小时降水量之间的差值
rain_diff = np.diff(rain_means)
rain_diff = np.insert(rain_diff, 0, rain_means[0])  # 添加第一个小时的降水值

timestamps = [os.path.basename(file)[:10] for file in file_list]
plt.figure(figsize=(20, 10))

# 设置x轴刻度和标签
xtick_labels = ['06Z\n21JUN\n2017', '12Z', '18Z',  '00Z\n22JUN\n2017', '06Z', '12Z', '18Z']
num_ticks = len(xtick_labels)
xticks = np.linspace(0, len(timestamps) - 1, num_ticks)  # 根据标签数量生成刻度
plt.xticks(xticks, xtick_labels)

plt.bar(timestamps, rain_diff,  color='lightgreen',width=0.5)
plt.xlabel('')
plt.ylabel('')
plt.title('')
plt.xticks(rotation=90)

# 设置边框
ax = plt.gca()
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('柱状图')
plt.show()
