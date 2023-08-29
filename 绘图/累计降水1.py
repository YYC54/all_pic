import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import re
from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker

def get_files(folder, start_date):
    files = []
    pattern = re.compile(f'{start_date}.*_rain.nc')

    for file in os.listdir(folder):
        if pattern.match(file):
            files.append(os.path.join(folder, file))
    print(files)
    return sorted(files)


def calc_accumulated_rain(files, accum_intervals):
    lon_range = slice(90, 93)
    lat_range = slice(29, 31)

    accum_rain = []
    for interval in accum_intervals:
        interval_files = files[:interval]
        if len(interval_files) == 1:
            with xr.open_dataset(interval_files[0]) as ds:
                rain_sum = ds['rain'].sel(lon=lon_range, lat=lat_range)
        else:
            with xr.open_mfdataset(interval_files, combine='by_coords') as ds:
                rain_sum = ds['rain'].sum(dim='time').sel(lon=lon_range, lat=lat_range)
        accum_rain.append(rain_sum)
    return accum_rain


def make_colormap():
    colors = ['lightgreen', 'green', 'dodgerblue', 'darkblue']
    n_bins = [3] * (len(colors) - 1) + [1]
    cmap_name = 'white_green_lightblue_darkblue'
    cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)
    norm = mcolors.BoundaryNorm(np.arange(0, len(colors) + 1), cmap.N)
    return cmap, norm


cmap, norm = make_colormap()
color_levels = {
    3: {'bounds': [ 0.1, 3.0, 10.0, 20.0], 'colors': cmap, 'norm': norm},
    6: {'bounds': [ 0.1, 4.0, 13.0, 25.0], 'colors': cmap, 'norm': norm},
    12: {'bounds': [ 0.1, 5.0, 15.0, 30.0], 'colors': cmap, 'norm': norm},
    24: {'bounds': [ 0.1, 10.0, 25.0, 50.0], 'colors': cmap, 'norm': norm}
}



class CustomLongitudeFormatter(LongitudeFormatter):
    def __call__(self, x, pos=None):
        return f"{abs(x):g}°{'E' if x >= 0 else 'W'}".replace('°', '')


class CustomLatitudeFormatter(LatitudeFormatter):
    def __call__(self, x, pos=None):
        return f"{abs(x):g}°{'N' if x >= 0 else 'S'}".replace('°', '')


def plot_rain_maps(accum_rain, intervals):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    axes = axes.flatten()

    for i, (ax, rain_map) in enumerate(zip(axes, accum_rain)):
        ax.set_title(f'rain in {intervals[i]} hours', fontsize = 18)
        ax.coastlines()

        # 自定义网格线和刻度标签格式
        gl = ax.gridlines(draw_labels=True, xlocs=mticker.FixedLocator(range(90, 93, 1)),
                          ylocs=mticker.FixedLocator(range(28, 32, 1)))
        gl.xformatter = CustomLongitudeFormatter()
        gl.yformatter = CustomLatitudeFormatter()
        gl.xlabel_style = {'size': 11}
        gl.ylabel_style = {'size': 11}



        ax.set_extent([90, 93, 29, 31], crs=ccrs.PlateCarree())

        
        rain_data = gaussian_filter(rain_map, sigma=3)

        bounds = color_levels[intervals[i]]['bounds']
        cmap = color_levels[intervals[i]]['colors']
        cmap.set_under('white', 0)
        cmap.set_over('darkblue', 1)

        norm = plt.Normalize(bounds[0], bounds[-1])
        rain_plot = ax.contourf(rain_map.lon, rain_map.lat, rain_data, levels=bounds, extend='both',
                                transform=ccrs.PlateCarree(), cmap=cmap, norm=norm)

       
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("bottom", size="5%", pad=0.3, axes_class=plt.Axes)
        fig.colorbar(rain_plot, cax=cax, orientation='horizontal', extend='max')

        lhasa_lon = 91.12
        lhasa_lat = 29.65

        ax.scatter(lhasa_lon, lhasa_lat, marker='o', color='red', zorder=10, label='Lhasa')
        ax.annotate('Lhasa', xy=(lhasa_lon, lhasa_lat), xytext=(lhasa_lon + 0.5, lhasa_lat + 0.5), fontsize=15,
                    color='black', arrowprops=dict(facecolor='black', arrowstyle='->'))

    plt.tight_layout()
    plt.savefig('累计降水',dpi = 300)
    plt.show()

# 参数设置
folder = '/Users/yanyuchen/绘图/分析场预报场/降水'  
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
