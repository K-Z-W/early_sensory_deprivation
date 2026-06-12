import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

dir_op1 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_4/output/blind/micapipe_v0.2.0'
dir_op2 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_4/output/sight/micapipe_v0.2.0'
dir_out = [dir_op1, dir_op2]
dir_lab = 'desc-se_task-rest_acq-AP_bold_235vls_st'

parc_l = hcp.mmp.map_all[hcp.struct.cortex_left]
parc_r = hcp.mmp.map_all[hcp.struct.cortex_right]
parc   = hcp.mmp.map_all[hcp.struct.cortex]

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

for i in range(2):
    sbj_lis = [os.path.basename(x) for x in sorted(glob.glob(dir_out[i]+'/sub*'))]
    for n in range(len(sbj_lis)):        
        sj  = sbj_lis[n]
        print('saving gifti for ', sj)
        ts_lr = nib.load(dir_out[i]+'/'+sj+'/ses-01/func/'+dir_lab+'/surf/'+sj+'_ses-01_surf-fsLR-32k_desc-timeseries_clean.shape.gii').agg_data()
        v_save_gii(ts_lr.T, dir_out[i]+'/'+sj+'/ses-01/func/'+dir_lab+'/surf/', sj)