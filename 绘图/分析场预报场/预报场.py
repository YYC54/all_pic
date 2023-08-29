import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from scipy.ndimage import gaussian_filter

def read_nc(file, value):
    dataset = nc.Dataset(file)
    value = dataset.variables[value][:]
    return value


# 读取nc文件
file_path = "/Users/yanyuchen/绘图/分析场预报场/预报场/2017062116_u.nc"
u_wind = read_nc(file_path, 'u')

file_path = "/Users/yanyuchen/绘图/分析场预报场/预报场/2017062116_v.nc"
v_wind = read_nc(file_path, 'v')

file_path = "/Users/yanyuchen/绘图/分析场预报场/预报场/2017062116_t.nc"
temperature = read_nc(file_path, 't')

file_path = '/Users/yanyuchen/绘图/分析场预报场/预报场/2017062116_p.nc'
pressure = read_nc(file_path, 'p')

file_path = '/Users/yanyuchen/绘图/分析场预报场/预报场/2017062116_rh.nc'
rh = read_nc(file_path, 'rh')
#rh = np.where(rh == 9.96921E36, np.nan, rh)

file_path = "/Users/yanyuchen/绘图/分析场预报场/预报场/2017062116_geopt.nc"
height = read_nc(file_path, 'geopt')


lons = read_nc(file_path, 'lon')
lats = read_nc(file_path, 'lat')
lon_range = (75, 100)
lat_range = (26, 38)

# 筛选经度和纬度的范围
lon_idx = np.where((lons >= lon_range[0]) & (lons <= lon_range[1]))[0]
lat_idx = np.where((lats >= lat_range[0]) & (lats <= lat_range[1]))[0]

# 读取筛选后的经度和纬度
lons = lons[lon_idx]
lats = lats[lat_idx]


u_wind = u_wind[:, lat_idx, :][:, :, lon_idx]
v_wind = v_wind[:, lat_idx, :][:, :, lon_idx]
temperature = temperature[:, lat_idx, :][:, :, lon_idx]
pressure = pressure[:, lat_idx, :][:, :, lon_idx]
height = height[:, lat_idx, :][:, :, lon_idx]

lon_grid, lat_grid = np.meshgrid(lons, lats)

# 目标压力（以Pa为单位）
target_pressure = 400 * 100

# 计算每个网格点的最接近400 hPa的高度层
pressure_diff = np.abs(pressure - target_pressure)
closest_level = np.argmin(pressure_diff, axis=0)

# 插值
u_wind_interp = np.empty_like(lon_grid)
v_wind_interp = np.empty_like(lon_grid)
temperature_interp = np.empty_like(lon_grid)
pressure_interp = np.empty_like(lon_grid)
rh_interp = np.empty_like(lon_grid)
height_interp = np.empty_like(lon_grid)

#rh_interp = rh_interp * 1e14
for i in range(lon_grid.shape[0]):
    for j in range(lon_grid.shape[1]):
        level = closest_level[i, j]
        u_wind_interp[i, j] = u_wind[level, i, j]
        v_wind_interp[i, j] = v_wind[level, i, j]
        temperature_interp[i, j] = temperature[level, i, j]
        pressure_interp[i, j] = pressure[level, i, j]
        rh_interp[i, j] = rh[level, i, j]
        height_interp[i, j] = height[level, i, j]

# 降采样因子
sampling_factor = 20

# 降采样
u_wind_sampled = u_wind_interp[::sampling_factor, ::sampling_factor]
v_wind_sampled = v_wind_interp[::sampling_factor, ::sampling_factor]
temperature_sampled = temperature_interp[::sampling_factor, ::sampling_factor]
pressure_sampled = pressure_interp[::sampling_factor, ::sampling_factor]
rh_sampled = rh_interp[::sampling_factor, ::sampling_factor]


lon_grid_sampled = lon_grid[::sampling_factor, ::sampling_factor]
lat_grid_sampled = lat_grid[::sampling_factor, ::sampling_factor]


