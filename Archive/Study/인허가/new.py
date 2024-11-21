# 라이브러리 가져오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# class 만들기

# LinearRegression이라는 클래스 만듦
# lect4에서 클래스를 불러와서 사용함
class LinearRegression:
def __init__(self):
    print("Linear Regression version: 0.1")

def load_dataset(self, filename):
    '''
    경로에 저장되어 있는 csv 데이터를 로딩한다.
    :param filename:
    :return:
    '''
    df = pd.read_csv(filename)
    df.head()
    df.shape
    return df

def prepare_dataset(self, df):
X = df.values[:, 0] # 0은 인덱스 번호 # 만명을 기준으로
y = df.values[:, 1] # 1은 인덱스 번호 # 10,000 달러를 기준으로
m = len(y) # m은 나중에 비용함수를 계산할 때 사용되는 변수
print("X =", X[:5])
print("y =", y[:5])
print("m =", m)
return X, y, m

def create_scatter(self, X, y):
    plt.scatter(X, y, color="red", marker="+")
    plt.grid()
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.xlabel("Population of City in 10,000s'")
    plt.ylabel("Profit in $10,000s'")
    plt.title("Scatter plot of training data")
    plt.show()


# massage를 print 하는 함수
def print_message(self, msg):
    print(msg)