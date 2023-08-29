import numpy
import cartopy
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from netCDF4 import Dataset
from xarray import DataArray
from wrf import getvar, interplevel, vertcross, vinterp, ALL_TIMES, CoordPair, xy_to_ll, ll_to_xy, to_np, get_cartopy, \
    latlon_coords, cartopy_xlim, cartopy_ylim
from matplotlib.animation import FuncAnimation
import cartopy.feature as cfeature
from IPython.display import HTML
import os
import warnings

warnings.filterwarnings('ignore')



def filename_dt(file_path):
    filename = os.path.basename(file_path)
    date_str = filename.split('_')[2]
    return date_str

WRF_DIRECTORY = "/public/home/lihf_hx/yyc/WRF/MYJ"
WRF_FILES = [
    "wrfout_d01_2012-07-20_00:00:00",
    "wrfout_d01_2012-07-21_00:00:00",
    'wrfout_d01_2012-07-22_00:00:00']

_WRF_FILES = [os.path.abspath(os.path.join(WRF_DIRECTORY, f)) for f in WRF_FILES]
for f in _WRF_FILES:
    if not os.path.exists(f):
        raise ValueError("{} does not exist. "
                         "Check for typos or incorrect directory.".format(f))


def single_wrf_file():
    global _WRF_FILES
    return _WRF_FILES[0]


def multiple_wrf_files():
    global _WRF_FILES
    return _WRF_FILES
_WRF_FILES = multiple_wrf_files()
for file_path in _WRF_FILES:
    # file_path = multiple_wrf_files()
    # filename = os.path.basename(file_path)
    wrf_file = Dataset(file_path)

    slp = getvar(wrf_file, "slp", timeidx=12)
    td2 = getvar(wrf_file, "td2", timeidx=12, units="degF")
    u_sfc = getvar(wrf_file, "ua", timeidx=12, units="kt")[12, :]
    v_sfc = getvar(wrf_file, "va", timeidx=12, units="kt")[12, :]

    cart_proj = get_cartopy(slp)
    lats, lons = latlon_coords(slp)

    fig = plt.figure(figsize=(10, 7.5))
    geo_axes = plt.axes(projection=cart_proj)

    states = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')
    geo_axes.add_feature(states, linewidth=1.5, edgecolor='red')
    geo_axes.coastlines('50m', linewidth=0.8, edgecolor='red')

    slp_levels = numpy.arange(980., 1030., 2.5)
    td2_levels = numpy.arange(10., 79., 3.)

    td2_rgb = numpy.array([[181, 82, 0], [181, 82, 0],
                           [198, 107, 8], [206, 107, 8],
                           [231, 140, 8], [239, 156, 8],
                           [247, 173, 24], [255, 189, 41],
                           [255, 212, 49], [255, 222, 66],
                           [255, 239, 90], [247, 255, 123],
                           [214, 255, 132], [181, 231, 148],
                           [156, 222, 156], [132, 222, 132],
                           [112, 222, 112], [82, 222, 82],
                           [57, 222, 57], [33, 222, 33],
                           [8, 206, 8], [0, 165, 0],
                           [0, 140, 0], [3, 105, 3]]) / 255.0

    td2_cmap, td2_norm = from_levels_and_colors(td2_levels, td2_rgb, extend="both")

    slp_contours = plt.contour(to_np(lons),
                               to_np(lats),
                               to_np(slp),
                               levels=slp_levels,
                               colors="black",
                               transform=crs.PlateCarree())

    plt.contourf(to_np(lons), to_np(lats),
                 to_np(td2), levels=td2_levels,
                 cmap=td2_cmap, norm=td2_norm,
                 extend="both",
                 transform=crs.PlateCarree())

    thin = [int(x / 10.) for x in lons.shape]
    plt.barbs(to_np(lons[::thin[0], ::thin[1]]),
              to_np(lats[::thin[0], ::thin[1]]),
              to_np(u_sfc[::thin[0], ::thin[1]]),
              to_np(v_sfc[::thin[0], ::thin[1]]),
              transform=crs.PlateCarree())

    plt.clabel(slp_contours, fmt="%i")
    plt.colorbar(ax=geo_axes, shrink=.86, extend="both", label='相对湿度 (%)')
    # Define Beijing's longitude and latitude
    beijing_lon, beijing_lat = 116.5, 39.9042

    # Add an arrow pointing to Beijing and annotationarrowstyle="->"
    plt.annotate('北京', xy=(beijing_lon, beijing_lat), xycoords=crs.PlateCarree(),
                 xytext=(-50, 30), textcoords="offset points",
                 arrowprops=dict(facecolor='red', width=5))

    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.xlim(cartopy_xlim(slp))
    plt.ylim(cartopy_ylim(slp))

    date_str = filename_dt(file_path)
    plt.title(date_str + '_12时相对湿度（MYJ方法）')

    plt.savefig('/public/home/lihf_hx/yyc/WRF/图/相对湿度/相对湿度12（MYJ方法)'+date_str+'.jpg')
    plt.show()
