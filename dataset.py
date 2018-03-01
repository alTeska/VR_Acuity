# Single-datdataset creation
# import numpy as np
import pandas as pd
import math

def check_nan(DataFrame, key):
    for i, x in enumerate(DataFrame[key]):
        if math.isnan(x):
            print(i, x)
            # DataFrame.drop(DataFrame.index[i], inplace=True)
            # i -= 1

df_tbl = {}

path = 'VR_Acuity_Data/datasets/'
fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC.h5',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC.h5',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU.h5',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC.h5',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC.h5',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC.h5',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC.h5',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC.h5', ]

fnameClean = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC_clean.h5',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC_clean.h5',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU_clean.h5',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC_clean.h5',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC_clean.h5',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC_clean.h5',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC_clean.h5',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC_clean.h5', ]

# read data from files and clean from NaN values
key = '/preprocessed/Rigid Body/Rat/'
keyPass = 'Orientation'
for i, x in enumerate(fname):
    df_tbl[i] = pd.read_hdf(path+fname[i], key+keyPass).dropna()
    check_nan(df_tbl[i], 'X')
    check_nan(df_tbl[i], 'Y')
    check_nan(df_tbl[i], 'Z')

# concat data from different experiments
DF = pd.DataFrame()
for i, x in enumerate(fname):
    DF = pd.concat([DF, df_tbl[i]], ignore_index=True)

# save data to file
DF.to_hdf('VR_Acuity_Data/datasets/data_all.h5', keyPass, table=True)
for i, x in enumerate(fname):
    df_tbl[i].to_hdf('VR_Acuity_Data/datasets/'+fnameClean[i], keyPass, table=True)
