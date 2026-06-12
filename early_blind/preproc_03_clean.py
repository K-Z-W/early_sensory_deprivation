import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp

dir_ts  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts/'
dir_txt = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/regout/'
dir_tx0 = ['d2', 'd2', 'd3', 'd3']
dir_tx1 = ['blnd', 'ctrl', 'eb', 'sc']

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/'
mask_l = np.load(dir_mask + '4grp_LH_mask_470vls.npy')
mask_r = np.load(dir_mask + '4grp_RH_mask_470vls.npy')
mask   = np.concatenate((mask_l, mask_r))

dir_op1 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/blnd/micapipe_v0.2.0'
dir_op2 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_2/outputs/ctrl/micapipe_v0.2.0'
dir_op3 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/EB/micapipe_v0.2.0'
dir_op4 = r'/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/SC/micapipe_v0.2.0'
dir_out = [dir_op1, dir_op2, dir_op3, dir_op4]
dir_grp = ['blnd', 'ctrl', 'EB', 'SC']
dir_lab = ['desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-rest_run-01_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX', 'desc-se_task-resting_bold_470vls_noFIX']


from sklearn.linear_model import LinearRegression as LReg
def v_ts_regressout(ts, regout):

    ts_y = ts.copy()
    n_time, n_vert = np.shape(ts_y)
    if n_time > n_vert:
        Exception("wrong axis")
        
    ts_x = np.tile(regout, (n_time, 1))

    reg_sdls = LReg()
    res_sdls = reg_sdls.fit(ts_x, ts_y)

    y_residual = ts_y - res_sdls.predict(ts_x)

    return y_residual

for g in range(4):
    sbj_lis = [os.path.basename(x) for x in sorted(glob.glob(dir_out[g]+'/sub*'))]
    sex_lis = np.loadtxt(dir_txt + dir_tx0[g] + '_' + dir_tx1[g] + '_sex.txt')
    age_lis = np.loadtxt(dir_txt + dir_tx0[g] + '_' + dir_tx1[g] + '_age.txt')
    if (len(sbj_lis)!=len(sex_lis)) or (len(sbj_lis)!=len(age_lis)):
        Exception("numbers of variables are not eaqual")
    
    for s in range(len(sbj_lis)):
        sj    = sbj_lis[s]
        print(sj)
        regout = np.zeros((1,2))
        regout[0,0] = sex_lis[s]
        regout[0,1] = age_lis[s]
    
        ts_l  = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/noFIX_sm4_'+sj+'_hemi-L_surf-fsLR-32k_clean.func.gii').agg_data()
        ts_r  = nib.load(dir_out[g]+'/'+sj+'/func/'+dir_lab[g]+'/surf/noFIX_sm4_'+sj+'_hemi-R_surf-fsLR-32k_clean.func.gii').agg_data()
        ts_lr = np.concatenate((ts_l, ts_r), axis=1)

        ts = ts_lr[:, mask!=0]
        ts_sav = v_ts_regressout(ts, regout)

        np.save(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g], sj+'_clean_reg_470vls_noFIX.npy'), ts_sav)