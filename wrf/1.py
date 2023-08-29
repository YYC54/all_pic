import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 打开nc文件
data = nc.Dataset('/public/home/lihf_hx/yyc/WRF/MYNN/wrfout_d02_2012-07-21_00:00:00')

rain_grid = data.variables['RAINNC'][:]
rain_conv = data.variables['RAINC'][:]
rain = rain_grid + rain_conv


# 计算累积降水
rain_cumulative = rain[-1,:,:] - rain[0,:,:]  # 最后一个时次的降水减第一个时次的降水

# 获取经纬度数据
lon = data.variables['XLONG'][0,:,:]
lat = data.variables['XLAT'][0,:,:]


# 创建地图
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# 添加省级行政区划
provinces = cfeature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lines',
                scale='50m',
                facecolor='none')
ax.add_feature(provinces, edgecolor='black')

# levels = [0, 1, 25, 80, np.max(rain_cumulative)],levels = levels
# 绘制累积降水分布图
contour = ax.contourf(lon, lat, rain_cumulative, transform=ccrs.PlateCarree())

# 添加颜色条
fig.colorbar(contour, ax=ax, orientation='vertical', label='累计降水 (mm)')

# 添加网格线
ax.gridlines(draw_labels=True)

# 添加标题
ax.set_title('7.21 24h累计降水（MYNN方法）')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# 保存图像为文件
plt.savefig('/public/home/lihf_hx/yyc/WRF/图/MYNN/24h.jpg')

plt.show()
