import cfg
import h5py
import pandas as pd

pd.options.mode.chained_assignment = None  # to be fixed


dfrat = pd.read_hdf(cfg.relational_fname, 'Rat_Behavior').set_index('index')
colChoice = ['X_Pos', 'Y_Pos', 'Z_Pos', 'X_Ori', 'Y_Ori', 'Z_Ori']

#filtering the dataset
dfratrear = dfrat[dfrat['Y_Pos'] < cfg.FILT_REARING_YPOS]
dfratclean = dfratrear[  (dfratrear['Y_Ori'] > cfg.FILT_CLEANING_YORI)
                       & (dfratrear['Y_Pos'] > cfg.FILT_CLEANING_YPOS)]

# smoothing dataset
g = dfratclean.groupby('session_id')
dfratclean[colChoice] = g[colChoice].rolling(window=cfg.WIDNOW_DATA,
                                             center=cfg.WINDOW_DATA_CENTER).mean().values

dfratclean.dropna(inplace=True)


dfevent   = pd.read_hdf(cfg.relational_fname, 'Events').set_index('index')
dfsession = pd.read_hdf(cfg.relational_fname, 'Sessions').set_index('index')

with h5py.File(cfg.filtered_fname, 'w') as f:
    f.create_dataset('Rat_Behavior', data=dfratclean.to_records())
    f.create_dataset('Events'      , data=dfevent.to_records())
    f.create_dataset('Sessions'    , data=dfsession.astype('|S').to_records())
