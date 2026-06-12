import os, sys, glob, math
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

#-------------------------
def v_calc_fc(ts_seed, ts_other, ztransform=False): # ts: seeds(or vertices) x time points
    
    fc = []

    if len(np.shape(ts_seed)) == 1:
        ts_seed = ts_seed[np.newaxis,:]
    
    num_seed, num_time1 = np.shape(ts_seed)
    num_vert, num_time2 = np.shape(ts_other)
    if num_time1 == num_time2:
        for i in range(num_seed):
            ts_seed_use = ts_seed[i,:]
            x = ts_seed_use[np.newaxis,:]
            y = ts_other.copy()
            cov = np.sum(((x - x.mean(axis=1))*(y - y.mean(axis=1, keepdims=True))), axis=1) / (num_time1 - 1)
            cor = cov / (np.std(x, axis=1, ddof=1) * np.std(y, axis=1, ddof=1))

            if ztransform:
                cor = np.arctanh(cor) # fisher-z transform

            fc.append(cor)
    else:
        raise ValueError('Time series length are not identical')

    fc = np.asarray(fc)

    return fc
#--------------------------------

dir_ts  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts_sm/'
dir_tx0 = ['d2', 'd2', 'd3', 'd3', 'd4', 'd4']
dir_tx1 = ['blnd', 'ctrl', 'eb', 'sc', 'blind', 'sight']

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/'
mask_l = np.load(dir_mask + '4grp_LH_mask_470vls.npy')
mask_r = np.load(dir_mask + '4grp_RH_mask_470vls.npy')
mask   = np.concatenate((mask_l, mask_r))

dir_data = r'/gpfs3/well/margulies/users/anw410/data'
map_seed = np.load(dir_data + '/blindness/serious_3rd/results/6groups/angle_6grps_seed.npy')[mask!=0]
num_seed = len(np.unique(map_seed)) - 1

fcz_all  = []
for d in range(num_seed):
    fcz_seed = np.zeros((98, sum(mask!=0)))    
    i = 0
    for g in range(len(dir_tx0)):
        # sbj_lis = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g],'sub*.npy')))]
        sbj_lis_raw = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g],'sub*.npy')))]   
        sbj_lis     = sorted(sbj_lis_raw, key=len)
        for s in range(len(sbj_lis)):
            print(sbj_lis[s])
            ts = np.load(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g], sbj_lis[s]))
            ts_seed = ts.T[map_seed==d+1, :].mean(axis=0)
            fcz_seed[i,:] = v_calc_fc(ts_seed, ts.T, ztransform=True)
            i += 1
    fcz_all.append(fcz_seed)

fcz_all = np.asarray(fcz_all)
print(fcz_all.shape)
np.save(dir_data + '/blindness/serious_3rd/results/6groups/fc/fcz_based_aov-th.npy', fcz_all)
