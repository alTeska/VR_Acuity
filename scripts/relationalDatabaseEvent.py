# Script for creation of new dataset - analogical to VR_Acuity_Relational_Database_ER_Diagram.pdf
import pandas as pd
import h5py
import ast


def index_df(df):
    p = len(df.index)
    l = df.i[p-1]
    dfOut = df.set_index('i')
    dfOut = dfOut.reindex(range(0, l+1))
    dfOut.fillna(method='pad', inplace=True)
    return dfOut


def make_dict(event):
    eventD = {}
    for i in range(0, len(event)-1):
        # change to string in proper format
        str_dict = event[i].decode('UTF-8').replace('\'', '\"')
        # find location of "attr"
        n = str_dict.find('"attr"')

        if n != -1:
            str_dict = str_dict='{' + str_dict[n:]
            dictionary = ast.literal_eval(str_dict)
            dictionary[dictionary['attr'] ] = dictionary.pop('value')
            del dictionary['attr']
        else:
            dictionary = ast.literal_eval(str_dict)
        eventD[i] = dictionary
    return eventD


fname = glob('../datasets/raw/*.h5')

# EVENT:
key = '/events/'

eventArg  = {}
eventName = {}
eventlog  = {}
dfOri = {}

# Loading
for i, x in enumerate(fname):
    eventlog[i]  = pd.read_hdf(path+x+'.h5', key+'eventlog')

    fileName = h5py.File(path+x+'.h5', 'r')
    eventArg[i]  = fileName[key]['eventArguments']
    eventName[i] = fileName[key]['eventNames']

# loading original files - for full time/frame series data
key = '/preprocessed/Rigid Body/Rat/Orientation'

for i, x in enumerate(fname):
    dfOri[i] = pd.read_hdf(x, key)


# cleaning event arguments values
eventA = {}
for i, str_dict in enumerate(fname):
    eventA[i] = make_dict(eventArg[i])

# split attr data into 3 dictionaries
DFVis = {}
DFSpe = {}
# DFDur = {}

# split into 3 dictionaries
DFVis = {}
DFSpe = {}
DFDur = {}

for i in range(0, len(fname)):
    eventVis = {}
    eventSpe = {}
    eventDur = {}

    x = eventA[i]
    j, m, n = 0, 0, 0
    for ii in range(0, len(x)-1):
        k = list(x[ii].keys())[0]
        if   k == 'visible':
            eventVis[m] = {'visible':x[ii]['visible'], 'i':ii}
            m += 1
        elif k == 'speed':
            eventSpe[n] = {'speed':x[ii]['speed'], 'i':ii}
            n += 1
        elif k == 'duration':
            eventDur[j] = {'duration':x[ii]['duration'], 'i':ii}
            j += 1

    DFVis[i] = pd.DataFrame.from_dict(eventVis, orient='index')
    DFSpe[i] = pd.DataFrame.from_dict(eventSpe, orient='index')
    #DFDur[i] = pd.DataFrame.from_dict(eventDur, orient='index')

DFV = {}
DFS = {}
for i in range(0, len(fname)):
    DFV[i] = index_df(DFVis[i])
    DFS[i] = index_df(DFSpe[i])

# merging into one table of dataframes
df = {}
for i in range(0, len(fname)):
    df[i] = pd.concat([eventlog[i], DFV[i].visible], axis=1)
    df[i] = pd.concat([df[i]      , DFS[i].speed]  , axis=1)

    df[i].fillna(method='pad', inplace=True)
    df[i].fillna(0, inplace=True)

# creation of all time data series with events - filling in the time series
dfM = {}
for i, x in enumerate(fname):
    df1 = df[i].dropna()
    df1.drop({'Time'}, axis=1, inplace=True)

    dfM[i] = pd.merge(dfOri[i], df1, on='Frame', how='left')
    dfM[i].drop({'X', 'Y', 'Z'}, axis=1, inplace=True)

    dfM[i].fillna(method='ffill', inplace=True)


dfEvents = pd.DataFrame()

for i, x in enumerate(fname):
    # adding session id
    dfM[i]['session_id'] = i

    # merging into one dataset
    dfEvents = pd.concat([dfEvents, dfM[i]], axis=0, ignore_index=True)

dfEvents.to_hdf(path+'relationaDatabase.h5', 'Events')
