# 라이브러리 불러오기
import imp
from xml.etree.ElementInclude import include
from click import style
import numpy as np
import pandas as pd

# 사이킷런 불러오기
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn. preprocessing import MinMaxScaler
from sklearn import metrics

# 시각화 라이브러리 불러오기
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#판다스 전체보기 옵션 설정
pd.options.display.width = None
pd.options.display.max_columns = None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

from warnings import filterwarnings
filterwarnings(action = 'ignore')

#데이터 불러오기
filename = "C:/Users/Edward/Downloads/winequality-red.csv"
wine = pd.read_csv(filename)
print("Successfully Imported Data!")
print(wine.head())
print(wine.shape)

#EDA
wine.describe(include='all')

# 결측치 보기
print(wine.isna().sum())
wine.groupby("quality")["quality"].count()
sns.countplot(wine['quality'])
plt.show()

#Histogram
sns.set(style="darkgrid")
sns.histplot(data=wine, x="alcohol", color="red", label="Alcohol", kde=True, bins=10)
sns.histplot(data=wine, x="fixed acidity", color="skyblue", label="Fixed acidity", kde=True, bins=10)
plt.legend()
plt.show()

# Histogram matrix - alcohol, fixed acidity, volatile acidity, chlorides
fig, axs = plt.subplots(2, 2, figsize=(7, 7))
sns.set(style="darkgrid")
sns.histplot(data=wine, x="alcohol", color="red", label="Alcohol", kde=True, bins=10, ax=axs[0, 0])
sns.histplot(data=wine, x="fixed acidity", color="skyblue", label="Fixed acidity", kde=True, bins=10, ax=axs[0, 1])
sns.histplot(data=wine, x="volatile acidity", color="olive", label="Volatile acidity", kde=True, bins=10, ax=axs[1, 0])
sns.histplot(data=wine, x="chlorides", color="teal", label="Chlorides", kde=True, bins=10, ax=axs[1, 1])
plt.legend()
plt.show()

#Box plot
sns.boxplot(y=wine["free sulfur dioxide"])
plt.show()

#Box plot - all
wine_melted = pd.melt(wine)
print(wine_melted.head())
sns.boxplot(x="variable", y="value", data=wine_melted)
plt.show()

#Box plot - Select columns
wine_melted = pd.melt(wine[['free sulfur dioxide', 'total sulfur dioxide']])
wine_melted.head()
sns.boxplot(x='variable', y='value', data=wine_melted)
plt.show()

# Scatter plot
sns.regplot(x=wine['free sulfur dioxide'], y=wine['total sulfur dioxide'], line_kws={'color':"r","alpha":0.7,"lw":10})
plt.show()

sns.lmplot(x="free sulfur dioxide", y="total sulfur dioxide", hue="quality", data = wine)
plt.show()

sns.jointplot(x="free sulfur dioxide", y="total sulfur dioxide", data = wine, kind="reg")
plt.show()

sns.pairplot(wine, x_vars=["free sulfur dioxide", "total sulfur dioxide"], y_vars=["alcohol"], hue="quality", height=5, aspect=.8, kind="reg")
sns.pairplot(wine)
plt.show()

#Correlation
corr = wine.corr()
sns.heatmap(corr, annot=True)

#데이터 준비
X= wine[list(wine.columns)[:-1]]
Y= wine["quality"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=40)
print(X_train.shape) #(1119, 11)
print(X_test.shape) #(480, 11)
print(X_train.head())

#Min-Max 정규화
norm = MinMaxScaler()
norm_fit = norm.fit(X_train)
scal_xtrain = norm_fit.transform(X_train)
scal_xtest = norm_fit.transform(X_test)
print(scal_xtrain)

