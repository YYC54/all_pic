import os
import numpy as np
from pyhdf.SD import SD, SDC
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def read_hdf4_file(filepath, dataset_name):
    hdf_file = SD(filepath, SDC.READ)
    dataset = hdf_file.select(dataset_name)
    data = dataset.get()
    return data


def clean_data(data, fill_value):
    cleaned_data = np.where(data == fill_value, np.nan, data)
    return cleaned_data


def main():
    folder_path = '/Users/yanyuchen/气溶胶散点图/Merry-2'  #文件夹在这里改
    dataset_name = 'DUEXTTAU'
    fill_value = 9.9999999E14

    file_list = [f for f in os.listdir(folder_path) if f.endswith('.hdf')]


    min_lon, max_lon = 73, 86
    min_lat, max_lat = 35, 42

    tarim_data_sum = None
    file_count = 0

    for file in file_list:
        file_path = os.path.join(folder_path, file)
        print(file_path)
        data = read_hdf4_file(file_path, dataset_name)
        cleaned_data = clean_data(data, fill_value)


        lon_data = read_hdf4_file(file_path, 'XDim:EOSGRID')
        lat_data = read_hdf4_file(file_path, 'YDim:EOSGRID')

       
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

    average_tarim_data = tarim_data_sum / file_count


    plt.figure(figsize=(10, 9))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS,linestyle=':') #
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())


    c = ax.contourf(lon_grid, lat_grid, average_tarim_data, cmap='viridis')


    plt.colorbar(c, ax=ax, label='DUEXTTAU Value')

    x_ticks = np.arange(min_lon, max_lon + 1, 1)
    y_ticks = np.arange(min_lat, max_lat + 1, 1)

    ax.set_xticks(x_ticks, crs=ccrs.PlateCarree())
    ax.set_yticks(y_ticks, crs=ccrs.PlateCarree())


    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')


    ax.set_xticklabels([f'{x:.1f}°E' for x in x_ticks], fontsize=10)
    ax.set_yticklabels([f'{y:.1f}°N' for y in y_ticks], fontsize=10)


    plt.title('average_tarim_DUEXTTAU Value')
    plt.savefig("average_tarim_data.png")  #图片名称，保存路径
    plt.show()

if __name__ == "__main__":
    main()
