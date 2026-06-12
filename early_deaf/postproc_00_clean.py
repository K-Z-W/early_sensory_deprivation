import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from nilearn.interfaces.fmriprep import load_confounds
from nilearn import signal
import v_model_hsv as vmod

dir_data = r'/gpfs3/well/margulies/users/anw410/data/Deafness/output' 

labs_l = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.L.label.gii').agg_data()
labs_r = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.R.label.gii').agg_data()
labs   = np.concatenate((labs_l, labs_r))

for s in range(1,61):
    if s < 10:
        sjname = 'sub-0'+str(s)
    else:
        sjname = 'sub-'+str(s)

    print(sjname)
    img_dir = os.path.join(dir_data, sjname, 'func')
    img     = os.path.join(img_dir, sjname+'_task-rest_run-1_space-fsLR_den-91k_bold.dtseries.nii')
    img_data= nib.load(img).get_fdata()
    confs, samp_msk = load_confounds(img, strategy=('motion', 'high_pass', 'compcor'), motion='full', compcor='anat_combined', n_compcor=5, demean=False)
    img_clean = signal.clean(img_data, detrend=True, standardize='zscore_sample', sample_mask=samp_msk, confounds=confs, high_pass=0.01, low_pass=0.08, t_r=1.66, ensure_finite=True, extrapolate=False)
    cleaned_signal_cortex = img_clean[:,hcp.struct.cortex]
    cleaned_signal_surf = np.zeros((len(samp_msk), 32492*2))
    cleaned_signal_surf[:, labs!=0] = cleaned_signal_cortex

    np.save(os.path.join(img_dir, sjname + '_bold_91k_cleaned_ts.npy'), img_clean)
    vmod.v_save_cifti_surf(cleaned_signal_surf, img_dir, sjname + '_bold_fsLR-32k_cleaned.dtseries.nii')
