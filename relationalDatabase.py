import relationalDatabaseRat     as rDR
import relationalDatabaseEvent   as rDE
import relationalDatabaseSession as rDS
import h5py

f = h5py.File('datasets/relationalDatabase.h5', 'w')

f.create_dataset('Sessions', data=rDS.dfSessions.to_records())
f.create_dataset('Events', data=rDE.dfEvents.to_records())
f.create_dataset('Rat_Behavior', data=rDR.dfRatBehavior.to_records())
f.close()
