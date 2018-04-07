import cfg
import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm


pd.options.mode.chained_assignment = None  # to be fixed

dfOri = pd.DataFrame()
dfOri2 = pd.DataFrame()
dfOriU = pd.DataFrame()

dfrat   = pd.read_hdf(cfg.filtered_fname, 'Rat_Behavior').set_index('index')
dfevent = pd.read_hdf(cfg.filtered_fname, 'Rat_Behavior').set_index('index')
print('loaded')


## VECTORS WITHOUT Y
for name, dd in tqdm(dfrat.groupby('session_id')):
    dd['dT'] = dd['Time'].diff(1)
    # calculating lenghts of VecX and VecZ and creation of shifted vectors   #dd = dd.apply(decompose_vec_df, axis=1)
    dd['lVo'] = np.linalg.norm(np.array([dd.X_Ori, dd.Y_Ori, dd.Z_Ori])  )
    dd['lx1'] = dd['X_Ori'] / dd['lVo']
    dd['lz1'] = dd['Z_Ori'] / dd['lVo']

    # normalize the data to unit vector form
    dd['V1'] = np.linalg.norm(np.array([dd.lx1, 0, dd.lz1]))
    dd['lx1'] = dd.lx1 / dd.V1
    dd['lz1'] = dd.lz1 / dd.V1

    dfOri = pd.concat([dfOri, dd], axis=0, ignore_index=True)

dfOri.replace([np.inf, -np.inf], np.nan).dropna(inplace=True)

print('vectors')


## ANGLES and VELOCITY

# calculatinig the angles between X axis and the vectors
for name, dd in tqdm(dfOri.groupby('session_id')):
    dd['lx2'] = dd.lx1.shift(1)
    dd['lz2'] = dd.lz1.shift(1)

    V1 = np.array([dd.lx1, 0, dd.lz1])
    V2 = np.array([dd.lx2, 0, dd.lz2])

    dd['clockwise'] = dd.lz1 * dd.lx2 < dd.lx1 * dd.lz2
    dd.clockwise = dd.clockwise.astype(int).replace(to_replace=0, value=-1)

    dd['theta']  = np.arccos(np.dot(V1, V2) / (np.linalg.norm(V1) * np.linalg.norm(V2)))


    # angular velocity between two vectors
    dd['U'] = np.degrees(dd.theta * dd.clockwise)/ dd.dT
    dd['UM'] = dd['U'].rolling(window=20).mean(center=True)

    dfOri2 = pd.concat([dfOri2, dd], axis=0, ignore_index=True)

dfOri2.replace([np.inf, -np.inf], np.nan).dropna(inplace=True)

print('velocity')


## FILTERING HIGH DATA
dfOri2 = dfOri2[np.absolute(dfOri2['dT']) < 0.005] # filtering out big time gaps frame points
# dfOri2 = dfOri2[np.absolute(dfOri2['U'])  < 2000]   # too big velocities removal


dfsession = pd.read_hdf(cfg.relational_fname, 'Sessions').set_index('index')
with h5py.File(cfg.velocity_fname, 'w') as f:
    f.create_dataset('Rat_Behavior', data=dfOri2.to_records())
    f.create_dataset('Events'      , data=dfevent.to_records())
    f.create_dataset('Sessions'    , data=dfsession.astype('|S').to_records())
