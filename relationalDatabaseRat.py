# Script for creation of new dataset - analogical to VR_Acuity_Relational_Database_ER_Diagram.pdf
import numpy as np
import h5py
import pandas as pd

fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC', ]

# RAT BEHAVIOR:
path = 'datasets/'
key = '/preprocessed/Rigid Body/Rat/'
index = ['X', 'Y', 'Z']


dfPos = {}
dfOri = {}

dfP = pd.DataFrame()
dfO = pd.DataFrame()

# Loading
for i, x in enumerate(fname):
    dfOri[i] = pd.read_hdf(path+x+'.h5', key+'Orientation')
    dfPos[i] = pd.read_hdf(path+x+'.h5', key+'Position')

    # removing NaN/inf
    dfOri[i] = dfOri[i].replace([np.inf, -np.inf], np.nan).dropna()
    dfPos[i] = dfPos[i].replace([np.inf, -np.inf], np.nan).dropna()

    # removal of smaller then err and out of range values
    for k in index:
        dfOri[i] = dfOri[i][np.absolute(dfOri[i][k]) > 1e-5]
        dfOri[i] = dfOri[i][np.absolute(dfOri[i][k]) < 1]

        dfPos[i] = dfPos[i][np.absolute(dfPos[i][k]) > 1e-5]
        dfPos[i] = dfPos[i][np.absolute(dfPos[i][k]) < 1]

# Add session in, merge into two dataframes: orientation and position df
for i, x in enumerate(fname):
    dfPos[i]['session_id'] = i
    dfOri[i]['session_id'] = i
    dfP = pd.concat([dfP, dfPos[i]], axis=0, ignore_index=True)
    dfO = pd.concat([dfO, dfOri[i]], axis=0, ignore_index=True)


# merge into one dataset
dfRatBehavior = pd.merge(dfP, dfO, on=('Frame', 'Time', 'session_id'),
                        suffixes=('_Pos', '_Ori'))
