##Single-datdataset creation
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = 'VR_Acuity_Data/datasets/'
fname = [
    'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC.h5',
    'VRAcuityExp_2017-07-13_15-05-16_VR-2B_NIC.h5',
    'VRAcuityExp_2017-07-13_15-19-09_VR-2A_EDU.h5',
    'VRAcuityExp_2017-07-13_15-38-34_VR-1A_NIC.h5',
    'VRAcuityExp_2017-07-13_15-53-40_VR-1B_NIC.h5',
    'VRAcuityExp_2017-07-13_16-11-46_VR-3A_NIC.h5',
    'VRAcuityExp_2017-07-13_16-27-08_VR-3A_NIC.h5',
    'VRAcuityExp_2017-07-13_17-09-07_VR-5A_NIC.h5',
]

#rat_orientation = pd.read_hdf(path+fname[0], '/preprocessed/Rigid Body/Rat/Orientation')

rat_position = {}
j = 0
for i,x in enumerate(fname):
    rat_position[i] = pd.read_hdf(path+fname[i], '/preprocessed/Rigid Body/Rat/Position')

#for i,x in enumerate(rat_position):
#    df.append(df2), ignore_index=True)

#print(rat_position[0])
#print(rat_position[1])

#DF = df0.append(df1, ignore_index=True, verify_integrity=True)
DF = pd.concat([rat_position[0], rat_position[2]], ignore_index=True)
#print(DF)
