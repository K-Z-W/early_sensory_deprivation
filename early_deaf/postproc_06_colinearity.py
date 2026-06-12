import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

data_lab = 'Deafness'
dir_data = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/output' 
dir_stat = '/gpfs3/well/margulies/users/anw410/data/'+data_lab+'/stat'

mask = np.load(os.path.join(dir_stat, 'deaf_mask_surf_RAW-clean.npy')).squeeze() 

parc_cortex = hcp.cortex_data(hcp.mmp.map_all[hcp.struct.cortex])
parc = parc_cortex[mask!=0]

def v_calc_vif(ts):

    vif_calc = np.zeros(3)
    ts_v1 = ts.T[(parc==1)|(parc==181),:].mean(axis=0)
    ts_s1 = ts.T[(parc==9)|(parc==51)|(parc==52)|(parc==53)|(parc==189)|(parc==231)|(parc==232)|(parc==233),:].mean(axis=0)
    ts_a1 = ts.T[(parc==24)|(parc==204),:].mean(axis=0)

    df_ts = pd.DataFrame({'V':ts_v1, 'S':ts_s1, 'A':ts_a1})
    vif_calc[0] = vif(df_ts.values, 0)
    vif_calc[1] = vif(df_ts.values, 1)
    vif_calc[2] = vif(df_ts.values, 2)

    return vif_calc

vif_deaf = np.zeros((60,3))
n = 0
for s in range(1,61):
    if s < 10:
        sjname = 'sub-0'+str(s)
    else:
        sjname = 'sub-'+str(s)
        
    print(sjname)
    ts = nib.load(os.path.join(dir_data, sjname, 'func', sjname+'_bold_fsLR-32k_cleaned_sm6.dtseries.nii')).get_fdata()[:, mask!=0]

    vif_deaf[n,:] = v_calc_vif(ts)
    n += 1

print(n)
np.save(dir_stat + '/vif/vif_deaf.npy', vif_deaf)