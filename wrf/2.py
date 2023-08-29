import salem
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
fn = "/public/home/lihf_hx/yyc/WRF/MYNN/wrfout_d02_2012-07-21_00:00:00"
ds = salem.open_wrf_dataset(fn)
pcp = ds.RAINC + ds.RAINNC

rgb = ([237, 237, 237], [209, 209, 209], [173, 173, 173], [131, 131, 131],
       [93, 93, 93], [151, 198, 223], [111, 176, 214], [49, 129, 189],
       [26, 104, 174], [8, 79, 153], [62, 168, 91], [110, 193, 115],
       [154, 214, 149], [192, 230, 185], [223, 242, 217], [255, 255, 164],
       [255, 243, 0], [255, 183, 0], [255, 123, 0], [255, 62, 0],
       [255, 2, 0], [196, 0, 0], [136, 0, 0],
       )
clors = np.array(rgb) / 255.
clevs = [0.1, 1, 2, 5, 7.5, 10, 13, 16, 20, 25, 30, 35, 40, 50, 60,
         70, 80, 90, 100, 125, 150, 175, 200, 250
         ]

myproj = ccrs.PlateCarree()
fig = plt.figure(figsize=(16, 9.6), dpi=600)
ax = fig.add_subplot(111, projection=myproj)

cf = ax.contourf(pcp.lon, pcp.lat, pcp.isel(time=0), clevs, colors=clors, transform=myproj)
cb_cf = fig.colorbar(cf, ax=ax, ticks=clevs, shrink=.65)

# ax.add_geometries(Reader('/home/mw/input/shp4847/province_9south.shp').geometries(),
#                   crs=myproj, facecolor='none', edgecolor='k', linewidth=1)
provinces = cfeature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lines',
                scale='50m',
                facecolor='none')
ax.add_feature(provinces, edgecolor='black')

ax.set_title('累计降水')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# 保存图像为文件
plt.savefig('22.jpg')

plt.show()