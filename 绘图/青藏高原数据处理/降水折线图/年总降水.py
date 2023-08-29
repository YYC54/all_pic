import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress

# 读取nc文件
nc_file = '/output.nc'
ds = xr.open_dataset(nc_file)


# 选择经纬度范围（根据实际情况设置）
lat_range = [20, 40]
lon_range = [70, 110]

# 根据经纬度范围选择数据
precip_data = ds['tp'].sel(lat=slice(*lat_range), lon=slice(*lon_range))





# 选择时间范围
start_year = 1991
end_year = 2020

# 根据时间范围选择数据
precip_data = ds['tp'].sel(time=slice(f'{start_year}-01-01', f'{end_year}-12-31'))

# 对每个网格单元格计算每年的降水总量
annual_precip = precip_data.groupby('time.year').sum('time')

# 计算每年整个区域的降水总量
total_annual_precip = annual_precip.mean(dim=['lat', 'lon'])

# 平滑折线
window_size = 9
total_annual_precip_smoothed = savgol_filter(total_annual_precip, window_size, 3)

# 绘制年降水总量折线图
plt.figure(figsize=(12, 6))
plt.plot(total_annual_precip.year, total_annual_precip_smoothed, label='Annual Precipitation', linewidth=2)
plt.xlabel('Year')
plt.ylabel('Total Precipitation (mm)')
plt.title(f'Total Annual Precipitation in the Region ({start_year}-{end_year})')
plt.legend()
#plt.grid()

# 设置 x 轴范围
plt.xlim(start_year, end_year)

# 在原点处绘制一条垂直于 x 轴的直线
#plt.axvline(x=start_year, color='grey', linestyle='--')

# 禁用 y 轴的科学计数法
plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)





# 添加拟合函数和 R 平方
fit = np.polyfit(total_annual_precip.year, total_annual_precip_smoothed, deg=1)
fit_func = np.poly1d(fit)
plt.plot(total_annual_precip.year, fit_func(total_annual_precip.year),'--')

slope, intercept, r_value, p_value, std_err = linregress(total_annual_precip.year, total_annual_precip_smoothed)
plt.text(0.05, 0.95, f'R-squared: {r_value**2:.2f}\nFit: y = {fit[0]:.2f}x + {fit[1]:.2f}', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='grey', alpha=0.8), verticalalignment='top')

#plt.grid()
plt.legend()

plt.savefig('年总降水折线图')


plt.show()







