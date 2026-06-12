import os, sys, glob
import numpy as np
import nibabel as nib
import pandas as pd
import hcp_utils as hcp
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

dir_ts  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/ts_sm/'
dir_tx0 = ['d2', 'd2', 'd3', 'd3', 'd4', 'd4']
dir_tx1 = ['blnd', 'ctrl', 'eb', 'sc', 'blind', 'sight']

labs_l = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.L.label.gii').agg_data()
labs_r = nib.load('/gpfs3/well/margulies/users/anw410/data/surfs/fsLR.32k.R.label.gii').agg_data()
labs   = np.concatenate((labs_l, labs_r))

dir_mask = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/'
mask_l = np.load(dir_mask + '4grp_LH_mask_470vls.npy')
mask_r = np.load(dir_mask + '4grp_RH_mask_470vls.npy')
mask   = np.concatenate((mask_l, mask_r))

parc_s = np.zeros(32492*2)
parc_s[labs!=0] = hcp.mmp.map_all[hcp.struct.cortex]
parc   = parc_s[mask!=0]

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

vif_blind = np.zeros((98,3))
n = 0
for g in range(len(dir_tx0)):
    sbj_lis_raw = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g],'sub*.npy')))]   
    sbj_lis     = sorted(sbj_lis_raw, key=len)

    for s in range(len(sbj_lis)):
        print(sbj_lis[s])
        ts = np.load(os.path.join(dir_ts, dir_tx0[g], dir_tx1[g], sbj_lis[s]))
        vif_blind[n,:] = v_calc_vif(ts)
        n += 1

print(n)
np.save('/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/results/6groups/vif/vif_blind.npy', vif_blind)