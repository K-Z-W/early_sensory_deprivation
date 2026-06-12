import os, sys, glob, math
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from sklearn.feature_selection import mutual_info_regression
from sklearn.neighbors import KernelDensity

#-------------------------
def estimate_entropy(data, bandwidth=0.2):
    
    kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(data.reshape(-1, 1))
    log_density = kde.score_samples(data.reshape(-1, 1))
    
    return -np.mean(log_density)

def v_NMI(ts_seed, ts_all):

    n_vert, n_vols = np.shape(ts_all)
    h_i = estimate_entropy(ts_seed)
    mat_nmi = np.zeros(n_vert)

    for j in range(n_vert):
        h_j = estimate_entropy(ts_all[j,:])
        mi = mutual_info_regression(ts_seed.reshape(-1, 1), ts_all[j, :])[0]
        mat_nmi[j] = mi / np.sqrt(h_i * h_j)

    return mat_nmi
#--------------------------------

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/'
mask_l = np.load(dir_mask + '4grp_LH_mask_470vls.npy')
mask_r = np.load(dir_mask + '4grp_RH_mask_470vls.npy')
mask   = np.concatenate((mask_l, mask_r))

dir_data = r'/gpfs3/well/margulies/users/anw410/data'
map_seed = np.load(dir_data + '/blindness/serious_3rd/results/6groups/angle_6grps_seed.npy')[mask!=0]

ts_all = np.load(str(sys.argv[1])).T
ts_seed = ts_all[map_seed==1, :].mean(axis=0)
nmi_mat = v_NMI(ts_seed, ts_all)

np.save(str(sys.argv[2]) + '/nmi_'+ str(sys.argv[3]) +'.npy', nmi_mat)
