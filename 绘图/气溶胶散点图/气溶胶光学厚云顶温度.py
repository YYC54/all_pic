import os
import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import netCDF4
import geopandas as gpd
from shapely.geometry import Point

def get_monthly_mean_aod_ctt_within_boundary(aod_filename, ctt_filename, boundary_gdf):
    aod_file = SD(aod_filename, SDC.READ)
    aod_data = aod_file.select('DUEXTTAU')[:]

    aod_data = aod_data[0]

    ydim_data = aod_file.select('YDim:EOSGRID')[:]
    xdim_data = aod_file.select('XDim:EOSGRID')[:]

    aod_lat = np.linspace(-90, 90, len(ydim_data))
    aod_lon = np.linspace(-180, 180, len(xdim_data))

    aod_file.end()

    with netCDF4.Dataset(ctt_filename, 'r') as ctt_file:
        ctt_lat = ctt_file.variables['lat'][:]
        ctt_lon = ctt_file.variables['lon'][:]
        ctt_data = ctt_file.variables['ctt'][:]

    aod_lon_grid, aod_lat_grid = np.meshgrid(aod_lon, aod_lat)
    aod_lat_lon = np.column_stack((aod_lat_grid.ravel(), aod_lon_grid.ravel()))

    aod_points = [Point(lat_lon) for lat_lon in aod_lat_lon]
    aod_within_boundary = [boundary_gdf.contains(point) for point in aod_points]
    aod_data_within_boundary = aod_data.ravel()[aod_within_boundary]

    ctt_lon_grid, ctt_lat_grid = np.meshgrid(ctt_lon, ctt_lat)
    ctt_lat_lon = np.column_stack((ctt_lat_grid.ravel(), ctt_lon_grid.ravel()))

    ctt_points = [Point(lat_lon) for lat_lon in ctt_lat_lon]
    ctt_within_boundary = [boundary_gdf.contains(point) for point in ctt_points]
    ctt_data_within_boundary = ctt_data.ravel()[ctt_within_boundary]

    if aod_data_within_boundary.size != 9.9999999E14:
        aod_mean = np.mean(aod_data_within_boundary)
    else:
        aod_mean = np.nan

    if ctt_data_within_boundary.size != -999:
        ctt_mean = np.mean(ctt_data_within_boundary)
    else:
        ctt_mean = np.nan

    return aod_mean, ctt_mean

boundary_gdf = gpd.read_file('/Users/yanyuchen/气溶胶散点图/tarim_region.shp').iloc[0]['geometry']

aod_folder = '/Users/yanyuchen/气溶胶散点图/Merry-2'
ctt_folder = '/Users/yanyuchen/气溶胶散点图/CTO'

aod_files = sorted(os.listdir(aod_folder))
ctt_files = sorted(os.listdir(ctt_folder))

aod_means = []
ctt_means = []
for aod_file, ctt_file in zip(aod_files, ctt_files):
    aod_filename = os.path.join(aod_folder, aod_file)
    ctt_filename = os.path.join(ctt_folder, ctt_file)
    print(aod_filename)
    print(ctt_filename)
    aod_mean, ctt_mean = get_monthly_mean_aod_ctt_within_boundary(aod_filename, ctt_filename, boundary_gdf)
    aod_means.append(aod_mean)
    ctt_means.append(ctt_mean)

plt.scatter(aod_means, ctt_means, s=20)
plt.xlabel('AOD')
plt.ylabel('CTT')
plt.title('tarim_month_mean_AOD_CTT')

z = np.polyfit(aod_means, ctt_means, 1)
p = np.poly1d(z)  # 生成函数方程

plt.plot(aod_means, p(aod_means), "r")
plt.annotate('y = {:.2f}x + {:.2f}'.format(z[0], z[1]), (0.95, 0.95), xycoords='axes fraction', ha='right', va='top')

path = 'aod_ctt.png'  # 改成你的保存路径
plt.savefig(path, dpi=300)

# 显示散点图
plt.show()


