# %% [markdown]
# ## 데이터 준비

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
df_rs = pd.read_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/df_rs_new.csv')
df_rf = pd.read_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/df_rf_new.csv')
x = pd.read_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/05_23_경제심리지수_금리.csv')

# %% [markdown]
# ### 데이터 확인

# %%
df_o

# %%
df_c

# %%
df_rs

# %%
df_rf

# %%
x

# %% [markdown]
# ## 데이터 전처리

# %%
x['휴업시작일자']=x['인허가일자']
x['휴업종료일자']=x['인허가일자']
x

# %%
pd.set_option('display.max_row', 1000)

# %%
xo = x[['인허가일자', '경제심리지수', '대출금리', '후행종합지수']]
xo

# %%
xc = x[['폐업일자', '경제심리지수', '대출금리', '후행종합지수']]
xc

# %%
xrs = x[['휴업시작일자', '경제심리지수', '대출금리', '후행종합지수']]
xrs

# %%
xrf = x[['휴업종료일자', '경제심리지수', '대출금리', '후행종합지수']]
xrf

# %%
# 시작 날짜와 끝나는 날짜 지정
start_date = "2018-01-01"
end_date = "2023-07-31"

df_c['폐업일자'] = df_c['폐업일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
df_o['인허가일자'] = df_o['인허가일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
df_rs['휴업시작일자'] = df_rs['휴업시작일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
df_rf['휴업종료일자'] = df_rf['휴업종료일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
xc['폐업일자'] = xc['폐업일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
xo['인허가일자'] = xo['인허가일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
xrs['휴업시작일자'] = xrs['휴업시작일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))
xrf['휴업종료일자'] = xrf['휴업종료일자'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', errors='coerce'))

# 시계열 생성
df_o = df_o[(df_o["인허가일자"] >= start_date) & (df_o["인허가일자"] <= end_date)].set_index("인허가일자")
df_c = df_c[(df_c["폐업일자"] >= start_date) & (df_c["폐업일자"] <= end_date)].set_index("폐업일자")
df_rs = df_rs[(df_rs["휴업시작일자"] >= start_date) & (df_rs["휴업시작일자"] <= end_date)].set_index("휴업시작일자")
df_rf = df_rf[(df_rf["휴업종료일자"] >= start_date) & (df_rf["휴업종료일자"] <= end_date)].set_index("휴업종료일자")
xo = xo[(xo["인허가일자"] >= start_date) & (xo["인허가일자"] <= end_date)].set_index("인허가일자")
xc = xc[(xc["폐업일자"] >= start_date) & (xc["폐업일자"] <= end_date)].set_index("폐업일자")
xrs = xrs[(xrs["휴업시작일자"] >= start_date) & (xrs["휴업시작일자"] <= end_date)].set_index("휴업시작일자")
xrf = xrf[(xrf["휴업종료일자"] >= start_date) & (xrf["휴업종료일자"] <= end_date)].set_index("휴업종료일자")

# %%
print(df_o.info())
print(df_c.info())
print(df_rs.info())
print(df_rf.info())
print(xo.info())
print(xc.info())
print(xrs.info())
print(xrf.info())

# %%
df_c.head()

# %%
df_o.head()

# %%
df_rs.head()

# %%
df_rf.head()

# %%
xc.head()

# %%
xo.head()

# %%
xrs.head()

# %%
xrf.head()

# %%
df_o=df_o.astype(int)
df_c=df_c.astype(int)
df_rs=df_rs.astype(int)
df_rf=df_rf.astype(int)

# %%
df_c = df_c.resample('M').agg(np.sum)
df_o = df_o.resample('M').agg(np.sum)
df_rs = df_rs.resample('M').agg(np.sum)
df_rf = df_rf.resample('M').agg(np.sum)

# %%
df_c.head()

# %%
df_o.head()

# %%
df_rs.head()

# %%
df_rf.head()

# %%
dataframes = [df_o, df_c, df_rs, df_rf]

for df in dataframes:
    print(df.isnull().sum())

# %% [markdown]
# ## 결과

# %% [markdown]
# ### 실내 마스크 해제

# %%
# 실내마스크 해제 23년 3월 20일
pre_period = ['2020-01-31', '2023-03-31']
post_period = ['2023-04-30', '2023-07-31']

# %% [markdown]
# #### 개업

# %% [markdown]
# ##### Report

# %%
# for index, row in df_o.iteritems():
#     try:
#         if row.sum() > 2:
#             op = pd.DataFrame(row).join(xo, how='left')
#         ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_o.summary('report'))
#         ci_o.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
im_op = []

for index, row in df_o.iteritems():
    try:
        if row.sum() > 2:
            op = pd.DataFrame(row).join(xo, how='left')
        ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_o.summary_data.to_dict()
        im_op.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_o.p_value,2))])
    except ValueError as e:
        print(e)

im_op = pd.DataFrame(im_op, columns=['업종;절대효과;상대효과;p-value'])
im_op.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/im_op.csv', index=False, encoding='utf-8')
im_op

# %% [markdown]
# #### 폐업

# %% [markdown]
# ##### Report

# %%
# for index, row in df_c.iteritems():
#     try:
#         if row.sum() > 2:
#             cl = pd.DataFrame(row).join(xc, how='left')
#         ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_c.summary('report'))
#         ci_c.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
im_cl = []

for index, row in df_c.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(xc, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_c.summary_data.to_dict()
        im_cl.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_c.p_value,2))])
    except ValueError as e:
        print(e)

im_cl = pd.DataFrame(im_cl, columns=['업종;절대효과;상대효과;p-value'])
im_cl.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/im_cl.csv', index=False, encoding='utf-8')
im_cl

# %% [markdown]
# #### 휴업시작

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rs.iteritems():
#     try:
#         if row.sum() > 2:
#             rs = pd.DataFrame(row).join(xrs, how='left')
#         ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rs.summary('report'))
#         ci_rs.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
im_rs = []

for index, row in df_rs.iteritems():
    try:
        if row.sum() > 2:
            rs = pd.DataFrame(row).join(xrs, how='left')
        ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rs.summary_data.to_dict()
        im_rs.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rs.p_value,2))])
    except ValueError as e:
        print(e)

