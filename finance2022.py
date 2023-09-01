# %% [markdown]
# # 타 국가의 은행 파산이 국내 금융지주사에 미치는 영향

# %% [markdown]
# 공변량 후보: 미국, 한국(환율, 경제 성장률, GDP, 금리, 주식지수)
# 
# 환율 USD, KRW, USD/KRW  V
# 
# 주식 지수: KOSPI, KRX100, DJI 
# 
# 무역 거래량? 외교지수?

# %%
import FinanceDataReader as fdr
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import numpy as np
from datetime import datetime, timedelta
from causalimpact import CausalImpact
import warnings
warnings.filterwarnings('ignore')

# %%
# KS11 (KOSPI 지수), 2022년~현재
df = fdr.DataReader('KS11', '2022')
df = pd.DataFrame(df)
x = pd.DataFrame(df['Close'])
x

# %%
df1 = fdr.DataReader('105560', '2021') #KB
df1 = pd.DataFrame(df1)
df1

# %%
df2 = fdr.DataReader('316140', '2021') #우리
df2 = pd.DataFrame(df2)
df2

# %%
df3 = fdr.DataReader('086790', '2021') #하나
df3 = pd.DataFrame(df3)
df3

# %%
df4 = fdr.DataReader('055550', '2021') #신한
df4 = pd.DataFrame(df4)
df4

# %%
df5 = fdr.DataReader('139130', '2021') #DGB
df5 = pd.DataFrame(df5)
df5

# %%
df6 = fdr.DataReader('138930', '2021') #BNK
df6 = pd.DataFrame(df6)
df6

# %%
df7 = fdr.DataReader('175330', '2021') #JB
df7 = pd.DataFrame(df7)
df7

# %%
dfs = []  # DataFrame들을 저장할 리스트

for i in range(1, 5):
    df = eval('df{}'.format(i))  # 직접 DataFrame에 접근
    dfs.append(df['Close'])  # 'Close' 열을 리스트에 추가

# DataFrame들을 병합
merged_df = dfs[0]  # 첫 번째 DataFrame으로 시작
for i in range(1, len(dfs)):
    merged_df = pd.merge(merged_df, dfs[i], on='Date', how='inner')

# 병합된 DataFrame 출력
merged_df

# %%
# 열 이름에 숫자를 붙여 변경
new_columns = [f'Close_{i+1}' for i in range(len(merged_df.columns))]
merged_df.columns = new_columns

# 변경된 열 이름 확인
print(merged_df.columns)
merged_df = pd.DataFrame(merged_df)

# %%
merged_df.to_csv('merged_df1.csv')

# %%
x.reset_index(inplace=True)
x['Date'] = pd.to_datetime(x['Date'])
x.set_index('Date')
x

# %%
merged_df.reset_index(inplace=True)
merged_df['Date'] = pd.to_datetime(merged_df['Date'])
merged_df.set_index('Date')
merged_df

# %%
# 주중, 주말 및 공휴일 설정
weekmask = 'Mon Tue Wed Thu Fri'
weekend = ['Sat', 'Sun']  # 주말 설정
today = datetime.now()
tomorrow = today + timedelta(1)
holidays = pd.to_datetime(['2023-01-01', tomorrow])  # 공휴일 날짜 설정
today = today.strftime('%Y-%m-%d')

# CustomBusinessDay 객체 생성
custom_business_day = CustomBusinessDay(weekmask=weekmask, holidays=holidays, calendar=weekend)

# 주말과 공휴일을 포함한 모든 비즈니스 데이 날짜 생성
business_dates = pd.date_range(start=merged_df['Date'].min(), end=merged_df['Date'].max(), freq=custom_business_day)

# 주말과 공휴일을 포함한 모든 날짜로 데이터프레임 재생성
merged_df.set_index('Date', inplace=True)  # 인덱스 재설정
merged_df = merged_df.reindex(business_dates)

x.set_index('Date', inplace=True)
x = x.reindex(business_dates)

# 결측치를 이전 유효한 값으로 채우기
merged_df = merged_df.fillna(method='ffill')

x = x.fillna(method='bfill')

# 변경된 데이터프레임 출력
merged_df

# %%
x

# %%
merged_df.columns = ['KB', '우리', '하나', '신한']
merged_df

# %%
merged_df.to_csv('merged_df.csv')

# %%
# SVB 파산
pre_period = ['2021-01-04', '2023-03-09']
post_period = ['2023-03-10', today]

# %%
for index, row in merged_df.iteritems():
    try:
        if row.sum() > 2:
            ci = pd.DataFrame(row).join(x, how='left')
        cib = CausalImpact(ci, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = cib.summary_data.to_dict()
        print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(cib.p_value,2)))
    except ValueError as e:
        print(e)

# %%
for index, row in merged_df.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(x, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        print(index)
        print(ci_c.summary())
        ci_c.plot()
        print('____________________________________________________________________________________________________')
    except ValueError as e:
        print(e)

# %%
# 거리두기 해제
pre_period = ['2021-01-04', '2022-04-18']
post_period = ['2022-04-19', today]

# %%
for index, row in merged_df.iteritems():
    try:
        if row.sum() > 2:
            ci = pd.DataFrame(row).join(x, how='left')
        cib = CausalImpact(ci, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = cib.summary_data.to_dict()
        print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(cib.p_value,2)))
    except ValueError as e:
        print(e)

# %%
for index, row in merged_df.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(x, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        print(index)
        print(ci_c.summary())
        ci_c.plot()
        print('____________________________________________________________________________________________________')
    except ValueError as e:
        print(e)

# %%
# 미 연준 빅스텝
pre_period = ['2021-01-04', '2022-07-27']
post_period = ['2022-07-28', today]

# %%
for index, row in merged_df.iteritems():
    try:
        if row.sum() > 2:
            ci = pd.DataFrame(row).join(x, how='left')
        cib = CausalImpact(ci, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = cib.summary_data.to_dict()
        print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(cib.p_value,2)))
    except ValueError as e:
        print(e)

# %%
for index, row in merged_df.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(x, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        print(index)
        print(ci_c.summary())
        ci_c.plot()
        print('____________________________________________________________________________________________________')
    except ValueError as e:
        print(e)

# %%
'''for index, row in merged_df.iteritems():
    try:
        ci_o = CausalImpact(row, pre_period, post_period, model_args={'fit_method': 'hmc'})
        print(index)
        print(ci_o.summary())
        ci_o.plot()
        print('____________________________________________________________________________________________________')
    except ValueError as e:
        print(e)'''


