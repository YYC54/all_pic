import os
import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import netCDF4
import geopandas as gpd
from shapely.geometry import Point
from scipy.interpolate import griddata
from scipy.interpolate import griddata
def extract_region(data, lats, lons, lat_bounds, lon_bounds):
    lat_indices = np.where((lats >= lat_bounds[0]) & (lats <= lat_bounds[1]))[0]
    lon_indices = np.where((lons >= lon_bounds[0]) & (lons <= lon_bounds[1]))[0]
    return data[np.ix_(lat_indices, lon_indices)]
def  get_tarim_basin_mean_aod_ctt(aod_filename,ctt_filename):
    # 读取光学厚度数据

    aod_file = SD(aod_filename, SDC.READ)
    aod_data = aod_file.select('DUEXTTAU')[:]

    aod_data = aod_data[0]

    ydim_data = aod_file.select('YDim:EOSGRID')[:]
    xdim_data = aod_file.select('XDim:EOSGRID')[:]

    aod_lats = np.linspace(-90, 90, len(ydim_data))
    aod_lons = np.linspace(-180, 180, len(xdim_data))

    aod_file.end()

    # 读取云顶温度数据

    ctt_file = netCDF4.Dataset(ctt_filename, 'r')
    ctt_data = ctt_file.variables['ref_liq'][0, :, :]
    ctt_lats = ctt_file.variables['lat'][:]
    ctt_lons = ctt_file.variables['lon'][:]
    ctt_file.close()

    # 将AOD数据插值到CTT的网格上
    aod_lat_grid, aod_lon_grid = np.meshgrid(aod_lats, aod_lons, indexing='ij')
    aod_data_interp = griddata((aod_lat_grid.flatten(), aod_lon_grid.flatten()), aod_data.flatten(),
                               (ctt_lats[:, None], ctt_lons[None, :]), method='nearest')
    lat_bounds = (35, 42)
    lon_bounds = (74, 86)
    aod_region_data_interp = extract_region(aod_data_interp, ctt_lats, ctt_lons, lat_bounds, lon_bounds)
    ctt_region_data = extract_region(ctt_data, ctt_lats, ctt_lons, lat_bounds, lon_bounds)
    aod_mean = np.nanmean(aod_region_data_interp)
    ctt_mean = np.nanmean(ctt_region_data)
    return  aod_mean,ctt_mean

boundary_gdf = gpd.read_file('/Users/yanyuchen/气溶胶散点图/tarim_region.shp').iloc[0]['geometry']

aod_folder = '/Users/yanyuchen/气溶胶散点图/Merry-2'
ctt_folder = '/Users/yanyuchen/气溶胶散点图/LWP'

aod_files = sorted(os.listdir(aod_folder))
ctt_files = sorted(os.listdir(ctt_folder))

aod_means = []
ctt_means = []
for aod_file, ctt_file in zip(aod_files, ctt_files):
    aod_filename = os.path.join(aod_folder, aod_file)
    ctt_filename = os.path.join(ctt_folder, ctt_file)
    print(aod_filename)
    print(ctt_filename)
    aod_mean, ctt_mean = get_tarim_basin_mean_aod_ctt(aod_filename, ctt_filename)
    aod_means.append(aod_mean)
    ctt_means.append(ctt_mean)

plt.scatter(aod_means, ctt_means, s=20)
plt.xlabel('AOD')
plt.ylabel('Ref_Liq')
plt.title('tarim_month_mean_AOD_Ref_Liq')

z = np.polyfit(aod_means, ctt_means, 1)
p = np.poly1d(z)  # 生成函数方程

plt.plot(aod_means, p(aod_means), "r")
plt.annotate('y = {:.2e}x + {:.2e}'.format(z[0], z[1]), (0.95, 0.95), xycoords='axes fraction', ha='right', va='top')

path = 'aod_ref_liq.png'  # 改成你的保存路径
plt.savefig(path, dpi=300)

# 显示散点图
plt.show()