im_rs = pd.DataFrame(im_rs, columns=['업종;절대효과;상대효과;p-value'])
im_rs.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/im_rs.csv', index=False, encoding='utf-8')
im_rs

# %% [markdown]
# #### 휴업종료

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rf.iteritems():
#     try:
#         if row.sum() > 3:
#             rf = pd.DataFrame(row).join(xrf, how='left')
#         ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rf.summary('report'))
#         ci_rf.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
im_rf = []

for index, row in df_rf.iteritems():
    try:
        if row.sum() > 2:
            rf = pd.DataFrame(row).join(xrf, how='left')
        ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rf.summary_data.to_dict()
        im_rf.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rf.p_value,2))])
    except ValueError as e:
        print(e)

im_rf = pd.DataFrame(im_rf, columns=['업종;절대효과;상대효과;p-value'])
im_rf.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/im_rf.csv', index=False, encoding='utf-8')
im_rf

# %% [markdown]
# ### 실외 마스크 해제

# %%
# 실외 마스크 해제 22년 9월 26일
pre_period = ['2020-01-31', '2022-09-30']
post_period = ['2022-10-31', '2023-01-31']

# %% [markdown]
# #### 개업

# %% [markdown]
# ##### report

# %%
# for index, row in df_o.iteritems():
#     try:
#         if row.sum() > 2:
#             op = pd.DataFrame(row).join(xo, how='left')
#         ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_o.summary('report'))
#         ci_o.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
om_op = []

for index, row in df_o.iteritems():
    try:
        if row.sum() > 2:
            op = pd.DataFrame(row).join(xo, how='left')
        ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_o.summary_data.to_dict()
        om_op.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_o.p_value,2))])
    except ValueError as e:
        print(e)

om_op = pd.DataFrame(om_op, columns=['업종;절대효과;상대효과;p-value'])
om_op.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/om_op.csv', index=False, encoding='utf-8')
om_op

# %% [markdown]
# #### 폐업

# %% [markdown]
# ##### Report

# %%
# for index, row in df_c.iteritems():
#     try:
#         if row.sum() > 2:
#             cl = pd.DataFrame(row).join(xc, how='left')
#         ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_c.summary('report'))
#         ci_c.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
om_cl = []

for index, row in df_c.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(xc, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_c.summary_data.to_dict()
        om_cl.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_c.p_value,2))])
    except ValueError as e:
        print(e)

