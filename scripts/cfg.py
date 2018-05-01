3# File names
relational_fname = 'datasets/preprocessed/relationalDatabase.h5'
velocity_fname = 'datasets/preprocessed/velocityDatabase.h5'
filtered_fname = 'datasets/preprocessed/filteredDatabase.h5'

# Rolling windows
WIDNOW_DATA = 20
WINDOW_DATA_CENTER = True
WINDOW_VELOCITY_CENTER = True

# Filtering values
FILT_REARING_YPOS = 0.13
FILT_CLEANING_YPOS = 0.07
FILT_CLEANING_YORI = -0.75
FILT_DTIME = 0.005
