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

WRF_DIRECTORY = "/public/home/lihf_hx/yyc/WRF/YSU"
WRF_FILES = [

            "wrfout_d01_2012-07-21_00:00:00",
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
# _WRF_FILES = multiple_wrf_files()


cross_start = CoordPair(lat=39.55, lon=115.5)
cross_end = CoordPair(lat=39.55, lon=117.25)

file_path = multiple_wrf_files()
wrf_file = [Dataset(x) for x in file_path]


slp = getvar(wrf_file, "slp", timeidx=15)
z = getvar(wrf_file, "z", timeidx=15)
dbz = getvar(wrf_file, "dbz", timeidx=15)
Z = 10**(dbz/10.)
z_cross = vertcross(Z, z, wrfin=wrf_file,
                    start_point=cross_start,
                    end_point=cross_end,
                    latlon=True, meta=True)

dbz_cross = 10.0 * numpy.log10(z_cross)

lats, lons = latlon_coords(slp)
cart_proj = get_cartopy(slp)

fig = plt.figure(figsize=(15,5))
ax_slp = fig.add_subplot(1,2,1,projection=cart_proj)
ax_dbz = fig.add_subplot(1,2,2)

states = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
                             name='admin_1_states_provinces_lines')
land = cfeature.NaturalEarthFeature(category='physical', name='land', scale='50m',
                            facecolor=COLORS['land'])
ocean = cfeature.NaturalEarthFeature(category='physical', name='ocean', scale='50m',
                            facecolor=COLORS['water'])


slp_levels = numpy.arange(950.,1030.,5)
slp_contours = ax_slp.contour(to_np(lons),
                              to_np(lats),
                              to_np(slp),
                              levels=slp_levels,
                              colors="black",
                              zorder=3,
                              transform=crs.PlateCarree())

ax_slp.clabel(slp_contours, fmt="%i")

ax_slp.plot([cross_start.lon, cross_end.lon],
            [cross_start.lat, cross_end.lat],
            color="yellow",
            marker="o",
            zorder=3,
            transform=crs.PlateCarree())


ax_slp.add_feature(ocean)
ax_slp.add_feature(land)
ax_slp.add_feature(states, linewidth=.5, edgecolor="black")


dbz_levels = numpy.arange(-40.,50.,1.)
dbz_contours = ax_dbz.contourf(to_np(dbz_cross), levels=dbz_levels, cmap=get_cmap("jet"))
cb_dbz = fig.colorbar(dbz_contours, ax=ax_dbz)
cb_dbz.ax.tick_params(labelsize=8)


coord_pairs = to_np(dbz_cross.coords["xy_loc"])
x_ticks = numpy.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]

thin = [int(x/5.) for x in x_ticks.shape]
ax_dbz.set_xticks(x_ticks[1::thin[0]])
ax_dbz.set_xticklabels(x_labels[::thin[0]], rotation=45, fontsize=8)


vert_vals = to_np(dbz_cross.coords["vertical"])
v_ticks = numpy.arange(vert_vals.shape[0])

thin = [int(x/8.) for x in v_ticks.shape]
ax_dbz.set_yticks(v_ticks[::thin[0]])
ax_dbz.set_yticklabels(vert_vals[::thin[0]], fontsize=8)

ax_dbz.set_xlabel("维度，经度", fontsize=12)
ax_dbz.set_ylabel("高度 (m)", fontsize=12)

ax_slp.set_title("7-21_15时海平面气压场_YSU方法(hPa)", {"fontsize" : 14})
ax_dbz.set_title("7-21_15时雷达反射率_YSU方法(dBZ)", {"fontsize" : 14})

plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
plt.savefig('33333')
plt.show()