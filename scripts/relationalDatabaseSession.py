# Script for creation of new dataset - analogical to VR_Acuity_Relational_Database_ER_Diagram.pdf
import cfg
import h5py
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm


fnames = glob('datasets/raw/*.h5')

keys = ['RAT', 'Capture Start Time', 'EXPERIMENTER', 'Take Name']
dfkeys = ['rat_id', 'date', 'experimenter', 'original_name']


data_loads, dfS = {}, {}
df_sessions = pd.DataFrame()

for i, fname in tqdm(enumerate(fnames)):
    data_loads[i] = h5py.File(fname, 'r').attrs  # load the dataset

    dfS[i] = pd.DataFrame(data={'session_id': [i]})  # create needed dataframes and indices

    # copy data to dataframes
    for j, key in enumerate(keys):
        dfS[i][dfkeys[j]] = data_loads[i][key]

    speed = data_loads[i]['VR_ACUITY_CYLINDER_SPEEDS']
    dfS[i]['VRspeed'] = np.nan
    dfS[i]['VRspeed'] = dfS[i]['VRspeed'].apply(lambda x: speed).astype('str')

    df_sessions = pd.concat([df_sessions, dfS[i]], axis=0, ignore_index=True)  # merge into one dataframe
    df_sessions['video_name'] = df_sessions['original_name']+'-Camera 11136'


df_sessions = df_sessions.astype('|S')

with h5py.File(cfg.relational_fname, 'w') as f:
    f.create_dataset('Sessions', data=df_sessions.to_records())
