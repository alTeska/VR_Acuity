import cfg
import h5py
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm


fnames = glob('datasets/raw/*.h5')

keys   = ['RAT', 'Capture Start Time', 'EXPERIMENTER', 'Take Name']
dfkeys = ['rat_id', 'date', 'experimenter', 'original_name']

df = pd.DataFrame()

for i, fname in tqdm(enumerate(fnames)):
    data = h5py.File(fname, 'r').attrs  # load the dataset
    dd = pd.DataFrame(data={'session_id': [i]})

    for dfkey, key in zip(dfkeys, keys):
        dd[dfkey] = data[key]  # load data to dataframe

    dd['video_name'] = dd['original_name']+'-Camera 11136'

    # speed table save as string
    speed = data['VR_ACUITY_CYLINDER_SPEEDS']
    dd['VRspeed'] = np.nan
    dd['VRspeed'] = dd['VRspeed'].apply(lambda x: speed).astype('str')

    df = df.append(dd)


with h5py.File(cfg.relational_fname, 'w') as f:
    f.create_dataset('Sessions', data=df.astype('|S').to_records())
