import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np

# 读取nc文件
file_path = "/Users/yanyuchen/绘图/分析场预报场/分析场/2017062106_u.nc"
dataset = nc.Dataset(file_path)

# 获取U风、经度和纬度数据
u_wind = dataset.variables["u"][:]

file_path = "/Users/yanyuchen/绘图/分析场预报场/分析场/2017062106_v.nc"
dataset = nc.Dataset(file_path)

# 获取V风数据
v_wind = dataset.variables["v"][:]


file_path = "/Users/yanyuchen/绘图/分析场预报场/分析场/2017062106_t.nc"
dataset = nc.Dataset(file_path)

temperature = dataset.variables["t"][:]





lons = dataset.variables["lon"][:]
lats = dataset.variables["lat"][:]

# 创建网格
lon_grid, lat_grid = np.meshgrid(lons, lats)

# 选择一个特定的高度层
height_level = 10
u_wind_h = u_wind[height_level, :, :]
v_wind_h = v_wind[height_level, :, :]
temperature_h = temperature[height_level, :, :]

# 降采样因子
sampling_factor = 15


# 对数据进行降采样
lon_grid_sampled = lon_grid[::sampling_factor, ::sampling_factor]
lat_grid_sampled = lat_grid[::sampling_factor, ::sampling_factor]
u_wind_sampled = u_wind_h[::sampling_factor, ::sampling_factor]
v_wind_sampled = v_wind_h[::sampling_factor, ::sampling_factor]
temperature_sampled = temperature_h[::sampling_factor, ::sampling_factor]





# 绘制风矢图和温度等值线
fig, ax = plt.subplots(figsize=(10, 6))
quiver = ax.quiver(lon_grid_sampled, lat_grid_sampled, u_wind_sampled, v_wind_sampled, scale=400)
contour = ax.contour(lon_grid_sampled, lat_grid_sampled, temperature_sampled, levels=20, colors='k')  # 修改 levels 参数以改变等值线数量

quiver = ax.quiver(lon_grid_sampled, lat_grid_sampled, u_wind_sampled, v_wind_sampled, scale=400)

# 添加相关标签和标题
ax.set_title("风矢图 (U风 & V风) - 高度层 {} - 降采样因子 {}".format(height_level, sampling_factor))
ax.set_xlabel("经度")
ax.set_ylabel("纬度")

# 显示图表
plt.show()