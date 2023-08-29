import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# 读取原始数据
with open('/Users/yanyuchen/青藏高原dem图/gts_omb_oma_01.txt', 'r') as f:
    raw_data = f.readlines()
    data = []
    for row in raw_data:
        fields = row.split()
        data.append(fields)

    df = pd.DataFrame(data)
    column_names = ['1', 'Column1', 'lat', 'lon', 'height', '5', '6', '7',
                    '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'
                    , '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29']
    df.columns = column_names
    df = df.iloc[:457, :]
    df = df.drop([0])
    df = df.dropna(how='all')
    df = df[df['1'] != '1']
    df = df.reset_index(drop=True)

lon = df['lon'].astype(float).values
lat = df['lat'].astype(float).values
alt = df['height'].astype(float).values

xi, yi = np.meshgrid(np.linspace(lon.min(), lon.max(), 1000), np.linspace(lat.min(), lat.max(), 1000))

# 双线性插值
zi = griddata((lon, lat), alt, (xi, yi), method='linear')
zi = np.nan_to_num(zi)
#mask = np.ma.make_mask(zi,-9999), nan=-9999

# 使用 contourf 绘制高程图
cset = plt.contourf(xi, yi, zi, 8, cmap='gray_r')

# 添加 colorbar
cbar = plt.colorbar(cset, orientation='horizontal', extend='both', extendfrac=0.1)

# 设置 colorbar 标记的位置和标签
cbar.set_ticks(np.linspace(zi.min(), zi.max(), 5))
cbar.set_ticklabels([f'{val:.0f}' for val in np.linspace(zi.min(), zi.max(), 5)])

# 显示图像
plt.title('Digital Elevation Model')
plt.savefig('11_contourf_no_shading')
plt.show()
