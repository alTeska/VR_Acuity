import relationalDatabaseEvent   as rDE
import relationalDatabaseSession as rDS
import numpy as np
import pandas as pd
import h5py


pd.options.mode.chained_assignment = None  # to be fixed

path = 'datasets/'

dfOri = pd.DataFrame()
dfOri2 = pd.DataFrame()
dfOriU = pd.DataFrame()

dfrat = pd.read_hdf(path+'filteredDatabase.h5', 'Rat_Behavior').set_index('index')
dfevent = pd.read_hdf(path+'relationalDatabase.h5', 'Events').set_index('index')

print('loaded')


## VECTORS WITHOUT Y
for name, dd in dfrat.groupby('session_id'):
    dd['dT'] = dd['Time'].diff(1)

    # calculating lenghts of VecX and VecZ and creation of shifted vectors   #dd = dd.apply(decompose_vec_df, axis=1)
    dd['lVo'] = np.linalg.norm(np.array([dd.X_Ori, dd.Y_Ori, dd.Z_Ori])  )
    dd['lx1'] = dd['X_Ori'] / dd['lVo']
    dd['lz1'] = dd['Z_Ori'] / dd['lVo']

    # normalize the data to unit vector form
    dd['V1'] = np.linalg.norm(np.array([dd.lx1, 0, dd.lz1]))
    dd['lx1'] = dd.lx1 / dd.V1
    dd['lz1'] = dd.lz1 / dd.V1

    dd['V1_ori'] = np.linalg.norm(np.array([dd.X_Ori, 0, dd.Z_Ori]))
    dd['lx1_ori'] = dd.X_Ori / dd.V1
    dd['lz1_ori'] = dd.Z_Ori / dd.V1

    dfOri = pd.concat([dfOri, dd], axis=0, ignore_index=True)

dfOri = dfOri.replace([np.inf, -np.inf], np.nan).dropna()

print('vectors')


## ANGLES and VELOCITY

# calculatinig the angles between X axis and the vectors
for name, dd in dfOri.groupby('session_id'):
    V1 = np.array([dd.lx1, 0, dd.lz1])
    V2 = np.array([1     , 0, 0     ])

#   theta0 = np.arccos(lx1*1 + lz1*0 / (np.linalg.norm(V1) * np.linalg.norm(V2)))
    dd['theta0'] = np.arccos(dd.lx1 / (np.linalg.norm(V1) * np.linalg.norm(V2)))
    dd['theta1'] = dd.theta0.shift(1)
    dd['theta']  = dd.theta0 - dd.theta1
    dd.drop({'theta0','theta1'}, axis=1, inplace=True)

    # angular velocity between two vectors
    dd['U'] = np.degrees(dd.theta)/ dd.dT
    dfOri2 = pd.concat([dfOri2, dd], axis=0, ignore_index=True)

dfOri2 = dfOri2.replace([np.inf, -np.inf], np.nan).dropna()

print('velocity')


## FILTERING HIGH DATA
dfOri2 = dfOri2[np.absolute(dfOri2['dT']) < 0.005] # filtering out big time gaps frame points
dfOri2 = dfOri2[np.absolute(dfOri2['U'])  < 600]   # too big velocities removal

print('filtered and smooth')


f = h5py.File(path+'velocityDatabase.h5', 'w')

# f.create_dataset('Sessions', data=rDS.dfSessions.to_records())
# f.create_dataset('Events', data=rDE.dfEvents.to_records())
f.create_dataset('Rat_Behavior', data=dfOri2.to_records())
f.close()
