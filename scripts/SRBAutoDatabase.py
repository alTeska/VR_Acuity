import cfg
import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm

pd.options.mode.chained_assignment = None  # to be fixed


rat_auto = pd.DataFrame()
rat  = pd.read_hdf(cfg.velocity_fname, 'Rat_Behavior').set_index('index')
stim = pd.read_hdf(cfg.relational_fname, 'Events').set_index('index')
stim.drop(labels=['MotiveExpTimeSecs'], axis=1, inplace=True)

rat_s = pd.merge(rat, stim, on=['Frame', 'Time', 'session_id'])
rat_sf = rat_s[rat_s.Filtered == 1]

limits = pd.DataFrame(cfg.LIMITS)



# create limit columns
rat_sf['Dmin'], rat_sf['Dmax'] = 0, 0
rat_sf['change'] = False
for index, row in tqdm(limits.iterrows()):
rat_sf['change'] = (rat_sf['Dmin']==0) & (rat_sf['speed']==row['speed'])
    rat_sf['Dmin'] = np.where(rat_sf['change']==True, row['min'], rat_sf['Dmin'])
    rat_sf['Dmax'] = np.where(rat_sf['change']==True, row['max'], rat_sf['Dmax'])

rat_sf['SRB'] = (rat_sf['U'] > rat_sf['Dmin']) & (rat_sf['U'] < rat_sf['Dmax'])

# dropping unused columns
rat_sf.drop(['Filtered', 'change'], axis=1, inplace=True)


# MERGING SRB THAT HAVE REALLY SHORT BREAKS
rat_up2 = pd.DataFrame()
for name, dd in rat_sf.groupby('session_id'):
    # calculating dtime - time difference between srb
    dfSRBtemp = dd[dd['SRB']==True]
    dfSRBtemp['dtime'] = dfSRBtemp['Time'].diff(1)
    df2 = pd.merge(dd, dfSRBtemp[['dtime', 'Frame', 'session_id','Time']], on=['Frame', 'session_id','Time'], how='outer')
    df2.fillna(0, inplace=True)

    #special time cases
    dftemp = dfSRBtemp[(dfSRBtemp['dtime']>0.005) & (dfSRBtemp['dtime']<0.1)]
    dftemp = dftemp.reset_index(drop=True)

    maxF, minF = {}, {}
    minF={}
    df2['SRBall'] = df2['SRB']
    df2['SRBtt'] = False
    # merge super close events
    for i in np.arange(0,len(dftemp)):
        maxF[i] = dftemp.Time[i]
        minF[i] = maxF[i]-dftemp.dtime[i]

        df2['SRBtt'] = (df2['Time']>minF[i]) & (df2['Time']<maxF[i]) | (df2['SRBtt']==True)
        df2['SRBall'] = (df2['SRBtt']==True) | (df2['SRBall']==True)


    df2['dtimeA'] = df2['dtime']
    df2.drop('dtime', inplace=True, axis=1)

    # DELETING SHORT SRB
    # calculating dtime - time of srb
    dfSRBtemp2 = df2[df2['SRBall']==False]
    dfSRBtemp2['dtime'] = dfSRBtemp2['Time'].diff(1)
    df22 = pd.merge(df2, dfSRBtemp2[['dtime', 'Frame', 'session_id','Time']], on=['Frame', 'session_id','Time'], how='outer')
    df22.fillna(0, inplace=True)

    #special time cases
    dftemp2 = dfSRBtemp2[(dfSRBtemp2['dtime']<0.4) & (dfSRBtemp2['dtime']>0.0049)]
    dftemp2 = dftemp2.reset_index(drop=True)
    maxF2, minF2 = {}, {}
    df22['SRBall2'] = df22['SRBall']
    df22['SRBtt2'] = False

    # delete short events
    for i in np.arange(0,len(dftemp2)):
        maxF2[i] = dftemp2.Time[i]
        minF2[i] = dftemp2.Time[i] - dftemp2.dtime[i]
        df22['SRBtt2'] = ((df22['Time']>=minF2[i]) & (df22['Time']<=maxF2[i])) | (df22['SRBtt2']==True)
        df22['SRBall2'] = (df22['SRBtt2']==False) & (df22['SRBall2'] == True)

    rat_auto = pd.concat([rat_auto, df22], axis=0, ignore_index=True)


with h5py.File(cfg.SRBauto_fname, 'w') as f:
    f.create_dataset('Rat_Behavior', data=rat_auto.to_records())
