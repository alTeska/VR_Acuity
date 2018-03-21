# Script for creation of new dataset - analogical to VR_Acuity_Relational_Database_ER_Diagram.pdf
import numpy as np
import pandas as pd
import h5py

fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC', ]

keys = [
    'RAT',
    'Capture Start Time',
    'EXPERIMENTER',
    'Take Name',
]

dfkeys = [
    'rat id',
    'date',
    'experimenter',
    'original name',
]

# SESSION:
path = 'datasets/'
fileName = {}
dfS = {}
dfSessions = pd.DataFrame()

for i, x in enumerate(fname):
    # load the dataset
    fileName[i] = h5py.File(path+x+'.h5', 'r').attrs

    # create needed dataframes and indices
    d = {'session id': [i]}
    dfS[i] = pd.DataFrame(data=d)
    dfS[i] = dfS[i].reindex(columns=['session id']+dfkeys+['video name'])

# copy data to dataframes
for i, x in enumerate(fname):
    for j, key in enumerate(keys):
        dfS[i][dfkeys[j]] = fileName[i][key]

    speed = fileName[i]['VR_ACUITY_CYLINDER_SPEEDS']
    dfS[i]['VRspeed'] = np.nan
    dfS[i]['VRspeed'] = dfS[i]['VRspeed'].apply(lambda x: speed).astype('str')

    # merge into one dataframe
    dfSessions = pd.concat([dfSessions, dfS[i]], axis=0, ignore_index=True)
    dfSessions['video name'] = dfSessions['original name']+'-Camera 11136'

dfSessions = dfSessions.astype('|S')
