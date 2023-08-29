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
    print(df['7'])


lon = df['lon'].astype(float).values
lat = df['lat'].astype(float).values
alt = df['height'].astype(float).values
var_7 = df['7'].astype(float).values
# 增加插值点数量
# num_points = 10000
# xi, yi = np.meshgrid(np.linspace(lon.min(), lon.max(), num_points), np.linspace(lat.min(), lat.max(), num_points))
#
# # 插值
# zi = griddata((lon, lat), alt, (xi, yi), method='linear')
# zi = np.nan_to_num(zi)
#
# # 画图
# plt.imshow(zi, cmap='gray_r', extent=[lon.min(), lon.max(),lat.min(),  lat.max()])  # 使用 terrain 色彩映射增加对比度
#
# # 添加 colorbar
# cbar = plt.colorbar(orientation='horizontal', extend='both', extendfrac=0.1)
#
# #  colorbar 标记的位置和标签
# cbar.set_ticks(np.linspace(zi.min(), zi.max(), 5))
# cbar.set_ticklabels([f'{val:.0f}' for val in np.linspace(zi.min(), zi.max(), 5)])

count_blue = 0
count_red = 0

for i, value in enumerate(var_7):
    if value >= 0:
        count_blue += 1
        plt.plot(lon[i], lat[i], 'bo', markersize=2, markerfacecolor='none')
    else:
        count_red += 1
        plt.plot(lon[i], lat[i], 'ro', markersize=2, markerfacecolor='none')



x_ticks = np.arange(min(lon), max(lon)+1, 5)
y_ticks = np.arange(min(lat), max(lat)+1, 2)

plt.xticks(x_ticks, [f'{x:.0f}°E' for x in x_ticks],fontsize = 12)
plt.yticks(y_ticks, [f'{y:.0f}°N' for y in y_ticks],fontsize = 10)





# 显示图像
plt.title(f'QC_good:{count_blue}   QC_bad:{count_red}   Missing:0')
plt.savefig('1')
plt.show()
