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

WRF_DIRECTORY = "/public/home/lihf_hx/yyc/WRF/MYJ"
WRF_FILES = [

            "wrfout_d01_2012-07-20_00:00:00",
            "wrfout_d01_2012-07-21_00:00:00",
             'wrfout_d01_2012-07-22_00:00:00',
             ]

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


file_path = multiple_wrf_files()
wrf_file = [Dataset(f) for f in file_path]
slp_all = getvar(wrf_file, "slp", timeidx=ALL_TIMES)
cart_proj = get_cartopy(slp_all)
fig = plt.figure(figsize=(10,7.5))
ax_slp = plt.axes(projection=cart_proj)
states = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                             name='admin_1_states_provinces_lines')
land = cfeature.NaturalEarthFeature(category='physical', name='land', scale='50m',
                                    facecolor=COLORS['land'])
ocean = cfeature.NaturalEarthFeature(category='physical', name='ocean', scale='50m',
                                     facecolor=COLORS['water'])
slp_levels = numpy.arange(950.,1030.,5.)
num_frames = slp_all.shape[0]

def animate(i):
    ax_slp.clear()
    slp = slp_all[i,:]

    lats, lons = latlon_coords(slp)

    ax_slp.add_feature(ocean)
    ax_slp.add_feature(land)
    ax_slp.add_feature(states, linewidth=.5, edgecolor="black")
    slp_contours = ax_slp.contour(to_np(lons),
                                  to_np(lats),
                                  to_np(slp),
                                  levels=slp_levels,
                                  colors="black",
                                  zorder=5,
                                  transform=crs.PlateCarree())
    ax_slp.clabel(slp_contours, fmt="%i")
    ax_slp.set_xlim(cartopy_xlim(slp))
    ax_slp.set_ylim(cartopy_ylim(slp))
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    plt.title('2012年7月20日至22日海平面压力随时间的变化（MYJ）')
    return ax_slp


ani = FuncAnimation(fig, animate, num_frames, interval=500)
HTML(ani.to_jshtml())
html = ani.to_jshtml()
with open('MYJ.html', 'w') as f:
    f.write(html)

