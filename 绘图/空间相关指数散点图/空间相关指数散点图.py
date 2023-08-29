import os
import glob
import xarray as xr
import numpy as np
from scipy.interpolate import interp2d

# def interpolate_t2m_to_air_data(t2m_data, air_data):
#     t2m_data_interp = t2m_data.interp(lat=air_data.lat, lon=air_data.lon, method='linear')
#     return t2m_data_interp
def interpolate_t2m_to_air_data(t2m_data, air_data_selected):

    time_range = slice(
        max(t2m_data.time.min(), air_data_selected.time.min()),
        min(t2m_data.time.max(), air_data_selected.time.max())
    )

    print(f"air_data_selected time coords: {air_data_selected.time}")
    print(f"t2m_data time coords: {t2m_data.time}")


    t2m_data_interp = t2m_data.sel(time=time_range).interp(
        lat=air_data_selected.lat, lon=air_data_selected.lon, method='linear'
    )
    return t2m_data_interp

''''''''''''#数据文件夹路径t2m

folders = [
    '/Users/yanyuchen/空间相关指数散点图/NCC_CSM11_1991-1993',
    '/Users/yanyuchen/空间相关指数散点图/NCC_CSM11_1994-2005',
    '/Users/yanyuchen/空间相关指数散点图/NCC_CSM11_2006-2013',
    '/Users/yanyuchen/空间相关指数散点图/NCC_CSM11_2014-2020'
]
''''''''''''''''''
nc_files = []

for folder in folders:
    os.chdir(folder)
    for file in glob.glob("MODESv2_ncc_csm11_*_monthly_em.nc"):
        nc_files.append(os.path.abspath(file))

your_variable_name = 't2m'
reference_file = '/Users/yanyuchen/空间相关指数散点图/reanalysis/NCEP_DOE_Reanalysis_2/air.2m.mon.mean.nc'#实测文件路径air



data = []

for file in nc_files:
    try:
        with xr.open_dataset(file) as ds:

            ds = ds.assign_coords(time=lambda ds: ds.time.astype("datetime64[D]"))


            assert np.all(np.diff(ds.time.values.astype(np.int64)) > 0), f"时间坐标不是单调递增的：{file}"

            variable_data = ds[your_variable_name]
            data.append(variable_data)
    except KeyError as e:
        print(f"在文件 {file} 中找不到变量 {your_variable_name}。")
        print(f"错误信息: {e}")
        print("跳过此文件。")
        continue

if data:
    data_combined = xr.concat(data, dim='time')
    print(data_combined)
else:
    print("未找到任何可用的数据。")

with xr.open_dataset(reference_file) as ds_ref:
    air_data = ds_ref['air']

for file, t2m_data in zip(nc_files, data_combined):

    start_year, start_month = int(file[-20:-16]), int(file[-16:-14])
    # print(start_year)
    # print(start_month)
    end_year = start_year + 1

    air_data_selected = air_data.sel(time=slice(f"{start_year}-{start_month:02d}-01", f"{end_year}-{start_month:02d}-01"))
    air_data_selected = np.squeeze(air_data_selected)
    #print(air_data_selected.shape)


    t2m_data_interp = interpolate_t2m_to_air_data(t2m_data, air_data_selected)
    #print(t2m_data_interp.shape)
    air_data_selected = air_data_selected.sel(lat=t2m_data_interp.lat, lon=t2m_data_interp.lon)
    # 将 t2m 数据和 air 数据拉平
    t2m_flat = t2m_data_interp.values.reshape(t2m_data_interp.shape[0], -1)
    air_data_flat = air_data_selected.values.reshape(air_data_selected.shape[0], -1)

    # 时间维度上的形状如果不匹配截断较长的数组
    if t2m_flat.shape[0] != air_data_flat.shape[0]:
        min_len = min(t2m_flat.shape[0], air_data_flat.shape[0])
        t2m_flat = t2m_flat[:min_len]
        air_data_flat = air_data_flat[:min_len]
    print(f"t2m_flat shape: {t2m_flat.shape}")
    print(f"air_data_flat shape: {air_data_flat.shape}")

    assert t2m_flat.shape == air_data_flat.shape, f"不匹配的形状：t2m_flat = {t2m_flat.shape}, air_data_flat = {air_data_flat.shape}"

    # 逐个时间步计算空间相关系数
correlations = np.array(
            [np.corrcoef(t2m_flat[i].ravel(), air_data_flat[i].ravel())[0, 1] for i in range(t2m_flat.shape[0])])

print(f"时间范围: {start_year}-{start_month:02d} to {end_year}-{start_month:02d}, 空间相关系数: {correlations}")
