import numpy as np
import xarray as xr
from scipy.signal import detrend
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# 读取nc文件
nc_file = '/Users/yanyuchen/绘图/青藏高原数据处理/output.nc'
ds = xr.open_dataset(nc_file, chunks={'time': 100, 'lat': 10, 'lon': 10})

# 选择经纬度范围
lat_range = [20, 40]
lon_range = [70, 110]

# 根据经纬度范围选择数据
data = ds['tp'].sel(lat=slice(*lat_range), lon=slice(*lon_range))

# 选择时间范围
start_year = 1991
end_year = 2020
data = data.sel(time=slice(f'{start_year}-01-01', f'{end_year}-12-31'))

# 调整数据维度顺序，将时间维度放在第一个位置
data = data.transpose('time', 'lat', 'lon')

# 去除趋势（如果需要）
plateau_data_detrended_np = detrend(data, axis=0)

# 将 NumPy 数组转换回 DataArray
plateau_data_detrended = xr.DataArray(plateau_data_detrended_np, coords=data.coords, dims=data.dims)

# 计算EOF
from eofs.xarray import Eof
solver = Eof(plateau_data_detrended, weights=None)
eofs = solver.eofsAsCorrelation(neofs=3)
pcs = solver.pcs(npcs=3)

# 绘制EOFs和PCs
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})

for i, ax in enumerate(axes[0]):
    eof = eofs.sel(mode=i)
    eof.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='RdBu_r', add_colorbar=False)
    ax.coastlines()
    ax.set_title(f'EOF{i + 1}')

for i, ax in enumerate(axes[1]):
    pc = pcs.sel(mode=i)
    pc.plot(ax=ax)
    ax.set_title(f'PC{i + 1}')

plt.show()
