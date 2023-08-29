import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress
import dask

# 读取nc文件
nc_file = '/Users/yanyuchen/绘图/青藏高原数据处理/output.nc'
ds = xr.open_dataset(nc_file, chunks={'time': 100, 'lat': 10, 'lon': 10})


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


spring_data = precip_data.sel(time=precip_data['time.season'] == 'DJF') # 'MAM' chun'JJA'xia 'SON'qiu 'DJF'don
spring_start_year = 1992
spring_end_year = 2020
spring_precip_data = spring_data.sel(time=slice(f'{spring_start_year-1 }-12-01', f'{spring_end_year}-02-28')) # 冬季的画start year需要-1


# 对每个网格单元格计算每年的降水天数
annual_rainy_days = (spring_precip_data > 0).groupby('time.year').sum('time')


#print(annual_rainy_days)
# 计算每年整个区域的降水天数
total_annual_rainy_days = annual_rainy_days.mean(dim=['lat', 'lon'])

total_annual_rainy_days = total_annual_rainy_days.compute()

# 平滑折线
window_size = 9
total_annual_rainy_days_smoothed = savgol_filter(total_annual_rainy_days, window_size, 3)

# 绘制年降水天数折线图
plt.figure(figsize=(12, 6))
plt.plot(total_annual_rainy_days.year, total_annual_rainy_days_smoothed, label='Annual Rainy Days', linewidth=2)
plt.xlabel('Year')
plt.ylabel('Total Rainy Days')
plt.title('(d)')
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
fit = np.polyfit(total_annual_rainy_days.year, total_annual_rainy_days_smoothed, deg=1)
fit_func = np.poly1d(fit)
plt.plot(total_annual_rainy_days.year, fit_func(total_annual_rainy_days.year),'--')

slope, intercept, r_value, p_value, std_err = linregress(total_annual_rainy_days.year, total_annual_rainy_days_smoothed)
plt.text(0.05, 0.95, f'R-squared: {r_value**2:.2f}\nFit: y = {fit[0]:.2f}x + {fit[1]:.2f}', transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='grey', alpha=0.8), verticalalignment='top')

#plt.grid()
plt.legend()

plt.savefig('冬总降水天数折线图')
plt.show()