om_cl = pd.DataFrame(om_cl, columns=['업종;절대효과;상대효과;p-value'])
om_cl.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/om_cl.csv', index=False, encoding='utf-8')
om_cl

# %% [markdown]
# #### 휴업시작

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rs.iteritems():
#     try:
#         if row.sum() > 2:
#             rs = pd.DataFrame(row).join(xrs, how='left')
#         ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rs.summary('report'))
#         ci_rs.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
om_rs = []

for index, row in df_rs.iteritems():
    try:
        if row.sum() > 2:
            rs = pd.DataFrame(row).join(xrs, how='left')
        ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rs.summary_data.to_dict()
        om_rs.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rs.p_value,2))])
    except ValueError as e:
        print(e)

om_rs = pd.DataFrame(om_rs, columns=['업종;절대효과;상대효과;p-value'])
om_rs.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/om_rs.csv', index=False, encoding='utf-8')
om_rs

# %% [markdown]
# #### 휴업종료

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rf.iteritems():
#     try:
#         if row.sum() > 3:
#             rf = pd.DataFrame(row).join(xrf, how='left')
#         ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rf.summary('report'))
#         ci_rf.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
om_rf = []

for index, row in df_rf.iteritems():
    try:
        if row.sum() > 2:
            rf = pd.DataFrame(row).join(xrf, how='left')
        ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rf.summary_data.to_dict()
        om_rf.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rf.p_value,2))])
    except ValueError as e:
        print(e)

om_rf = pd.DataFrame(om_rf, columns=['업종;절대효과;상대효과;p-value'])
om_rf.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/om_rf.csv', index=False, encoding='utf-8')
om_rf

# %% [markdown]
# ### 거리두기해제

# %%
# 거리두기 완전 해제 22년 4월 18일
pre_period = ['2020-01-31', '2022-04-30']
post_period = ['2022-05-31', '2022-08-31']

# %% [markdown]
# #### 개업

# %% [markdown]
# ##### report

# %%
# for index, row in df_o.iteritems():
#     try:
#         if row.sum() > 2:
#             op = pd.DataFrame(row).join(xo, how='left')
#         ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_o.summary('report'))
#         ci_o.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
dl_op = []

for index, row in df_o.iteritems():
    try:
        if row.sum() > 2:
            op = pd.DataFrame(row).join(xo, how='left')
        ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_o.summary_data.to_dict()
        dl_op.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_o.p_value,2))])
    except ValueError as e:
        print(e)

dl_op = pd.DataFrame(dl_op, columns=['업종;절대효과;상대효과;p-value'])
dl_op.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/dl_op.csv', index=False, encoding='utf-8')
dl_op

# %% [markdown]
# #### 폐업

# %% [markdown]
# ##### Report

# %%
# for index, row in df_c.iteritems():
#     try:
#         if row.sum() > 2:
#             cl = pd.DataFrame(row).join(xc, how='left')
#         ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_c.summary('report'))
#         ci_c.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
dl_cl = []

for index, row in df_c.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(xc, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_c.summary_data.to_dict()
        dl_cl.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_c.p_value,2))])
    except ValueError as e:
        print(e)

dl_cl = pd.DataFrame(dl_cl, columns=['업종;절대효과;상대효과;p-value'])
dl_cl.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/dl_cl.csv', index=False, encoding='utf-8')
dl_cl

# %% [markdown]
# #### 휴업시작

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rs.iteritems():
#     try:
#         if row.sum() > 2:
#             rs = pd.DataFrame(row).join(xrs, how='left')
#         ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rs.summary('report'))
#         ci_rs.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
dl_rs = []

for index, row in df_rs.iteritems():
    try:
        if row.sum() > 2:
            rs = pd.DataFrame(row).join(xrs, how='left')
        ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rs.summary_data.to_dict()
        dl_rs.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rs.p_value,2))])
    except ValueError as e:
        print(e)

dl_rs = pd.DataFrame(dl_rs, columns=['업종;절대효과;상대효과;p-value'])
dl_rs.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/dl_rs.csv', index=False, encoding='utf-8')
dl_rs

# %% [markdown]
# #### 휴업종료

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rf.iteritems():
#     try:
#         if row.sum() > 3:
#             rf = pd.DataFrame(row).join(xrf, how='left')
#         ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rf.summary('report'))
#         ci_rf.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
dl_rf = []

