# %%
import pandas as pd
import numpy as np
from causalimpact import CausalImpact
import sys
import warnings
warnings.filterwarnings('ignore')

# %%
df_o=pd.read_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/df_o_new.csv')
df_c=pd.read_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/df_c_new.csv')
x = pd.read_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/경제심리지수 및 금리.csv', encoding='cp949')

# %%
df_o

# %%
df_c

# %%
x

# %%
pd.set_option('display.max_row', 1000)

# %%
df_c['폐업일자'] = df_c['폐업일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
df_o['인허가일자'] = df_o['인허가일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
x['폐업일자'] = x['폐업일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))
x['인허가일자'] = x['인허가일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d'))

# %%
xo = x[['인허가일자', '경제심리지수', '대출금리']]
xo

# %%
xc = x[['폐업일자', '경제심리지수', '대출금리']]
xc

# %%
df_c = df_c.set_index('폐업일자')
df_o = df_o.set_index('인허가일자')
xc = xc.set_index('폐업일자')
xo = xo.set_index('인허가일자')

# %%
df_c

# %%
df_o

# %%
xc

# %%
xo

# %%
df_o=df_o.astype(int)
df_c=df_c.astype(int)
xo=xo.astype(int)
xc=xc.astype(int)

# %%
df_c = df_c.resample('M').agg(np.sum)
df_o = df_o.resample('M').agg(np.sum)
pre_period = ['2020-01-31', '2022-04-30']
post_period = ['2022-05-31', '2022-12-31']

# %%
df_c

# %%
df_o

# %%
# 시작 날짜와 끝나는 날짜 지정
start_date = "2020-01-01"
end_date = "2023-06-30"

df_o = df_o.reset_index()
df_c = df_c.reset_index()
xo = xo.reset_index()
xc = xc.reset_index()

# 시계열 생성
df_o = df_o[(df_o["인허가일자"] >= start_date) & (df_o["인허가일자"] <= end_date)].set_index("인허가일자")
df_c = df_c[(df_c["폐업일자"] >= start_date) & (df_c["폐업일자"] <= end_date)].set_index("폐업일자")
xo = xo[(xo["인허가일자"] >= start_date) & (xo["인허가일자"] <= end_date)].set_index("인허가일자")
xc = xc[(xc["폐업일자"] >= start_date) & (xc["폐업일자"] <= end_date)].set_index("폐업일자")

# %%


# %% [markdown]
# ## 분석결과

# %% [markdown]
# ### 개업

# %%
op = pd.DataFrame(df_o['휴게음식점']).join(xo, how='left')
# ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
# ci_o.plot()
op

# %%
for index, row in df_o.iteritems():
    try:
        if row.sum() > 2:
            op = pd.DataFrame(row).join(xo, how='left')
        ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        print(index)
        print(ci_o.summary())
        ci_o.plot()
        print('____________________________________________________________________________________________________')
    except ValueError as e:
        print(e)

# %% [markdown]
# ### 폐업

# %%
for index, row in df_c.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(xc, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        print(index)
        print(ci_c.summary())
        ci_c.plot()
        print('____________________________________________________________________________________________________')
    except ValueError as e:
        print(e)

# %% [markdown]
# ## 분석결과 타당성

# %%
# pre_period = ['2020-01-31', '2021-10-31']
# post_period = ['2021-11-30', '2022-04-30']

# %% [markdown]
# ### 개업

# %%
# for index, row in df_o.iteritems():
#     try:
#         if row.sum() > 3:
#             op = pd.DataFrame(row).join(xo, how='left')
#         ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_o.summary())
#         ci_o.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ### 폐업

# %%
# for index, row in df_c.iteritems():
#     try:
#         if row.sum() > 2:
#             cl = pd.DataFrame(row).join(xc, how='left')
#         ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_c.summary())
#         ci_c.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ## 결과 summary화

# %% [markdown]
# ### 결과

# %%
pre_period = ['2020-01-31', '2022-04-30']
post_period = ['2022-05-31', '2022-12-31']

# %%
for index, row in df_o.iteritems():
    try:
        if row.sum() > 2:
            op = pd.DataFrame(row).join(xo, how='left')
        ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_o.summary_data.to_dict()
        print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(ci_o.p_value,2)))
    except ValueError as e:
        print(e)

# %%
for index, row in df_c.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(xc, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_c.summary_data.to_dict()
        print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(ci_c.p_value,2)))
    except ValueError as e:
        print(e)

# %% [markdown]
# ### 타당성

# %%
# pre_period = ['2020-01-31', '2021-10-31']
# post_period = ['2021-11-30', '2022-04-30']

# %%
# for index, row in df_o.iteritems():
#     try:
#         if row.sum() > 3:
#             op = pd.DataFrame(row).join(xo, how='left')
#         ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         summary = ci_o.summary_data.to_dict()
#         print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(ci_o.p_value,2)))
#     except ValueError as e:
#         print(e)

# %%
# for index, row in df_c.iteritems():
#     try:
#         if row.sum() > 2:
#             cl = pd.DataFrame(row).join(xc, how='left')
#         ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         summary = ci_c.summary_data.to_dict()
#         print(index + "," + str(round(summary['average'].get('abs_effect'),2)) + '%,' + str(round((summary['average'].get('rel_effect')*100),2)) + '%,' + str(round(ci_c.p_value,2)))
#     except ValueError as e:
#         print(e)


