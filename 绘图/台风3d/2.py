import netCDF4 as nc
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 用您的nc文件路径替换 "your_nc_file_path.nc"
nc_file = "/Users/yanyuchen/台风3d/Ttemp_soulik.nc"

# 打开nc文件
dataset = nc.Dataset(nc_file)

# 获取变量的值
temperature = dataset.variables["t"]
longitude = dataset.variables["longitude"]
latitude = dataset.variables["latitude"]
level = dataset.variables["level"]

longitude = dataset.variables["longitude"]
print("Minimum longitude:", np.min(longitude[:]))
print("Maximum longitude:", np.max(longitude[:]))
print("Longitude precision:", np.round(np.max(np.diff(longitude[:])), 4))
latitude = dataset.variables["latitude"]
print("Minimum latitude:", np.min(latitude[:]))
print("Maximum latitude:", np.max(latitude[:]))
print("Latitude precision:", np.round(np.max(np.diff(latitude[:])), 4))




# 获取以(124.5, 17.5)为中心的10°x10°范围内的经纬度索引
center_lon, center_lat = 124.5, 17.5   # -0.25
min_lon, max_lon = 122.5, 132.5  # 122.5-132.5
min_lat, max_lat = 25.5, 35.5  # 25.5-35.5

lon_indices = np.where((longitude[:] >= min_lon) & (longitude[:] <=max_lon ))[0]
lat_indices = np.where((latitude[:] >= max_lat) & (latitude[:] <= min_lat))[0]

print(lat_indices)
print(lon_indices)

if len(lon_indices) > 0 and len(lat_indices) > 0:
    # 截取指定范围内的温度数据
    subset_temperature = temperature[:, lat_indices, lon_indices]

    # 绘制台风暖心立体图
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # 绘制等压线
    for idx, p in enumerate(level[:]):
        if p >= 50 and p <= 1000:
            # 选取特定气压层的温度数据
            temperature_layer = subset_temperature[idx, :, :]
            # 绘制等压线
            contour = ax.contour(longitude[lon_indices], latitude[lat_indices], temperature_layer, levels=10, linewidths=1, colors='k')
            ax.clabel(contour, fontsize=10, inline=1, fmt='%1.0f')

    # 添加地理特征
    ax.add_feature(cfeature.COASTLINE, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linestyle='-', edgecolor='black')

    # 设置地图边界
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

    # 设置标题
    ax.set_title(f"Typhoon Warm Core Cross-Section (50-1000 hPa) at {desired_time_dt}")

    # 显示图像
    plt.show()
else:
    print("Requested longitude and latitude range not found in the dataset.")
