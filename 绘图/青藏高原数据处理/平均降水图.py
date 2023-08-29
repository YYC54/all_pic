import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 读取nc文件
nc_file = '/Users/yanyuchen/绘图/青藏高原数据处理/output.nc'
ds = xr.open_dataset(nc_file)

# 选择时间范围
start_year = 1991
end_year = 2020

# 根据时间范围选择数据
precip_data = ds['tp'].sel(time=slice(f'{start_year}-01-01', f'{end_year}-12-31'))

# 计算每年的平均降水量
annual_mean_precip = precip_data.groupby('time.year').mean(dim='time')

# 计算30年平均降水量
mean_precip = annual_mean_precip.mean(dim='year')

# 插值以提高分辨率
new_lat = np.arange(mean_precip.lat.min(), mean_precip.lat.max(), 0.25)
new_lon = np.arange(mean_precip.lon.min(), mean_precip.lon.max(), 0.25)
print(new_lat)
print(new_lon)

mean_precip_high_res = mean_precip.interp(lat=new_lat, lon=new_lon, method='cubic')



# 定义青藏高原地区的边界
lon_min, lon_max = 67, 104
lat_min, lat_max = 21, 40

# 创建带有青藏高原地区边界的地图
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# 绘制降水量平均分布图
mean_precip_high_res.plot(ax=ax, cmap='Blues', robust=True, cbar_kwargs={'label': 'Precipitation (mm/day)', 'shrink': 0.5})

# 添加地理特征
ax.add_feature(cfeature.BORDERS, linestyle='-', edgecolor='black')
ax.add_feature(cfeature.COASTLINE, linestyle='-', edgecolor='black')
ax.set_title(f'Average Precipitation from {start_year} to {end_year}')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.show()
