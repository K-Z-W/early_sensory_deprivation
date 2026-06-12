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

data_lab = 'Deafness'
dir_data = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/output' 
dir_stat = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat'
mask = np.load('/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat/deaf_mask_surf_RAW-clean.npy').squeeze()
res_th = nib.load(os.path.join(dir_stat, 'stat_clean_results', 'deaf_angle_cleaned-sm6_stat-param_clus-perm5000.dscalar.nii')).get_fdata().squeeze()
res_th_msk = res_th[mask!=0]

fc_all = []
for s in range(1,61):
    if s in [18,53]:
        continue
        
    if s < 10:
        sjname = 'sub-0'+str(s)
    else:
        sjname = 'sub-'+str(s)
        
    print(sjname)
    ts = nib.load(os.path.join(dir_data, sjname, 'func', sjname + '_bold_fsLR-32k_cleaned_sm6.dtseries.nii')).get_fdata()
    ts_use = ts.copy()[:,mask!=0]
    num_seed = len(np.unique(res_th_msk)) - 1
    ts_seed = np.zeros((num_seed, np.shape(ts_use)[0]))
    for d in range(num_seed):
        ts_seed[d,:] = ts_use[:, res_th_msk == d+1].mean(axis=1)
    fc = v_calc_fc(ts_seed, ts_use.T, ztransform=True)
    fc_all.append(fc)

fc_all = np.asarray(fc_all)
print(fc_all.shape)

for i in range(num_seed):
    np.save(os.path.join(dir_stat, 'stat_clean', 'fc_based-on-th_seed-0'+str(i+1)+'.npy'), fc_all[:,i,:])
        
        

























