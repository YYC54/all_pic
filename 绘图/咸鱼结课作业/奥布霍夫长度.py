import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.linear_model import Ridge
from scipy.interpolate import make_interp_spline
# 使用 Pandas 读取 CSV 文件并跳过前 4 行
df = pd.read_csv('/Users/yanyuchen/绘图/咸鱼结课作业/1/TOA_2019-03-07_fast(1).csv', delimiter=',', skiprows=3)

# 计算整个数据集的风速平均值
mean_Ux = np.mean(df.iloc[:, 2])
mean_Uy = np.mean(df.iloc[:, 3])
mean_Uz = np.mean(df.iloc[:, 4])

def custom_function(x, a, b, c, d):
    return a * np.sin(b * x + c) + d


# 定义一个函数来计算摩擦速度和潜在温度通量
def compute_u_star_and_flux(row):
    u_prime = row.iloc[2] - mean_Ux
    v_prime = row.iloc[3] - mean_Uy
    w_prime = row.iloc[4] - mean_Uz

    uw = u_prime * w_prime

    u_prime_sq = u_prime ** 2
    w_prime_sq = w_prime ** 2

    u_star = np.sqrt((-uw + np.sqrt(uw ** 2 + u_prime_sq * w_prime_sq)) / 2)

    # 计算潜在温度通量
    e_HMP_01 = row.iloc[12]
    p = row.iloc[10]
    T = row.iloc[7]

    # 计算比湿
    #q = 0.622 * (e_HMP_01 / (ps_7500 - e_HMP_01))

    # 计算潜在温度
    #theta_v = (Tv_CSAT + 273.15) * (1 + 0.61 * q)
    theta_v = T * (1000 / p) ** 0.286

    return u_star, theta_v, w_prime

# 使用 apply 方法计算每一行的摩擦速度和潜在温度，并将结果存储到新的 DataFrame 列中
df['u_star'], df['theta_v'], df['w_prime'] = zip(*df.apply(compute_u_star_and_flux, axis=1))

# 计算滑动窗口平均值
window_size = 2  # 请根据实际情况调整窗口大小
theta_v_rolling_mean = df['theta_v'].rolling(window=window_size).mean()

# 计算 theta_v_prime
df['theta_v_prime'] = df['theta_v'] - theta_v_rolling_mean

# 计算潜在温度通量
df['latent_heat_flux'] = df['theta_v_prime'] * df['w_prime']

# 定义常数
k = 0.4
g = 9.81


# 用观测到的温度代替虚温
Tv = df.iloc[:, 11] + 273.15

# 计算奥布霍夫长度
L = -(df['u_star'] ** 3 * Tv) / (k * g * df['latent_heat_flux'])

# 将奥布霍夫长度添加到 DataFrame 中
df['Obukhov_length'] = L
# 计算奥布霍夫长度的平均值和标准差
# mean_obukhov_length = df['Obukhov_length'].mean()
# std_obukhov_length = df['Obukhov_length'].std()

# 定义异常值阈值，例如平均值加减3倍标准差
threshold_upper = -0.5
threshold_upper1 = 0.5
# 过滤掉异常值
filtered_df = df[(df['Obukhov_length'] > -0.5) & (df['Obukhov_length'] < 0.5)]


print(filtered_df)


x = np.array(filtered_df.index)
y = np.array(filtered_df['Obukhov_length'])
degree = 3

# 将x坐标轴分为200个等距点
x_new = np.linspace(x.min(), x.max(), 48)

# 使用 make_interp_spline 进行插值
spline = make_interp_spline(x, y, k=3)
y_smooth = spline(x_new)

# 绘制折线图和散点图
plt.figure(figsize=(12, 6))
#plt.scatter(x, y, label='Filtered Obukhov Length', s=3)
plt.plot(x_new, y_smooth, label='Fit Line')

plt.xlabel('Time Index')
plt.ylabel('Obukhov Length')
plt.title('Filtered Obukhov Length ')

ticks = [0, 17075, 34150, 51225, 68300, 85375, 102450, 119525, 136600, 153675, 170750, 187825, 204900, 221975, 239050, 256125, 273200, 290275, 307350, 324425, 341500, 358575, 375650, 392725, 409800, 426875, 443950, 461025, 478100, 495175, 512250, 529325, 546400, 563475, 580550, 597625, 614700, 631775, 648850, 665925, 683000, 700075, 717150, 734225, 751300, 768375, 785450, 802525]
tick_labels = list(range(1, 49))
plt.xticks(ticks, tick_labels, rotation=45)

plt.legend()
plt.savefig('Obukhov_Length_48_units_with_fit_line.png')
plt.show()

