import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
# 将数据转换为 DataFrame
df = pd.read_csv('/Users/yanyuchen/咸鱼结课作业/1/slow_data1(1).csv', delimiter=',', header=0, na_values='NAN')
df.drop(0, inplace=True)

df['CO2flux'] = df['CO2flux'].astype(float)
df['Rain'] = df['Rain'].astype(float)

# 将CO2flux小于-10的数据赋值为NaN
threshold = -10
df.loc[df['CO2flux'] < threshold, 'CO2flux'] = np.nan
threshold1 = 10
df.loc[df['CO2flux'] > threshold1, 'CO2flux'] = np.nan

# threshold1 = 4
# df.loc[df['Rain'] > threshold1, 'Rain'] = np.nan


# 删除含有NaN的行
df1 = df.dropna(subset=['CO2flux', 'Rain'])
# df1 = df1[df1['Rain'] != 0]


#对CO2flux和Rain进行标准化
# scaler = StandardScaler()
# df1[['CO2flux', 'Rain']] = scaler.fit_transform(df1[['CO2flux', 'Rain']])



# 设置底图大小
figsize = (6, 6)

# 创建 JointGrid 对象
grid = sns.JointGrid(x='Rain', y='CO2flux', data=df1, height=figsize[0], ratio=1)

# 使用 plot_joint() 绘制散点图
grid.plot_joint(plt.scatter, alpha=0.4)

# 使用 plot_marginals() 绘制边缘直方图
grid.plot_marginals(sns.histplot, kde=False, color="blue")
plt.savefig('边缘直方图')
plt.show()
