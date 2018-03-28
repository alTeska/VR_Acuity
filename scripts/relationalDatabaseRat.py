# Script for creation of new dataset - analogical to VR_Acuity_Relational_Database_ER_Diagram.pdf
import h5py
import numpy as np
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
colChoice = ['X_Pos', 'Y_Pos', 'Z_Pos', 'X_Ori', 'Y_Ori', 'Z_Ori']

dfPos = {}
dfOri = {}

dfP = pd.DataFrame()
dfO = pd.DataFrame()

# Loading and merging
for i, x in enumerate(fname):
    dfOri[i] = pd.read_hdf(path+x+'.h5', key+'Orientation')
    dfPos[i] = pd.read_hdf(path+x+'.h5', key+'Position')

    dfOri[i]['session_id'] = i
    dfPos[i]['session_id'] = i

    # removal of rat carrying position changes p
    dfP = pd.concat([dfP, dfPos[i]], axis=0, ignore_index=True)
    dfO = pd.concat([dfO, dfOri[i]], axis=0, ignore_index=True)


# merge into one dataset
dfRat = pd.merge(dfP, dfO, on=('Frame', 'Time', 'session_id'),
                        suffixes=('_Pos', '_Ori'))

#FILTERING BAD VALUES
dfRat.replace([np.inf, -np.inf], np.nan).dropna(inplace=True)

# removal of smaller then err and out of range values
for col in colChoice:
    dfRat = dfRat[np.absolute(dfRat[col]) < 1]
    dfRat = dfRat[np.absolute(dfRat[col]) > 1e-5]

# removal of rat carrying position changes p
dfRat = dfRat[np.absolute(dfRat['X_Pos']) < 1.5e-1]
dfRat = dfRat[np.absolute(dfRat['Y_Pos']) < 3e-1]
dfRat = dfRat[np.absolute(dfRat['Z_Pos']) < 1e-1]
