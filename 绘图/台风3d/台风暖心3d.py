import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
# 读取nc文件
filename = '/Users/yanyuchen/台风3d/Ttemp_soulik.nc'
ds = xr.open_dataset(filename)

# # 如果时间变量是一个标量，为它创建一个维度
# if 'time' not in ds.coords:
#     ds = ds.expand_dims({'time': [ds['time'].values]})

# 使用数据集中存在的时间值
dataset_time = ds['time'].values
#print(dataset_time)


# 选择经纬度范围以及气压层
lat_range = slice(35.5,25.5)# 30.5 - 5, 30.5 + 5
lon_range = slice(122.5,132.5)#127.5 - 5, 127.5 + 5
print(lon_range)
print(lat_range)

pressure_levels = np.arange(50, 1001, 50)
#print(pressure_levels)


# 提取相关数据time=dataset_time,
temperature_data = ds['t'].sel( latitude=lat_range, longitude=lon_range, level=pressure_levels)
print(temperature_data)
# 绘制立体图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(temperature_data.longitude, temperature_data.latitude)
print(X,Y)

Z = temperature_data.level.values.reshape(-1, 1)




for i, level in enumerate(pressure_levels):
    temp_data = temperature_data.sel(level=level).values
    ax.contourf(X, Y, temp_data,  zdir='z',offset=level, alpha=0.5, cmap=cm.coolwarm, extend3d=True)# exten3d z延续

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Pressure (hPa)')
ax.set_title('Typhoon Warm Core Structure')


ax.set_box_aspect([1, 1, 0.5]) #设置x y z坐标轴比例 %


#ax.set_zlim(900, 100)
ax.view_init(elev=6, azim=90)  # elev仰角俯角 azim转向

# 设置z轴刻度
ax.set_zticks(np.arange(100, 1001, 100))

# 调整刻度大小和其他属性
ax.tick_params(axis='z', labelsize=8, pad=3)



plt.show()
