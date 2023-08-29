import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
from matplotlib.colors import LightSource

# 读取原始数据
with open('/Users/yanyuchen/青藏高原dem图/gts_omb_oma_01.txt', 'r') as f:
    raw_data = f.readlines()
    # 遍历每一行，将其分割为字段列表
    data = []
    for row in raw_data:
        fields = row.split()
        data.append(fields)

    # 使用 Pandas 将字段列表转换为 DataFrame
    df = pd.DataFrame(data)

    # 重命名列，使其具有更具描述性的名称
    column_names = ['1','Column1', 'lat', 'lon', 'height','5','6','7',
                    '8','9','10','11','12','13','14','15','16','17','18'
                    ,'19','20','21','22','23','24','25','26','27','28','29']
    df.columns = column_names

    df = df.iloc[:457, :]
    df = df.drop([0])
    df = df.dropna(how='all')
    df = df[df['1'] != '1']
    df = df.reset_index(drop=True)

lon = df['lon'].astype(float).values
lat = df['lat'].astype(float).values
alt = df['height'].astype(float).values

m = Basemap(projection='merc', lon_0=(73+104)/2, lat_0=(26+39)/2, resolution='i')
x, y = m(lon, lat)

xi, yi = np.meshgrid(np.linspace(x.min(), x.max(), 10000), np.linspace(y.min(), y.max(), 10000))
#，
# 双线性插值
zi = griddata((x, y), alt, (xi, yi), method='linear')
zi = np.nan_to_num(zi ,-9999)
print(zi)
mask = np.ma.make_mask(zi,-9999)

print(mask)
ls = LightSource(azdeg=315, altdeg=45)

# 使用光源对象将DEM数据的灰度图和光影叠加在一起
rgb = ls.shade(zi, cmap=plt.cm.gray_r, blend_mode='soft', vert_exag=1.0)

im = plt.imshow(rgb, cmap='gray', extent=[73, 104, 26, 39]) #, origin='lower'

# 添加 colorbar
cbar = plt.colorbar(im,orientation='horizontal', extend='both', extendfrac=0.1)

# 设置 colorbar 标记的位置和标签
cbar.set_ticks(np.linspace(zi.min(), zi.max(), 5))
cbar.set_ticklabels([f'{val:.0f}' for val in np.linspace(zi.min(), zi.max(), 5)])

# 显示图像
plt.title('Digital Elevation Model')
plt.savefig('11')
plt.show()
