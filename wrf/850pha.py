import numpy
import cartopy
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from netCDF4 import Dataset
from xarray import DataArray
from wrf import getvar, interplevel, vertcross,vinterp, ALL_TIMES, CoordPair, xy_to_ll, ll_to_xy, to_np, get_cartopy, latlon_coords, cartopy_xlim, cartopy_ylim
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
# file_path = single_wrf_file()
    wrf_file = Dataset(file_path)

    p = getvar(wrf_file, "pressure",timeidx=11)
    z = getvar(wrf_file, "z", units="dm", timeidx=11)
    ua = getvar(wrf_file, "ua", units="kt", timeidx=11)
    va = getvar(wrf_file, "va", units="kt", timeidx=11)
    wspd = getvar(wrf_file, "wspd_wdir", units="kt",timeidx=11)[0,:]

    ht_850 = interplevel(z, p, 850)
    u_850 = interplevel(ua, p, 850)
    v_850 = interplevel(va, p, 850)
    wspd_850 = interplevel(wspd, p, 850)
    lats, lons = latlon_coords(ht_850)
    cart_proj = get_cartopy(ht_850)
    geo_axes = plt.axes(projection=cart_proj)
    fig = plt.figure(figsize=(10,7.5))
    ax = plt.axes(projection=cart_proj)
    states = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')
    geo_axes.add_feature(states, linewidth=1.5, edgecolor='red')
    ax.coastlines('50m', linewidth=0.8)

    levels = numpy.arange(130., 170., 6.)
    contours = plt.contour(to_np(lons),
                              to_np(lats),
                              to_np(ht_850),
                              levels=levels,
                              colors="black",
                              transform=crs.PlateCarree())

    plt.clabel(contours, inline=1, fontsize=10, fmt="%i")

    levels = [1, 5, 10, 15, 20, 25, 30, 35, 40 ,45]
    wspd_contours = plt.contourf(to_np(lons),
                                    to_np(lats),
                                    to_np(wspd_850),
                                    levels=levels,
                                    cmap=get_cmap("rainbow"),
                                    transform=crs.PlateCarree())

    plt.colorbar(wspd_contours, ax=ax, orientation="horizontal", pad=.05, shrink=.75)


    thin = [int(x/10.) for x in lons.shape]
    plt.barbs(to_np(lons[::thin[0], ::thin[1]]),
              to_np(lats[::thin[0], ::thin[1]]),
              to_np(u_850[::thin[0], ::thin[1]]),
              to_np(v_850[::thin[0], ::thin[1]]),
              length=6,transform=crs.PlateCarree())

    # Set the map bounds
    ax.set_xlim(cartopy_xlim(ht_850))
    ax.set_ylim(cartopy_ylim(ht_850))
    ax.gridlines()
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    date_str = filename_dt(file_path)
    plt.title(date_str + ' _12时850hPa气压场和风场（MYJ方法）')

    plt.savefig('/public/home/lihf_hx/yyc/WRF/图/850hpa风场气压场/850hPa气压场和风场_12（MYJ方法)' + date_str + '.jpg')
    plt.show()