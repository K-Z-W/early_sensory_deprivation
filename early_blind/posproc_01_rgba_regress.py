import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

dir_ts  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts_sm/'
dir_tx0 = ['d2', 'd2', 'd3', 'd3', 'd4', 'd4']
dir_tx1 = ['blnd', 'ctrl', 'eb', 'sc', 'blind', 'sight']

labs_l = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.L.label.gii').agg_data()
labs_r = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.R.label.gii').agg_data()
labs   = np.concatenate((labs_l, labs_r))

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/'
mask_l = np.load(dir_mask + '4grp_LH_mask_470vls.npy')
mask_r = np.load(dir_mask + '4grp_RH_mask_470vls.npy')
mask   = np.concatenate((mask_l, mask_r))

parc_s = np.zeros(32492*2)
parc_s[labs!=0] = hcp.mmp.map_all[hcp.struct.cortex]
parc   = parc_s[mask!=0]

from sklearn.linear_model import LinearRegression as LReg
from sklearn.metrics import r2_score

def v_ts_nnls_vertex(ts, cov):
    ts_v1 = ts.T[(parc==1)|(parc==181),:].mean(axis=0)
    ts_s1 = ts.T[(parc==9)|(parc==51)|(parc==52)|(parc==53)|(parc==189)|(parc==231)|(parc==232)|(parc==233),:].mean(axis=0)
    ts_a1 = ts.T[(parc==24)|(parc==204),:].mean(axis=0)

    ts_x = np.vstack((ts_v1, ts_s1, ts_a1)).T
    ts_y = ts.copy()

    n_time, n_vert = np.shape(ts_y)
    reg = np.tile(cov, (n_time, 1))

    ts_x = np.hstack((ts_x, reg))
    
    reg_nnls = LReg(positive=False)
    res_nnls = reg_nnls.fit(ts_x, ts_y)

    rgba = np.zeros((4,ts.shape[1]))
    rgba[:3,:] = res_nnls.coef_.T[:3,:]
    y_hat = res_nnls.predict(ts_x)
    rgba[3, :] = r2_score(ts_y, y_hat, multioutput='raw_values')

    return rgba


reg = np.loadtxt('/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/regout/regress_var.txt')
k = 0
for g in range(len(dir_tx0)):
    rgba_all = []
    sbj_lis_raw = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g],'sub*.npy')))]   
    sbj_lis     = sorted(sbj_lis_raw, key=len)
    
    for s in range(len(sbj_lis)):
        print(sbj_lis[s])
        ts = np.load(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g], sbj_lis[s]))
        ts_use = ts.copy()

        cov = reg[k,:]
        rgba = v_ts_nnls_vertex(ts_use, cov)
        rgba_all.append(rgba)
        k += 1

    rgba_all = np.asarray(rgba_all)
    print(rgba_all.shape)

    np.save('/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/rgba_reg_unconstrained/rgba_'+dir_tx0[g]+'_'+dir_tx1[g]+'_regout.npy', rgba_all)