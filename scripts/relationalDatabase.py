import h5py
import cfg


with h5py.File(cfg.relational_fname, 'w') as f:
    pass

# f.create_dataset('Sessions', data=rDS.dfSessions.to_records())
# f.create_dataset('Events', data=rDE.dfEvents.to_records())
# f.create_dataset('Rat_Behavior', data=rDR.dfRat.to_records())
