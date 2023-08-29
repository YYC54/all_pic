import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler

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
df1 = df1[df1['Rain'] != 0]


#对CO2flux和Rain进行标准化
scaler = StandardScaler()
df1[['CO2flux', 'Rain']] = scaler.fit_transform(df1[['CO2flux', 'Rain']])

# 绘制散点图
plt.figure(figsize=(10, 6))
plt.scatter(df1['CO2flux'], df1['Rain'], s=10, c='blue', alpha=0.5)
plt.xlabel('CO2flux (mg/m^2/s)')
plt.ylabel('Rain')
plt.title('CO2flux vs Rain')
plt.savefig('scatter(雨季)')
plt.show()
