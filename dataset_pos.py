# Single-datdataset creation
import numpy as np
import pandas as pd

df_tbl = {}

path = 'VR_Acuity_Data/datasets/'
key = '/preprocessed/Rigid Body/Rat/'
keyPass = 'Position'
keys = {'X', 'Y', 'Z'}

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

# Err size check for data filtering
'''
df_err = {}

errKey = 'Error Per Marker'
for i, x in enumerate(fname):
    errValues = pd.read_hdf(path+fname[i], key+errKey)
    print(errValues.max())
    print(errValues.min())
'''

# read data and clean from NaN/inf/wrong values
for i, x in enumerate(fname):
    df_tbl[i] = pd.read_hdf(path+fname[i], key+keyPass).replace([np.inf, -np.inf], np.nan).dropna()

    # removal of smaller then err and out of range values
    for k in keys:
        df_tbl[i] = df_tbl[i][np.absolute(df_tbl[i][k]) > 1e-5]
        df_tbl[i] = df_tbl[i][np.absolute(df_tbl[i][k]) < 1]

    # removal of rat carrying position changes
    df_tbl[i] = df_tbl[i][df_tbl[i]['X'] < 1.5e-1]
    df_tbl[i] = df_tbl[i][df_tbl[i]['Y'] < 3e-1]
    df_tbl[i] = df_tbl[i][df_tbl[i]['Z'] < 1e-1]


# concat data from different experiments
DF = pd.DataFrame()
for i, x in enumerate(fname):
    DF = pd.concat([DF, df_tbl[i]], ignore_index=True)

# save data to file
DF.to_hdf(path+'data_all.h5', keyPass, table=True)

for i, x in enumerate(fname):
    df_tbl[i].to_hdf(path+fnameClean[i], keyPass, table=True)
