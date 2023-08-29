import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

# 删除含有NaN的行
df1 = df.dropna(subset=['CO2flux', 'Rain']).copy()

#对CO2flux和Rain进行标准化
scaler = StandardScaler()
df1[['CO2flux', 'Rain']] = scaler.fit_transform(df1[['CO2flux', 'Rain']])

df1['TIMESTAMP'] = pd.to_datetime(df1['TIMESTAMP'])

# 提取时间特征
df1['Year'] = df1['TIMESTAMP'].dt.year
df1['Month'] = df1['TIMESTAMP'].dt.month
df1['Day'] = df1['TIMESTAMP'].dt.day
df1['Hour'] = df1['TIMESTAMP'].dt.hour

# 删除原始的 TIMESTAMP 列
df1 = df1.drop(columns=['TIMESTAMP'])

# 选择特征和目标变量
X = df1[['Year', 'Month', 'Day', 'Hour', 'SWDOWN', 'SWUP', 'LWDOWN', 'LWUP', 'QG', 'QH', 'QE', 'SurfPressure', 'Ux', 'Uy', 'Uz', 'AirTemp', 'RH', 'SoilTemp', 'SoilMoisture', 'Rain']]
y = df1['CO2flux']

# 删除包含缺失值的行
X = X.dropna()
y = y.loc[X.index]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建线性回归模型
# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("均方误差: {:.2f}".format(mse))
print("R²分数: {:.2f}".format(r2))

# 获取系数和截距
coefficients = model.coef_
intercept = model.intercept_

# 打印拟合方程
equation = "CO2flux = "
for i, coef in enumerate(coefficients):
    equation += f"{coef:.2f} * {X.columns[i]} + "
equation += f"{intercept:.2f}"

print("拟合方程：")
print(equation)