height_sampled = height_interp[::sampling_factor, ::sampling_factor]

# 转换压力数据为hPa
pressure_hpa = pressure / 100

pressure_400 = np.where((pressure_hpa >= 395) & (pressure_hpa <= 405), pressure_hpa, np.nan)

# 生成一个与lon_grid和lat_grid相同形状的空数组，用于存储接近400 hPa的压力值
pressure_400_2d = np.empty_like(lon_grid)

# 使用np.nanmean沿axis=0计算压力值的平均值，结果为一个二维数组
pressure_400_2d = np.nanmean(pressure_400, axis=0)
pressure_400_2d_smoothed = gaussian_filter(pressure_400_2d, sigma=1)

sigma = 50  # 根据需要调整平滑参数
height_interp_smoothed = gaussian_filter(height_interp, sigma=sigma)
# 生成在390 hPa到410 hPa之间的均匀分布的等压线级别
#levels = np.linspace(390, 405, 8)

sigma_temp = 2  # Adjust the smoothing parameter as needed
temperature_interp_smoothed = gaussian_filter(temperature_sampled, sigma=sigma_temp)



# 绘制风矢图、温度等值线和400 hPa等压线
fig, ax = plt.subplots(figsize=(10, 6))
lon_min = 75
lon_max = 98
lat_min = 27
lat_max = 37.8
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
levels1 = np.linspace(0, 100, 21) # 21个值，即20个区间YlGnBu jet'、'viridis'、'magma'
# 基于现有的'BuGn'颜色映射创建一个更亮的版本
cmap_brighter = LinearSegmentedColormap.from_list('BuGn_brighter', plt.cm.BuGn(np.linspace(0.00001, 0.9, 256)))

# 使用新的颜色映射绘制填充等值线
contourf_rh = ax.contourf(lon_grid_sampled, lat_grid_sampled, rh_sampled, levels=levels1, cmap=cmap_brighter,alpha=1)
quiver = ax.quiver(lon_grid_sampled, lat_grid_sampled, u_wind_sampled, v_wind_sampled, scale=500)



temp_min = np.floor(np.nanmin(temperature_interp_smoothed))
temp_max = np.ceil(np.nanmax(temperature_interp_smoothed))

temp_levels = np.arange(temp_min, temp_max, 2)
contour_t = ax.contour(lon_grid_sampled, lat_grid_sampled, temperature_interp_smoothed, levels=temp_levels, colors='r', alpha=0.7)
ax.clabel(contour_t, inline=True, fontsize=8, fmt='%1.0f')
# height_levels = np.arange(np.nanmin(height_interp), np.nanmax(height_interp), 500)
# contour_height = ax.contour(lon_grid, lat_grid, height_interp, levels=height_levels, colors='black', linestyles='dashed', alpha=0.5)

height_levels = np.arange(np.nanmin(height_interp_smoothed), np.nanmax(height_interp_smoothed), 30)
contour_height = ax.contour(lon_grid, lat_grid, height_interp_smoothed, levels=height_levels, colors='b', alpha=0.6)
ax.clabel(contour_height, inline=True, fontsize=8, fmt='%1.0f')

cbar = plt.colorbar(contourf_rh, ax=ax)
cbar.set_label("rh (%)")

lhasa_lon = 91.12
lhasa_lat = 29.65

ax.scatter(lhasa_lon, lhasa_lat, marker='o', color='red', zorder=10,label = 'Lhasa')
ax.annotate('Lhasa', xy=(lhasa_lon, lhasa_lat), xytext=(lhasa_lon+0.5, lhasa_lat+0.5), fontsize=15, color='black', arrowprops=dict(facecolor='black', arrowstyle='->'))

ax.set_title('400 hPa forecast field')
ax.set_xlabel("lon")
ax.set_ylabel("lat")

plt.savefig('400 pha Forecast field',dpi = 300)
plt.show()







