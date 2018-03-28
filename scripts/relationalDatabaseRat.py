import cfg
import h5py
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm


fnames = glob('datasets/raw/*.h5')
key = '/preprocessed/Rigid Body/Rat/'


# RAT BEHAVIOR:
# Loading and merging
df = pd.DataFrame()
for i, fname in tqdm(enumerate(fnames)):
    pos = pd.read_hdf(fname, key + 'Position')
    ori = pd.read_hdf(fname, key + 'Orientation')
    dd = pd.merge(pos, ori, on=('Frame', 'Time'), suffixes=('_Pos', '_Ori'))
    dd['session_id'] = i
    df = df.append(dd)

# FILTERING BAD VALUES
df.replace([np.inf, -np.inf], np.nan).dropna(inplace=True)

# col_choices = ['X_Pos', 'Y_Pos', 'Z_Pos', 'X_Ori', 'Y_Ori', 'Z_Ori']
# removal of smaller then err and out of range values - to be checked
# for col in col_choices:
    # df = df[np.absolute(df[col]) < 1]
    # df = df[np.absolute(df[col]) > 1e-5]

# removal of rat carrying position changes p
df = df[np.absolute(df['X_Pos']) < 1.5e-1]
df = df[np.absolute(df['Y_Pos']) < 3e-1]
df = df[np.absolute(df['Z_Pos']) < 1e-1]


with h5py.File(cfg.relational_fname, 'a') as f:
    f.create_dataset('Rat_Behavior', data=df.to_records())
