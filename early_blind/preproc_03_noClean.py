import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

dir_ts  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts_sm/'
dir_tx0 = ['d2', 'd2', 'd3', 'd3', 'd4', 'd4']
dir_tx1 = ['blnd', 'ctrl', 'eb', 'sc', 'blind', 'sight']

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/'
mask_l = np.load(dir_mask + '4grp_LH_mask_470vls.npy')
mask_r = np.load(dir_mask + '4grp_RH_mask_470vls.npy')
mask   = np.concatenate((mask_l, mask_r))

dir_op1 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/blnd/micapipe_v0.2.0'
dir_op2 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/ctrl/micapipe_v0.2.0'
dir_op3 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/EB/micapipe_v0.2.0'
dir_op4 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/SC/micapipe_v0.2.0'
dir_op5 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_4/output/blind/micapipe_v0.2.0'
dir_op6 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_4/output/sight/micapipe_v0.2.0'
dir_out = [dir_op1, dir_op2, dir_op3, dir_op4, dir_op5, dir_op6]
dir_grp = ['blnd', 'ctrl', 'EB', 'SC', 'blind', 'sight']
dir_lab = ['desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX', 'desc-se_task-rest_acq-AP_bold_235vls_st', 'desc-se_task-rest_acq-AP_bold_235vls_st']

for g in range(len(dir_out)):
    sbj_lis_raw = [os.path.basename(x) for x in sorted(glob.glob(dir_out[g]+'/sub*'))]   
    sbj_lis     = sorted(sbj_lis_raw, key=len)
    
    for s in range(len(sbj_lis)):
        sj  = sbj_lis[s]
        print(sj)

        if g > 3:
            ts_l  = nib.load(dir_out[g]+'/'+sj+'/ses-01/func/'+dir_lab[g]+'/surf/sm4_msk_'+sj+'_hemi-L_surf-fsLR-32k_clean.func.gii').agg_data()
            ts_r  = nib.load(dir_out[g]+'/'+sj+'/ses-01/func/'+dir_lab[g]+'/surf/sm4_msk_'+sj+'_hemi-R_surf-fsLR-32k_clean.func.gii').agg_data()
        else:
            ts_l  = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/noFIX_sm4_'+sj+'_hemi-L_surf-fsLR-32k_clean.func.gii').agg_data()
            ts_r  = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/noFIX_sm4_'+sj+'_hemi-R_surf-fsLR-32k_clean.func.gii').agg_data()
            
        ts_lr = np.concatenate((ts_l, ts_r), axis=1)
        ts = ts_lr[:, mask!=0]

        np.save(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g], sj+'_sm4.npy'), ts)