# import cfg
import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm

pd.options.mode.chained_assignment = None  # to be fixed

win_secs = 0.25
threshold = 300


def calculate_u(df):
    dfn = df[['Theta', 'Time']].diff()
    pos = dfn['Theta']
    pos_mask = pos > np.degrees(5.5)
    pos[pos_mask] = 360 - pos[pos_mask]

    neg_mask = pos < np.degrees(-5.5)
    pos[neg_mask] = 360 + pos[neg_mask]
    return pos / dfn['Time']


## Data Loading
dfrat2 = pd.DataFrame()
dfrat  = pd.read_hdf(cfg.filtered_fname, 'Rat_Behavior').set_index('index')

print('loaded')


## ANGLE
dfrat['Theta'] = np.degrees(np.arctan2(*(dfrat[['X_Ori', 'Z_Ori']].T
                                       / np.linalg.norm(dfrat[['X_Ori', 'Z_Ori']], axis=1)).values))

## VELOCITY
for name, dd in tqdm(dfrat.groupby('session_id')):
    dd['U'] = calculate_u(dd)
    dd['U_var'] = dd.U.rolling(window=int(win_secs * 240), center=False).std()
    dfrat2 = pd.concat([dfrat2, dd], axis=0, ignore_index=True)
#
print('velocity')

### Filter Out Bad Velocities
dfrat2 = dfrat2[np.abs(dfrat2.U) < threshold]


dfevent = pd.read_hdf(cfg.filtered_fname, 'Rat_Behavior').set_index('index')
dfsession = pd.read_hdf(cfg.relational_fname, 'Sessions').set_index('index')

with h5py.File(cfg.velocity_fname, 'w') as f:
    f.create_dataset('Rat_Behavior', data=dfrat2.to_records())
    f.create_dataset('Events'      , data=dfevent.to_records())
    f.create_dataset('Sessions'    , data=dfsession.astype('|S').to_records())
