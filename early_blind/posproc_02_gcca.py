import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from mvlearn.embed import GCCA

dir_ts  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts_sm/'
dir_tx0 = ['d2', 'd2', 'd3', 'd3', 'd4', 'd4']
dir_tx1 = ['blnd', 'ctrl', 'eb', 'sc', 'blind', 'sight']


gcca = GCCA(n_components=5)
ts_grp_all = []

for g in range(len(dir_tx0)):
    # sbj_lis = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g],'sub*.npy')))]
    sbj_lis_raw = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g],'sub*.npy')))]   
    sbj_lis     = sorted(sbj_lis_raw, key=len)

    for s in range(len(sbj_lis)):
        print(sbj_lis[s])
        ts = np.load(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g], sbj_lis[s]))
        ts_use = ts.copy()
        ts_norm = hcp.normalize(ts_use).T
        # print(ts_norm.shape)
        ts_grp_all.append(ts_norm)
        
# ts_grp_all = np.asarray(ts_grp_all)
# print(ts_grp_all.shape)

gcca_grp = gcca.fit_transform(ts_grp_all)
print(gcca_grp.shape)

np.save('/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/gcca/gcca_6grp_sm4.npy', gcca_grp)