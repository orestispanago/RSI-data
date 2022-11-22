import pandas as pd
import os
import matplotlib.pyplot as plt


def mkdir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


with open('CR800_MinAvg.dat', 'r') as file :
  filedata = file.read()

filedata = filedata.replace('NAN', '')

with open('data.dat', 'w') as file:
  file.write(filedata)

df = pd.read_csv('data.dat',skiprows=[0,2,3], parse_dates=True,
                 index_col='TIMESTAMP')
df.index.names=['Datetime']

days_list = [group[1] for group in df.groupby(df.index.date)]
for day in days_list:
    date_str = day.index[0].date().strftime('%Y%m%d')
    folder = f"converted_historical/{day.index[0].year}"
    mkdir_if_not_exists(folder)
    day.to_csv(f"{folder}/{date_str}.csv")

df = df.resample('1min').mean()
for col in list(df):
    plt.figure(figsize=(18,4))
    df[col].plot(style=',')
    plt.title(col)
    plt.show()