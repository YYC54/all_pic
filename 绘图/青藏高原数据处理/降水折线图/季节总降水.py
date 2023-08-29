import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress

# 读取nc文件
nc_file = '/Users/yanyuchen/绘图/青藏高原数据处理/output.nc'
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
#print(precip_data)
# 选择春季的时间范围
spring_data = precip_data.sel(time=precip_data['time.season'] == 'DJF') # 'MAM' chun'JJA'xia 'SON'qiu 'DJF'don
spring_start_year = 1992
spring_end_year = 2020
spring_precip_data = spring_data.sel(time=slice(f'{spring_start_year -1 }-12-01', f'{spring_end_year}-2-28')) # 冬季的画start year需要-1

# 对每个网格单元格计算每年的降水总量
#annual_precip = spring_precip_data.groupby('time.year').sum('time')
annual_precip = spring_precip_data.resample(time='AS-DEC').sum('time')

# 计算每年整个区域的降水总量
total_annual_precip = annual_precip.mean(dim=['lat', 'lon'])

# 平滑折线
window_size = 9
total_annual_precip_smoothed = savgol_filter(total_annual_precip, window_size, 3)
print(total_annual_precip_smoothed)
# 绘制年降水总量折线图
plt.figure(figsize=(12, 6))
plt.plot(total_annual_precip.time.dt.year, total_annual_precip_smoothed, label='observation line', linewidth=2) # 添加了time.dt total_annual_precip.time.dt.year所有
plt.xlabel('Year')
plt.ylabel('Total Precipitation (mm)')
plt.title('(d)')

# 设置 x 轴范围
plt.xlim(spring_start_year, spring_end_year)


# 禁用 y 轴的科学计数法
plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)

# 添加拟合函数和 R 平方
fit = np.polyfit(total_annual_precip.time.dt.year, total_annual_precip_smoothed, deg=1)
fit_func = np.poly1d(fit)
plt.plot(total_annual_precip.time.dt.year, fit_func(total_annual_precip.time.dt.year), '--',label= 'trend line')

slope, intercept, r_value, p_value, std_err = linregress(total_annual_precip.time.dt.year, total_annual_precip_smoothed)
plt.text(0.03, 0.7, f'R-squared: {r_value**2:.6f}\nFit: y = {fit[0]:.6f}x + {fit[1]:.6f}', transform=plt.gca().transAxes, bbox=dict(facecolor='None', edgecolor='None', alpha=0.8))#, verticalalignment='top'

#plt.grid()
plt.legend()


plt.savefig('/Users/yanyuchen/绘图/青藏高原数据处理/降水折线图/冬季降水折线图')
plt.show()

