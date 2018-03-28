import cfg
import h5py
import ast
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm


def index_df(df):
    p = len(df.index)
    dfOut = df.set_index('i')
    dfOut = dfOut.reindex(range(0, df.i[p-1]+1))
    dfOut.fillna(method='pad', inplace=True)
    return dfOut


def make_dict(event):
    eventD = {}
    for i in range(0, len(event)-1):
        str_dict = event[i].decode('UTF-8').replace('\'', '\"')  # change to string
        n = str_dict.find('"attr"')  # find location of "attr"

        if n != -1:
            str_dict = str_dict='{' + str_dict[n:]
            dictionary = ast.literal_eval(str_dict)
            dictionary[dictionary['attr'] ] = dictionary.pop('value')
            del dictionary['attr']
        else:
            dictionary = ast.literal_eval(str_dict)
        eventD[i] = dictionary
    return eventD


fnames = glob('datasets/raw/*.h5')
key = '/preprocessed/Rigid Body/Rat/Orientation'

# EVENT:
eventArgs, eventlogs = {}, {}
df = pd.DataFrame()

for i, fname in tqdm(enumerate(fnames)):
    # Loading
    f = h5py.File(fname, 'r')
    eventlogs[i] = pd.read_hdf(fname, '/events/eventlog')
    eventArgs[i] = f['/events/']['eventArguments']
    eventArgs[i] = make_dict(eventArgs[i])  # cleaning event arguments values

    # split attr data into 3 dictionaries
    eventVis, eventSpe = {}, {}

    m, n = 0, 0
    x = eventArgs[i]
    for ii in range(0, len(x)-1):
        k = list(x[ii].keys())[0]
        if   k == 'visible':
            eventVis[m] = {'visible':x[ii]['visible'], 'i':ii}
            m += 1
        elif k == 'speed':
            eventSpe[n] = {'speed':x[ii]['speed'], 'i':ii}
            n += 1

    ddV = index_df(pd.DataFrame.from_dict(eventVis, orient='index'))
    ddS = index_df(pd.DataFrame.from_dict(eventSpe, orient='index'))

    # merging into one table of dataframes
    dd = pd.concat([eventlogs[i], ddV.visible], axis=1)
    dd = pd.concat([dd          , ddS.speed]  , axis=1)

    dd.fillna(method='pad', inplace=True)
    dd.fillna(0           , inplace=True)

    dd.drop({'Time'}, axis=1, inplace=True)
    dd.dropna(inplace=True)

    # recreation for full time frame
    dd = pd.merge(pd.read_hdf(fname, key), dd, on='Frame', how='left')
    dd.drop({'X', 'Y', 'Z'}, axis=1, inplace=True)
    dd.fillna(method='ffill', inplace=True)

    dd['session_id'] = i  # adding session id
    df = df.append(dd)


with h5py.File(cfg.relational_fname, 'a') as f:
    f.create_dataset('Events', data=df.to_records())
