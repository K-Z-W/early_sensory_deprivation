import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

dir_com = r'/gpfs3/well/margulies/users/anw410/data/blindness/compare'
dir_op1 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/blnd/micapipe_v0.2.0'
dir_op2 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/ctrl/micapipe_v0.2.0'
dir_op3 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/EB/micapipe_v0.2.0'
dir_op4 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/SC/micapipe_v0.2.0'
dir_out = [dir_op1, dir_op2, dir_op3, dir_op4]
dir_grp = ['blnd', 'ctrl', 'EB', 'SC']
dir_lab = ['desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX']

parc_l = hcp.mmp.map_all[hcp.struct.cortex_left]
parc_r = hcp.mmp.map_all[hcp.struct.cortex_right]
parc   = hcp.mmp.map_all[hcp.struct.cortex]

# mask_l = nib.load('/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/scps/lh.smooth_msk_32k.func.gii').agg_data()
# mask_r = nib.load('/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/scps/rh.smooth_msk_32k.func.gii').agg_data()
# labs   = np.concatenate((mask_l, mask_r))

#---------------- Functions ------------------------------------------
def v_save_gii(data, dpath, fname):
    fl = data[:32492,:]
    fr = data[32492:,:]
    data_lh = nib.gifti.gifti.GiftiImage()
    data_lh.add_gifti_data_array(nib.gifti.gifti.GiftiDataArray(data=fl, datatype='NIFTI_TYPE_FLOAT32'))
    data_rh = nib.gifti.gifti.GiftiImage()
    data_rh.add_gifti_data_array(nib.gifti.gifti.GiftiDataArray(data=fr, datatype='NIFTI_TYPE_FLOAT32'))

    nib.save(data_lh, dpath + '/' + fname + '_hemi-L_surf-fsLR-32k_clean.func.gii') 
    nib.save(data_rh, dpath + '/' + fname + '_hemi-R_surf-fsLR-32k_clean.func.gii')
#--------------------------------------------------------------------

for i in range(4):
    rgba_all = []
    sbj_lis = [os.path.basename(x) for x in sorted(glob.glob(dir_out[i]+'/sub*'))]

    for n in range(len(sbj_lis)):        
        sj    = sbj_lis[n]
        print('saving gifti for ', sj)
        ts_lr = nib.load(dir_out[i]+'/'+sj+'/func/'+dir_lab[i]+'/surf/'+sj+'_surf-fsLR-32k_desc-timeseries_clean.shape.gii').agg_data()
        v_save_gii(ts_lr.T, dir_out[i]+'/'+sj+'/func/'+dir_lab[i]+'/surf/', sj)
    
