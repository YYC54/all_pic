import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import linregress, norm


def mk_test(x):
    n = len(x)
    s = 0
    for k in range(n - 1):
        for j in range(k + 1, n):
            s += np.sign(x[j] - x[k])
    unique_x = np.unique(x)
    g = len(unique_x)
    if n == g:
        var_s = (n * (n - 1) * (2 * n + 5)) / 18
    else:
        tp = np.zeros(unique_x.shape)
        for i in range(len(unique_x)):
            tp[i] = sum(x == unique_x[i])
        var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s == 0:
        z = 0
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    return s, var_s, z

# 读取nc文件
nc_file = '/Users/yanyuchen/绘图/青藏高原数据处理/output.nc'
ds = xr.open_dataset(nc_file, chunks={'time': 100, 'lat': 10, 'lon': 10})

# 选择时间范围
start_year = 1991
end_year = 2020

# 根据时间范围选择数据
precip_data = ds['tp'].sel(time=slice(f'{start_year}-01-01', f'{end_year}-12-31'))

# 对每个网格单元格计算每年的降水总量
annual_precip = precip_data.groupby('time.year').sum('time')

# 计算每年整个区域的降水总量
total_annual_precip = annual_precip.mean(dim=['lat', 'lon'])

total_annual_precip = total_annual_precip.compute()

s, var_s, z = mk_test(total_annual_precip.values)
#print(s)
n = len(total_annual_precip)
ustat_scaled = np.zeros(n)
ubstat_scaled = np.zeros(n)
for i in range(n):
    ustat_scaled[i] = sum(np.sign(total_annual_precip[i] - total_annual_precip[:i]))
    ubstat_scaled[i] = ustat_scaled[i] - i * (n - i) / (n - 1)

    #print(ubstat_scaled)

# 对 UF 和 UB 线进行标准化
ustat_norm = (ustat_scaled - np.mean(ustat_scaled)) / np.std(ustat_scaled)
ubstat_norm = (ubstat_scaled - np.mean(ubstat_scaled)) / np.std(ubstat_scaled)

# 使用 Savitzky-Golay 滤波器平滑 UF 和 UB 线
window_length = 3  # 调整窗口长度以更改平滑程度
polyorder = 2
ustat_smooth = savgol_filter(ustat_norm, window_length, polyorder)
ubstat_smooth = savgol_filter(ubstat_norm, window_length, polyorder)


plt.figure(figsize=(12, 6))
plt.xlabel('Year')
plt.ylabel('Mann-Kendall ')
plt.title(f'Mann-Kendall ({start_year}-{end_year})')
plt.xlim(start_year, end_year)
#plt.ylim(-3, 3)  # 修改 y 轴范围
#plt.ylim(min(ubstat_scaled) - 10, max(ubstat_scaled) + 10)

alpha = 0.05
z_critical = norm.ppf(1 - alpha / 2)
# 添加正负临界值线
plt.axhline(y=z_critical, color='r', linestyle='--', label=f'+{alpha} Critical Value ')
plt.axhline(y=-z_critical, color='r', linestyle='--', label=f'-{alpha} Critical Value ')
plt.axhline(y=0, color='k', linestyle='-', linewidth=1)

# 绘制缩小后的 Z 统计量随时间的变化
#plt.plot(total_annual_precip.year, [z_scaled] * len(total_annual_precip.year), label='Z-value (scaled)', linewidth=3)

# 绘制平滑后的标准化 UF 和 UB 线
plt.plot(total_annual_precip.year, ustat_smooth, label='UF', linewidth=3)
plt.plot(total_annual_precip.year, ubstat_smooth, label='UB', linewidth=3, linestyle='--')

plt.legend()
plt.savefig('年Mann-Kendall检验')
plt.show()






