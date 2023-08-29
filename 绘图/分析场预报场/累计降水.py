import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import re

# 读取文件夹中的文件
def get_files(folder, start_date):
    files = []
    pattern = re.compile(f'{start_date}.*_rain.nc')

    for file in os.listdir(folder):
        if pattern.match(file):
            files.append(os.path.join(folder, file))
    print(files)
    return sorted(files)

# 计算累计降水
def calc_accumulated_rain(files, accum_intervals):
    accum_rain = []
    for interval in accum_intervals:
        interval_files = files[:interval]
        if len(interval_files) == 1:
            with xr.open_dataset(interval_files[0]) as ds:
                rain_sum = ds['rain']
        else:
            with xr.open_mfdataset(interval_files, combine='by_coords') as ds:
                rain_sum = ds['rain'].sum(dim='time')
        accum_rain.append(rain_sum)
    return accum_rain


# 绘制降水填色图
def plot_rain_maps(accum_rain, intervals):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    axes = axes.flatten()

    for i, (ax, rain_map) in enumerate(zip(axes, accum_rain)):
        ax.set_title(f'{intervals[i]}h Accumulated Rainfall')
        ax.coastlines()
        ax.gridlines(draw_labels=True)

        rain_plot = rain_map.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='jet', add_colorbar=False)
        fig.colorbar(rain_plot, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)

    plt.tight_layout()
    plt.show()

# 参数设置
folder = '/Users/yanyuchen/绘图/分析场预报场/降水'  # 替换为您的文件夹路径
start_date = '2017062114'
accum_intervals = [3, 6, 12, 24]

# 主函数
def main():
    files = get_files(folder, start_date)
    #print(files)
    accum_rain = calc_accumulated_rain(files, accum_intervals)
    plot_rain_maps(accum_rain, accum_intervals)

if __name__ == '__main__':
    main()
