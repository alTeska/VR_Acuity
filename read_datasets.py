# read dataset - testing saved files
import pandas as pd

keyPass = 'Orientation'
df = pd.read_hdf('datasets/data_all.h5', keyPass)
#print(df)

keyPass = 'Position'
df = pd.read_hdf('datasets/data_all.h5', keyPass)
print(df)

for index, row in df.iterrows():
    print(row['Frame'], row['Time'], row['X'], row['Y'], row['Z'])
