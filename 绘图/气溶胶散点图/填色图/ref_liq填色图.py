import os
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4 as nc

def read_nc_file(filepath, dataset_name):
    nc_file = nc.Dataset(filepath, "r")
    data = nc_file.variables[dataset_name]
    return data


def clean_data(data, fill_value):
    cleaned_data = np.where((data <= fill_value), np.nan, data)
    return cleaned_data

def main():
    folder_path = '/Users/yanyuchen/气溶胶散点图/填色图/春'  # 文件夹在这里改
    dataset_name = 'ref_liq'
    fill_value = 0

    file_list = [f for f in os.listdir(folder_path) if f.endswith('.nc')]

    min_lon, max_lon = 73, 86
    min_lat, max_lat = 35, 42

    tarim_data_sum = None
    file_count = 0

    for file in file_list:
        file_path = os.path.join(folder_path, file)
        print(file_path)
        data_var = read_nc_file(file_path, dataset_name)
        nc_attrs = data_var.ncattrs()
        scale_factor = getattr(data_var, 'scale_factor', 1)
        add_offset = getattr(data_var, 'add_offset', 0.0)
        data = data_var[:] * scale_factor + add_offset
        cleaned_data = clean_data(data, getattr(data_var, '_FillValue'))


        lon_data = read_nc_file(file_path, 'lon')
        lat_data = read_nc_file(file_path, 'lat')

        lon_grid, lat_grid = np.meshgrid(lon_data, lat_data)

        tarim_mask = (
                (lon_grid >= min_lon) & (lon_grid <= max_lon) &
                (lat_grid >= min_lat) & (lat_grid <= max_lat)
        )
        tarim_data = np.where(tarim_mask, cleaned_data, np.nan)

        tarim_data_2d = np.nanmean(tarim_data, axis=0)

        if tarim_data_sum is None:
            tarim_data_sum = tarim_data_2d
        else:
            tarim_data_sum += tarim_data_2d

        file_count += 1

    average_tarim_data = (tarim_data_sum / file_count)
    print(file_count)
    #print(tarim_data_2d)
    print(tarim_data_sum)
    plt.figure(figsize=(10, 9))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')  #
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

    # min_value, max_value = 0, 0.1
    # num_levels = 21
    # color_levels = np.linspace(min_value, max_value, num_levels)
    # print(color_levels)
    # c = ax.contourf(lon_grid, lat_grid, average_tarim_data, levels=color_levels, cmap='viridis')
    #
    # plt.colorbar(c, ax=ax, label='ref_liq Value')

    average_tarim_data = np.nan_to_num(average_tarim_data, nan=0)

    c = ax.contourf(lon_grid, lat_grid, average_tarim_data, cmap='viridis')

    plt.colorbar(c, ax=ax, label='ref_liq Value')

    x_ticks = np.arange(min_lon, max_lon + 1, 1)
    y_ticks = np.arange(min_lat, max_lat + 1, 1)

    ax.set_xticks(x_ticks, crs=ccrs.PlateCarree())
    ax.set_yticks(y_ticks, crs=ccrs.PlateCarree())

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    ax.set_xticklabels([f'{x:.1f}°E' for x in x_ticks], fontsize=10)
    ax.set_yticklabels([f'{y:.1f}°N' for y in y_ticks], fontsize=10)




    plt.title('average_tarim_ref_liq Value')
    plt.savefig("average_tarim_ref_liq_data.png")  # 图片名称，保存路径
    plt.show()


if __name__ == "__main__":
    main()
