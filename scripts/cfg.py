# File names
relational_fname = 'datasets/preprocessed/relationalDatabase.h5'
velocity_fname   = 'datasets/preprocessed/velocityDatabase.h5'
filtered_fname   = 'datasets/preprocessed/filteredDatabase.h5'
SRBauto_fname    = 'datasets/preprocessed/SRBautoDatabase.h5'

# Rolling windows
WIDNOW_DATA = 40
WINDOW_DATA_CENTER = True
WINDOW_VELOCITY_CENTER = True

# Filtering values
FILT_REARING_YPOS = 0.13
FILT_CLEANING_YPOS = 0.07
FILT_CLEANING_YORI = -0.75
FILT_DTIME = 0.005

# Automatic
LIMITS = ({'speed':[ 7, 14,  28, -7, -14  , -28],
           'min'  :[ 1,  5,  13, -9, -21.5, -30],
           'max'  :[ 9, 18,  30, -1, -5   , -13]})

CLOSE_SRB_LIM = [0.005 , 0.2]
SHORT_SRB_LIM = [0.0049, 0.4]
