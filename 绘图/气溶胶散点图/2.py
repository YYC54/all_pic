import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import netCDF4
from scipy.interpolate import griddata

def extract_region(data, lats, lons, lat_bounds, lon_bounds):
    lat_indices = np.where((lats >= lat_bounds[0]) & (lats <= lat_bounds[1]))[0]
    lon_indices = np.where((lons >= lon_bounds[0]) & (lons <= lon_bounds[1]))[0]
    return data[np.ix_(lat_indices, lon_indices)]

# 读取光学厚度数据
aod_filename = '/Users/yanyuchen/气溶胶散点图/Merry-2/MERRA2_100.tavgM_2d_aer_Nx.198201.SUB.hdf'
aod_file = SD(aod_filename, SDC.READ)
aod_data = aod_file.select('DUEXTTAU')[:]

aod_data = aod_data[0]

ydim_data = aod_file.select('YDim:EOSGRID')[:]
xdim_data = aod_file.select('XDim:EOSGRID')[:]

# 假设纬度范围为-90到90，经度范围为-180到180
aod_lats = np.linspace(-90, 90, len(ydim_data))
aod_lons = np.linspace(-180, 180, len(xdim_data))

aod_file.end()

# 读取云顶温度数据
ctt_filename = '/Users/yanyuchen/气溶胶散点图/CTO/CTOmm19820101000000219AVPOS01GL.nc'
ctt_file = netCDF4.Dataset(ctt_filename, 'r')
ctt_data = ctt_file.variables['ctt'][0, :, :]
ctt_lats = ctt_file.variables['lat'][:]
ctt_lons = ctt_file.variables['lon'][:]
ctt_file.close()

# 创建AOD数据的网格点坐标
aod_lat_grid, aod_lon_grid = np.meshgrid(aod_lats, aod_lons, indexing='ij')

# 将AOD数据插值到CTT的网格上
aod_data_interp = griddata((aod_lat_grid.flatten(), aod_lon_grid.flatten()), aod_data.flatten(),
                           (ctt_lats[:, None], ctt_lons[None, :]), method='nearest')

# 提取塔里木地区的数据
lat_bounds = (35, 42)
lon_bounds = (74, 86)
aod_region_data_interp = extract_region(aod_data_interp, ctt_lats, ctt_lons, lat_bounds, lon_bounds)
ctt_region_data = extract_region(ctt_data, ctt_lats, ctt_lons, lat_bounds, lon_bounds)

# 将数据展平以便绘制散点图
aod_flat_interp = aod_region_data_interp.flatten()
ctt_flat = ctt_region_data.flatten()

# 创建散点图
plt.scatter(aod_flat_interp, ctt_flat, s=1)

plt.xlabel('Aerosol Optical Depth (AOD)')
plt.ylabel('Cloud Top Temperature (CTT)')
plt.title('AOD vs. CTT Scatter Plot ')

# 显示散点图
plt.show()