for index, row in df_rf.iteritems():
    try:
        if row.sum() > 2:
            rf = pd.DataFrame(row).join(xrf, how='left')
        ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rf.summary_data.to_dict()
        dl_rf.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rf.p_value,2))])
    except ValueError as e:
        print(e)

dl_rf = pd.DataFrame(dl_rf, columns=['업종;절대효과;상대효과;p-value'])
dl_rf.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/dl_rf.csv', index=False, encoding='utf-8')
dl_rf

# %% [markdown]
# ### 일상

# %%
# 일상 18 ~ 20년
pre_period = ['2018-01-31', '2020-08-31']
post_period = ['2020-09-30', '2020-12-31']

# %% [markdown]
# #### 개업

# %% [markdown]
# ##### report

# %%
# for index, row in df_o.iteritems():
#     try:
#         if row.sum() > 2:
#             op = pd.DataFrame(row).join(xo, how='left')
#         ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_o.summary('report'))
#         ci_o.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
pc_op = []

for index, row in df_o.iteritems():
    try:
        if row.sum() > 2:
            op = pd.DataFrame(row).join(xo, how='left')
        ci_o = CausalImpact(op, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_o.summary_data.to_dict()
        pc_op.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_o.p_value,2))])
    except ValueError as e:
        print(e)

pc_op = pd.DataFrame(pc_op, columns=['업종;절대효과;상대효과;p-value'])
pc_op.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/pc_op.csv', index=False, encoding='utf-8')
pc_op

# %% [markdown]
# #### 폐업

# %% [markdown]
# ##### Report

# %%
# for index, row in df_c.iteritems():
#     try:
#         if row.sum() > 2:
#             cl = pd.DataFrame(row).join(xc, how='left')
#         ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_c.summary('report'))
#         ci_c.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
pc_cl = []

for index, row in df_c.iteritems():
    try:
        if row.sum() > 2:
            cl = pd.DataFrame(row).join(xc, how='left')
        ci_c = CausalImpact(cl, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_c.summary_data.to_dict()
        pc_cl.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_c.p_value,2))])
    except ValueError as e:
        print(e)

pc_cl = pd.DataFrame(pc_cl, columns=['업종;절대효과;상대효과;p-value'])
pc_cl.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/pc_cl.csv', index=False, encoding='utf-8')
pc_cl

# %% [markdown]
# #### 휴업시작

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rs.iteritems():
#     try:
#         if row.sum() > 2:
#             rs = pd.DataFrame(row).join(xrs, how='left')
#         ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rs.summary('report'))
#         ci_rs.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
pc_rs = []

for index, row in df_rs.iteritems():
    try:
        if row.sum() > 2:
            rs = pd.DataFrame(row).join(xrs, how='left')
        ci_rs = CausalImpact(rs, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rs.summary_data.to_dict()
        pc_rs.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rs.p_value,2))])
    except ValueError as e:
        print(e)

pc_rs = pd.DataFrame(pc_rs, columns=['업종;절대효과;상대효과;p-value'])
pc_rs.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/pc_rs.csv', index=False, encoding='utf-8')
pc_rs

# %% [markdown]
# #### 휴업종료

# %% [markdown]
# ##### Report

# %%
# for index, row in df_rf.iteritems():
#     try:
#         if row.sum() > 3:
#             rf = pd.DataFrame(row).join(xrf, how='left')
#         ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
#         print(index)
#         print(ci_rf.summary('report'))
#         ci_rf.plot()
#         print('____________________________________________________________________________________________________')
#     except ValueError as e:
#         print(e)

# %% [markdown]
# ##### Summary

# %%
pc_rf = []

for index, row in df_rf.iteritems():
    try:
        if row.sum() > 2:
            rf = pd.DataFrame(row).join(xrf, how='left')
        ci_rf = CausalImpact(rf, pre_period, post_period, model_args={'fit_method': 'hmc'}, nseason=[{'period': 12}])
        summary = ci_rf.summary_data.to_dict()
        pc_rf.append([index + ";" + str(round(summary['average'].get('abs_effect'),2)) + ';' + str(round((summary['average'].get('rel_effect')*100),2)) + '%;' + str(round(ci_rf.p_value,2))])
    except ValueError as e:
        print(e)

pc_rf = pd.DataFrame(pc_rf, columns=['업종;절대효과;상대효과;p-value'])
pc_rf.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/pc_rf.csv', index=False, encoding='utf-8')
pc_rf


