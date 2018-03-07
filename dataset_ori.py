# Single-datdataset creation
import numpy as np
import pandas as pd

dfTbl = {}
path = 'datasets/'
key = '/preprocessed/Rigid Body/Rat/'
keyPass = 'Orientation'
index = {'X', 'Y', 'Z'}
h5 = '.h5'

fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC', ]

# read data and clean from NaN/inf/wrong values
for i, x in enumerate(fname):
    dfTbl[i] = pd.read_hdf(path+x+h5, key+keyPass).replace([np.inf, -np.inf], np.nan).dropna()

    # removal of smaller then err and out of range values
    for k in index:
        dfTbl[i] = dfTbl[i][np.absolute(dfTbl[i][k]) > 1e-5]
        dfTbl[i] = dfTbl[i][np.absolute(dfTbl[i][k]) < 1]

# concat data from different experiments
DF = pd.DataFrame()
for i, x in enumerate(fname):
    DF = pd.concat([DF, dfTbl[i]], ignore_index=True)

# save data to file
DF.to_hdf(path+'data_all.h5', keyPass, table=True)

for i, x in enumerate(fname):
    dfTbl[i].to_hdf(path+x+'_clean'+h5, keyPass, table=True)
