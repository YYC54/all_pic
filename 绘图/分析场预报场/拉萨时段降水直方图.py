import os
import re
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def get_files(folder):
    files = []
    for file in os.listdir(folder):
        files.append(os.path.join(folder, file))
    print(sorted(files))
    return sorted(files)

folder = '/Users/yanyuchen/绘图/分析场预报场/降水'
files = get_files(folder)
lon_range = slice(91.05, 91.15)
lat_range = slice(29.55, 29.65)

# 存储每个文件的平均值
mean_values = []

# 读取文件夹中的所有nc文件
for file in files:
    # 打开netCDF文件
    with xr.open_dataset(file) as ds:
        # 提取91.05-91.15, 29.55-29.65范围的数据
        data = ds.sel(lon=lon_range, lat=lat_range)['rain']
        # 计算平均值并添加到mean_values列表中
        mean_values.append(data.mean().values)

# 绘制直方图, edgecolor='black', linewidth=1.2
plt.hist(mean_values, bins=10, rwidth= 0.3, color='lightgreen')
plt.xlabel('')
plt.ylabel('')
plt.title('')

# 设置原点
ax = plt.gca()
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 限制x轴刻度范围
min_value = max(0, min(mean_values))  # 找到最小值且大于等于0的值
max_value = max(mean_values)
plt.xlim(min_value, max_value)

# # 设置x轴刻度和标签
# xticks = np.arange(min_value, max_value, step=6)  # 以0.5为步长生成刻度
# #xtick_labels = [f'{tick:.1f}' for tick in xticks]# 生成刻度标签
# xtick_labels = ['00Z 21JUN 2017','06Z','12Z','18Z','00Z 22JUN 2017','06Z','12Z','18Z']
#
# plt.xticks(xticks, xtick_labels)
#
# plt.show()

# 设置x轴刻度和标签
xtick_labels = ['00Z\n21JUN\n2017', '06Z', '12Z', '18Z', '00Z\n22JUN\n2017', '06Z', '12Z', '18Z']
num_ticks = len(xtick_labels)
xticks = np.linspace(min_value, max_value, num_ticks)  # 根据标签数量生成刻度
plt.xticks(xticks, xtick_labels)
plt.savefig('直方图')
plt.show()