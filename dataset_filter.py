# Script for filtering and creation of new dataset based on DataFilter.ipynb
import numpy as np
import pandas as pd

dfPos = {}
dfOri = {}
df    = {}
dfV = {}

path = 'datasets/'
key = '/preprocessed/Rigid Body/Rat/'
index = {'X', 'Y', 'Z'}
h5 = '.h5'

hyperparam = { 'BPFlimit' : 0.5 ,
               'LPFlimit' : 0.13,
               'MOVElimit': 0.02,}

sum_raw  = 0
sum_fil  = 0
sum_fil1 = 0
sum_fil2 = 0
sum_fil3 = 0

fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC', ]

# LOADING DATA
for i, x in enumerate(fname):
    dfPos[i] = pd.read_hdf(path+x+'_clean'+h5, 'Position')
    dfOri[i] = pd.read_hdf(path+x+'_clean'+h5, 'Orientation')
    sum_raw += len(dfPos[i])


# APPLYING FILTERS
# removal of rearing positions
for i, x in enumerate(fname):
    dfPos[i] = dfPos[i][dfPos[i]['Y'] < hyperparam['LPFlimit']]
    sum_fil1 += len(dfPos[i])

print('1. filtered data size: %f%%' % (sum_fil1*100/sum_raw))
# "scratching" removal
for i, x in enumerate(fname):
    dfOri[i] = dfOri[i][dfOri[i]['Y'] < hyperparam['BPFlimit']]
    dfOri[i] = dfOri[i][dfOri[i]['Y'] >-hyperparam['BPFlimit']]
    sum_fil2 += len(dfOri[i])

print('2. filtered data size: %f%%' % (sum_fil2*100/sum_raw))
# additional dataset for movment analysis - too fast removed
for i, x in enumerate(fname):
    # extraction of positon and time changes
    dfV[i] = dfPos[i].diff()
    dfV[i].Frame = dfPos[i].Frame
    dfV[i].dropna(inplace=True)

    # calculating velocity in all axes
    dfV[i]['dX'] = dfV[i].apply(lambda row: np.absolute(row.X) / row.Time, axis=1)
    dfV[i]['dY'] = dfV[i].apply(lambda row: np.absolute(row.Y) / row.Time, axis=1)
    dfV[i]['dZ'] = dfV[i].apply(lambda row: np.absolute(row.Z) / row.Time, axis=1)
    dfV[i].rename(columns={"Time":'dTime'}, inplace=True)
    dfV[i].drop({'X', 'Y', 'Z'}, axis=1, inplace=True)

    # diagonal velocity
    dfV[i]['Vxyz'] = dfV[i].apply(lambda row: np.sqrt(row.dX**2 + row.dY**2 + row.dZ**2), axis=1)

# fast movment removal
for i, x in enumerate(fname):
    dfV[i] = dfV[i][dfV[i]['Vxyz'] < hyperparam['MOVElimit']]
    sum_fil3 += len(dfV[i])
    #for k in index:
    #    dfV[i] = dfV[i][dfV[i][k] < hyperparam['MOVElimit']]


print('3. filtered data size: %f%%' % (sum_fil3*100/sum_raw))
# DATA MERGING - BASED ON FRAME
for i, x in enumerate(fname):
    df[i] = pd.merge( pd.merge(dfPos[i], dfOri[i], on='Frame', suffixes=('_Pos', '_Ori')), dfV[i], on='Frame')
    sum_fil += len(df[i])
    #print(i, df[i].keys())

print('final filtered data size: %f%%' % (sum_fil*100/sum_raw))

# SAVING DATA TO FILES
for i, x in enumerate(fname):
    df[i].to_hdf(path+x+'_filter'+h5, 'Full', table=True)
