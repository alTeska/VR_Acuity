# Script for creation of new dataset - analogical to VR_Acuity_Relational_Database_ER_Diagram.pdf
import numpy as np
import pandas as pd
import h5py

fname = glob('../datasets/raw/*.h5')

keys = [
    'RAT',
    'Capture Start Time',
    'EXPERIMENTER',
    'Take Name',
]

dfkeys = [
    'rat_id',
    'date',
    'experimenter',
    'original_name',
]

# SESSION:
fileName = {}
dfS = {}
dfSessions = pd.DataFrame()

for i, x in enumerate(fname):
    # load the dataset
    fileName[i] = h5py.File(x, 'r').attrs

    # create needed dataframes and indices
    d = {'session_id': [i]}
    dfS[i] = pd.DataFrame(data=d)
    dfS[i] = dfS[i].reindex(columns=['session_id']+dfkeys+['video_name'])

# copy data to dataframes
for i, x in enumerate(fname):
    for j, key in enumerate(keys):
        dfS[i][dfkeys[j]] = fileName[i][key]

    speed = fileName[i]['VR_ACUITY_CYLINDER_SPEEDS']
    dfS[i]['VRspeed'] = np.nan
    dfS[i]['VRspeed'] = dfS[i]['VRspeed'].apply(lambda x: speed).astype('str')

    # merge into one dataframe
    dfSessions = pd.concat([dfSessions, dfS[i]], axis=0, ignore_index=True)
    dfSessions['video_name'] = dfSessions['original_name']+'-Camera 11136'

dfSessions = dfSessions.astype('|S')
