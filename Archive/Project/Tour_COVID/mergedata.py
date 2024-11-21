# %%
import os
import pandas as pd

input_folder = 'C:/Users/Edward/Desktop/LOCALDATA_ALL_CSV/'
output_file = 'C:/Users/Edward/Desktop/PythonWorkspace/인허가/merged_and_filtered.csv'
columns_to_extract = [1, 5, 7, 8, 11, 26, 27]  # 0부터 시작하는 인덱스

merged_data = pd.DataFrame()

csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for csv_file in csv_files:
    csv_path = os.path.join(input_folder, csv_file)
    data = pd.read_csv(csv_path, usecols=columns_to_extract, encoding='cp949')
    merged_data = pd.concat([merged_data, data], ignore_index=True)

# 2번 열에서 중복 값이 1개만 있는 행만 선택
merged_data = merged_data[~(merged_data.duplicated(subset=merged_data.columns[1], keep=False) & 
                           ~merged_data.duplicated(subset=merged_data.columns[1], keep='first'))]

merged_data.to_csv(output_file, encoding='utf-8', index=False)

print(f"모든 CSV 파일이 통합되어 '{output_file}'에 저장되었습니다.")


# %%
merged_file_path = 'C:/Users/Edward/Desktop/PythonWorkspace/인허가/merged_and_filtered.csv'  # 통합된 CSV 파일의 경로

# CSV 파일을 읽어 DataFrame으로 로드
merged_df = pd.read_csv(merged_file_path)

# DataFrame의 처음 몇 개 행 출력
merged_df.info()

# %%
merged_data['개방서비스명'].unique()

# %%
merged_data['개방서비스명'].nunique()

# %%
del_df = merged_df[~merged_df.duplicated('개방서비스명', keep=False)]
del_df

# %%
merged_df = merged_df[merged_df.duplicated('개방서비스명') | merged_df.duplicated('개방서비스명', keep=False)]
merged_df

# %%
merged_df['개방서비스명'].unique()

# %%
threshold = 5  # 중복 개수의 임계값
counts = merged_df['개방서비스명'].value_counts()
values_to_keep = counts[counts <= threshold].index
df_filtered = merged_df[merged_df['개방서비스명'].isin(values_to_keep)]
df_filtered

# %%
merged_df = merged_df.groupby('개방서비스명').filter(lambda x: len(x) > threshold)
merged_df

# %%
print(merged_df['개방서비스명'].nunique())
print(merged_df['개방서비스명'].unique())

# %%
value_to_remove = 'N'
merged_df = merged_df[merged_df['개방서비스명'] != value_to_remove]
print(merged_df['개방서비스명'].nunique())
print(merged_df['개방서비스명'].unique())

# %%
merged_df

# %%
merged_df['인허가일자'] = pd.to_datetime(merged_df['인허가일자'], errors='coerce')
merged_df['폐업일자'] = pd.to_datetime(merged_df['폐업일자'], errors='coerce')
merged_df.info()

# %%
merged_df['기준'] = 1

# %%
df_o = merged_df[merged_df['영업상태구분코드'] == 1]
df_c = merged_df[merged_df['영업상태구분코드'] == 3]
a = [1,3]
df_w = merged_df[~merged_df['영업상태구분코드'].isin(a)]

# %%
df_w

# %%
df_o

# %%
df_c

# %%
T = df_w.shape[0] + df_o.shape[0] + df_c.shape[0]
T == merged_df.shape[0]

# %%
print(df_c.info())

# %%
df_o = df_o.groupby(['인허가일자', '개방서비스명'])['기준'].sum().unstack()
df_c = df_c.groupby(['폐업일자', '개방서비스명'])['기준'].sum().unstack()

# %%
df_o

# %%
df_c

# %%
df_o.info()

# %%
df_c.info()

# %%
df_o = df_o.fillna(0)
df_c = df_c.fillna(0)
df_o = df_o.astype(int)
df_c = df_c.astype(int)

# %%
df_o

# %%
df_c

# %%
df_o.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/df_o_new.csv')
df_c.to_csv('C:/Users/Edward/Desktop/PythonWorkspace/인허가/df_c_new.csv')


