import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from mvlearn.embed import GCCA

data_lab = 'Deafness'
dir_data = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/output' 
dir_grad = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat/grad'
mask = np.load('/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat/deaf_mask_surf_RAW-clean.npy').squeeze()


gcca = GCCA(n_components=5)
ts_grp_all = []

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
    ts_norm = hcp.normalize(ts_use).T
    ts_grp_all.append(ts_norm)

gcca_grp = gcca.fit_transform(ts_grp_all)
print(gcca_grp.shape)

np.save(dir_grad + '/gcca_deaf_6grp_clean-sm6.npy', gcca_grp)