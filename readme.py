import pandas as pd

df=pd.read_csv('score.csv',delimiter=' ')
# print(df['专业代码'])
print(df[df['专业代码']=='085212'])
df[df['专业代码']=='085212'].to_csv('085212.csv',index=False,encoding='gbk')
how to use git