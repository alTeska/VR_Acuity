import cfg
import h5py
import pandas as pd

pd.options.mode.chained_assignment = None  # to be fixed
colChoice = ['X_Pos', 'Y_Pos', 'Z_Pos', 'X_Ori', 'Y_Ori', 'Z_Ori']


dfrat = pd.read_hdf(cfg.relational_fname, 'Rat_Behavior').set_index('index')
dfrat2 = pd.read_hdf(cfg.relational_fname, 'Rat_Behavior').set_index('index')

#filtering the dataset
dfrat2['Filtered_a'] =  dfrat['Y_Pos'] < cfg.FILT_REARING_YPOS
dfrat2['Filtered_b'] = (dfrat['Y_Ori'] > cfg.FILT_CLEANING_YORI) & (dfrat['Y_Pos'] > cfg.FILT_CLEANING_YPOS)

dfrat['Filtered'] = dfrat2['Filtered_a'] | dfrat2['Filtered_b']


# smoothing dataset
g = dfrat.groupby('session_id')
dfrat[colChoice] = g[colChoice].rolling(window=cfg.WIDNOW_DATA,
                                        center=cfg.WINDOW_DATA_CENTER).mean().values


dfrat.dropna(inplace=True)

dfevent   = pd.read_hdf(cfg.relational_fname, 'Events').set_index('index')
dfsession = pd.read_hdf(cfg.relational_fname, 'Sessions').set_index('index')

with h5py.File(cfg.filtered_fname, 'w') as f:
    f.create_dataset('Rat_Behavior', data=dfrat.to_records())
    f.create_dataset('Events'      , data=dfevent.to_records())
    f.create_dataset('Sessions'    , data=dfsession.astype('|S').to_records())
