
from lecture4.LinearRegression_2 import LinearRegression

lr = LinearRegression()
lr.print_message("안녕하세요!")

# Linear Regression 안에 있는 load 함수 사용
filename ="C:/Users/Edward/Downloads/profit_population.csv"
df = lr.load_dataset(filename)

# Linear Regression 안에 있는 Prepare_dataset 함수 사용
X, y, m = lr.prepare_dataset(df)

# create_scatter 함수 사용
lr.create_scatter(X,y)