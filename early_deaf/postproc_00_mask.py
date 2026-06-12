import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from nilearn.interfaces.fmriprep import load_confounds
from nilearn import signal
import v_model_hsv as vmod

lab_data = 'Deafness'
dir_data = r'/gpfs3/well/margulies/users/anw410/data/'+lab_data+'/output' 
dir_save = r'/gpfs3/well/margulies/users/anw410/data/'+lab_data+'/stat' 

labs_l = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.L.label.gii').agg_data()
labs_r = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.R.label.gii').agg_data()
labs   = np.concatenate((labs_l, labs_r))

mutual_mask = np.zeros(59412)
for s in range(1,61):
    if s < 10:
        sjname = 'sub-0'+str(s)
    else:
        sjname = 'sub-'+str(s)

    img_dir  = os.path.join(dir_data, sjname, 'func')
    # img_lh   = nib.load(os.path.join(img_dir, 'lh.'+ sjname + '_bold_space-fsLR-cleaned.func.gii')).agg_data()
    # img_rh   = nib.load(os.path.join(img_dir, 'lh.'+ sjname + '_bold_space-fsLR-cleaned.func.gii')).agg_data()
    # img_data = np.concatenate((img_lh, img_rh), axis=1)
    # img_data_cortex = img_data[:, labs!=0]
    # img_data_cortex = nib.load(os.path.join(img_dir, sjname + '_rest_space-fsLR_den-91k_bold-clean.dtseries.nii')).get_fdata()[:,hcp.struct.cortex]
    img_data_cortex = np.load(os.path.join(img_dir, sjname + '_bold_91k_cleaned_ts.npy'))[:,hcp.struct.cortex]
    n_vl, n_vx = np.shape(img_data_cortex)
    img_mask = np.zeros(n_vx)
    img_data_std = img_data_cortex.std(axis=0)
    print(sjname + " : {0} NaNs".format(sum(img_data_std==0)))
    
    img_mask[img_data_std==0] = 1
    mutual_mask += img_mask

final_mask = np.ones(59412, dtype=int)
final_mask[mutual_mask!=0] = 0
final_mask_cortex = np.zeros((1,32492*2))
final_mask_cortex[0,:] = hcp.cortex_data(final_mask)

print("mutual-mask: {0} NaNs".format(sum(mutual_mask!=0)))

np.save(dir_save + '/deaf_mask_surf_RAW-clean.npy', final_mask_cortex)
vmod.v_save_cifti_surf(final_mask_cortex, dir_save, 'deaf_mask_RAW-clean.dscalar.nii')

    