import pandas as pd
import h5py

path = 'VR_Acuity_Data/VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC/'
fname = 'VRAcuityExp_2017-07-13_14-39-17_VR-4A_NIC.h5'
rat_position = pd.read_hdf(path+fname, '/preprocessed/Rigid Body/Rat/Position')

xyz_mean = rat_position[['X', 'Y', 'Z']].mean()
print(xyz_mean)
