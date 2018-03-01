# read dataset - testing saved files
import pandas as pd

df = pd.read_hdf('VR_Acuity_Data/datasets/data_all.h5', 'Position')
print(df)

# for index, row in df.iterrows():
#    print(row['Frame'], row['X'])
