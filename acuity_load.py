import pandas as pd
import h5py

path = 'VR_Acuity_Data/VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC/'
fname = 'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC.h5'
rat_position = pd.read_hdf(path+fname, '/preprocessed/Rigid Body/Rat/Position')

f = h5py.File(path+fname, 'r')

with h5py.File(path+fname) as f:
    attribute_names = [name  for name in f.attrs]
#print(attribute_names)


events = f['events']
eventNames = f['events']['eventNames']
eventArg = f['events']['eventArguments']

#print ([key for key in eventNames])
#print ([key for key in eventArg])
for key in eventArg:
    print(key)
