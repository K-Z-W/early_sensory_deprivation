import os, sys
import numpy as np
import nibabel as nib 
import scipy.stats as ss
import pycircstat as circ
import networkx as nx
import pandas as pd
from scipy import special
from v_stat_anova_ols import v_anova2_bs
from v_stat_circ_hktest import v_hkt
from v_tfce_server import v_tfce_labeling, v_tfce_calc

dir_surf = '/gpfs3/well/margulies/users/anw410/data/surfs'
dir_mask = '/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask'

msk_lh = nib.load(dir_mask + '/lh.4grp_mask_470vls.func.gii').agg_data()
msk_rh = nib.load(dir_mask + '/rh.4grp_mask_470vls.func.gii').agg_data()
msk    = np.concatenate((msk_lh, msk_rh))

def v_perm_tfce(data, n_perm, angle=False):

    tfce_max = np.zeros((2,3,n_perm))
        
    n_sub, n_ver = np.shape(data)

    for i in range(n_perm):
        sub_order = np.arange(n_sub)
        np.random.shuffle(sub_order)
        data_perm = data[sub_order,:]
        
        if angle:
            s_perm, _, _ = v_hkt(data_perm, factor_A, factor_B, chi_only=True, f_only=False)
         
        else:
            s_perm, _ = v_anova2_bs(data_perm, factor_A, factor_B, Covs, factor_names)
            
        data_stat = np.zeros((3,32492*2))
        data_stat[:,msk!=0] = s_perm
    
        for j in range(3):
            tfce_map = v_tfce_calc(data_stat[j,:])
            tfce_max[0,j,i] = tfce_map[:32492].max() # left hemisphere
            tfce_max[1,j,i] = tfce_map[32492:].max() # right hemisphere

    return tfce_max


factor_A = np.concatenate((np.ones(17), np.ones(18)*2, np.ones(16), np.ones(23)*2, np.ones(11), np.ones(13)*2))
factor_B = np.concatenate((np.ones(17+18), np.ones(16+23)*2, np.ones(11+13)*3))

cov = np.asarray(pd.read_csv('/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/stats/6groups/palm/design_with_cov.csv', header=None))
Covs = cov[:,6:]
factor_names= ['Status', 'Sites', 'Sex', 'Age_dm']

data_all = np.load(str(sys.argv[1]))
dir_save = str(sys.argv[2])
n_perm   = int(sys.argv[3])
pre_fix  = str(sys.argv[4])
pos_fix  = str(sys.argv[5])

if pre_fix=='angle':
    tfce_max = v_perm_tfce(data_all, n_perm, angle=True)
else:    
    tfce_max = v_perm_tfce(data_all, n_perm, angle=False)
    
np.save(dir_save+'/aov_'+pre_fix+'_tfce_perm_'+pos_fix+'_6grps.npy', tfce_max)



