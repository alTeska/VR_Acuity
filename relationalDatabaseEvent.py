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


fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC', ]

# EVENT:
key = '/events/'
path = 'datasets/'

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
    dfOri[i] = pd.read_hdf(path+fname[i]+'.h5', key)


# cleaning event arguments values
eventA = {}
for i, str_dict in enumerate(fname):
    eventA[i] = make_dict(eventArg[i])

# split attr data into 3 dictionaries
DFVis = {}
DFSpe = {}
# DFDur = {}

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
    # DFDur[i] = pd.DataFrame.from_dict(eventDur, orient='index')


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
ii = 0
dfM = {}
for ii, x in enumerate(fname):
    df1 = df[ii].dropna()
    df1.drop({'Time'}, axis=1, inplace=True)

    dfM[ii] = pd.merge(dfOri[ii], df1, on='Frame', how='left')
    dfM[ii].drop({'X', 'Y', 'Z'}, axis=1, inplace=True)

    dfM[ii].fillna(method='ffill', inplace=True)


dfEvents = pd.DataFrame()

# adding session id and merging into one dataset
for ii, x in enumerate(fname):
    dfM[i]['session_id'] = i
    dfEvents = pd.concat([dfEvents, dfM[i]], axis=0, ignore_index=True)


dfEvents.to_hdf(path+'relationaDatabase.h5', 'Events')
