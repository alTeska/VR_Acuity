import relationalDatabaseEvent   as rDE
import relationalDatabaseSession as rDS
import numpy as np
import pandas as pd
import h5py

pd.options.mode.chained_assignment = None  # to be fixed

windowsize = 100

path = 'datasets/'
dfrat = pd.read_hdf(path+'relationalDatabase.h5', 'Rat_Behavior').set_index('index')

colChoice = ['X_Pos', 'Y_Pos', 'Z_Pos', 'X_Ori', 'Y_Ori', 'Z_Ori']

#filtering the dataset
dfratrear = dfrat[dfrat['Y_Pos'] < 0.13]
dfratclean = dfratrear[  (dfratrear['Y_Ori'] > -0.75)
                       & (dfratrear['Y_Pos'] > 0.07)]

# smoothing dataset
g = dfratclean.groupby('session_id')
dfratclean[colChoice] = g[colChoice].rolling(window=windowsize).mean().values

dfratclean.dropna(inplace=True)

f = h5py.File('datasets/filteredDatabase.h5', 'w')

f.create_dataset('Sessions', data=rDS.dfSessions.to_records())
f.create_dataset('Events', data=rDE.dfEvents.to_records())
f.create_dataset('Rat_Behavior', data=dfratclean.to_records())
f.close()
