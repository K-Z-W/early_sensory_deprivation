import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

data_lab = 'Deafness'
dir_data = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/output' 
dir_rgba = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat/rgba'
dir_stat = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat'

mask = np.load(os.path.join(dir_stat, 'deaf_mask_surf_RAW-clean.npy')).squeeze() 

parc_cortex = hcp.cortex_data(hcp.mmp.map_all[hcp.struct.cortex])
parc = parc_cortex[mask!=0]

from sklearn.linear_model import LinearRegression as LReg
from sklearn.metrics import r2_score

def v_ts_nnls_vertex(ts):
    ts_v1 = ts.T[(parc==1)|(parc==181),:].mean(axis=0)
    ts_s1 = ts.T[(parc==9)|(parc==51)|(parc==52)|(parc==53)|(parc==189)|(parc==231)|(parc==232)|(parc==233),:].mean(axis=0)
    ts_a1 = ts.T[(parc==24)|(parc==204),:].mean(axis=0)

    ts_x = np.vstack((ts_v1, ts_s1, ts_a1)).T
    ts_y = ts.copy()

    reg_nnls = LReg(positive=True)
    res_nnls = reg_nnls.fit(ts_x, ts_y)

    rgba = np.zeros((4,ts.shape[1]))
    rgba[:3,:] = res_nnls.coef_.T
    y_hat = res_nnls.predict(ts_x)
    rgba[3, :] = r2_score(ts_y, y_hat, multioutput='raw_values')

    return rgba


rgba_all = []
for s in range(1,61):
    if s < 10:
        sjname = 'sub-0'+str(s)
    else:
        sjname = 'sub-'+str(s)
        
    print(sjname)
    ts = nib.load(os.path.join(dir_data, sjname, 'func', sjname+'_bold_fsLR-32k_cleaned_sm6.dtseries.nii')).get_fdata()[:, mask!=0]

    rgba = v_ts_nnls_vertex(ts)
    rgba_all.append(rgba)

rgba_all = np.asarray(rgba_all)
print(rgba_all.shape)

np.save(dir_rgba + '/RGBA_deaf_cleaned_sm6.npy', rgba_all)