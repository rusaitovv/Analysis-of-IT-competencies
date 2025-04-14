import pandas as pd
import chardet

with open('C:/Users/gorba/Downloads/Аналитик данных.csv', 'rb') as f:
    result = chardet.detect(f.read(10000))  # Анализ первых 10КБ

df = pd.read_csv('C:/Users/gorba/Downloads/Аналитик данных.csv', sep='\s*;\s*',
                 names=['Компетенция', 'Уровень владения'], encoding = 'IBM866',
                 skiprows=2, engine='python')

df = df.apply(lambda x: x.str.replace('"', '') if x.dtype == 'object' else x)

df['Уровень владения'] = pd.to_numeric(df['Уровень владения'], errors='coerce').fillna(0).astype(int)
print(df.head(), result)
print(df.dtypes)