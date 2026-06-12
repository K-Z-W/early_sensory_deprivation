import os, sys, glob, math
import numpy as np
import nibabel as nib
import hcp_utils as hcp

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask'
dir_op1 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/blnd/micapipe_v0.2.0'
dir_op2 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/ctrl/micapipe_v0.2.0'
dir_op3 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/EB/micapipe_v0.2.0'
dir_op4 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/SC/micapipe_v0.2.0'
dir_out = [dir_op1, dir_op2, dir_op3, dir_op4]
dir_grp = ['blnd', 'ctrl', 'EB', 'SC']
dir_lab = ['desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX']

msk = np.ones(32492*2)

for g in range(4):
    sbj_lis = [os.path.basename(x) for x in sorted(glob.glob(dir_out[g]+'/sub*'))]
    for s in range(len(sbj_lis)):
        sj    = sbj_lis[s]
        print(sj)
        # ts_l  = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/'+sj+'_hemi-L_surf-fsLR-32k_clean.func.gii').agg_data()
        # ts_r  = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/'+sj+'_hemi-R_surf-fsLR-32k_clean.func.gii').agg_data()
        # ts_lr = np.concatenate((ts_l, ts_r))
        ts_lr = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/'+sj+'_surf-fsLR-32k_desc-timeseries_clean.shape.gii').agg_data().T

        if ts_lr.shape[0]!=msk.shape:
            Exception("Concatenation direction is wrong")

        ts_chk = np.abs(ts_lr)
        ts_sum = np.apply_along_axis(math.fsum, 1, ts_chk)

        ts_msk = np.ones(32492*2)
        ts_msk[ts_sum==0] = 0

        msk = msk * ts_msk

msk_lh = msk[:32492]
msk_rh = msk[32492:]

labs_l = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.L.label.gii').agg_data()
labs_r = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.R.label.gii').agg_data()

msk_new_lh = np.zeros(32492)
msk_new_rh = np.zeros(32492)

msk_new_lh[labs_l!=0] = msk_lh[labs_l!=0]
msk_new_rh[labs_r!=0] = msk_rh[labs_r!=0]
msk_new = np.concatenate((msk_new_lh, msk_new_rh))

np.save(os.path.join(dir_mask, '4grp_LH_mask_470vls.npy'), msk_new_lh)
np.save(os.path.join(dir_mask, '4grp_RH_mask_470vls.npy'), msk_new_rh)

print('Total number of zeros is ', str(sum(msk_new==0) - 5572))

def v_save_gii(data, savepath, savename, half=False):

    if half:
        data_lh = nib.gifti.gifti.GiftiImage()
        data_lh.add_gifti_data_array(nib.gifti.gifti.GiftiDataArray(data, datatype='NIFTI_TYPE_FLOAT32'))

        savename_lh = 'lh.'+savename+'.func.gii'
        nib.save(data_lh, os.path.join(savepath, savename_lh))
    else:
        data_lh = nib.gifti.gifti.GiftiImage()
        data_lh.add_gifti_data_array(nib.gifti.gifti.GiftiDataArray(data[:32492], datatype='NIFTI_TYPE_FLOAT32'))
        data_rh = nib.gifti.gifti.GiftiImage()
        data_rh.add_gifti_data_array(nib.gifti.gifti.GiftiDataArray(data[32492:], datatype='NIFTI_TYPE_FLOAT32'))

        savename_lh = 'lh.'+savename+'.func.gii'
        nib.save(data_lh, os.path.join(savepath, savename_lh))
        savename_rh = 'rh.'+savename+'.func.gii'
        nib.save(data_rh, os.path.join(savepath, savename_rh))

v_save_gii(msk_new, dir_mask, '4grp_mask_470vls')