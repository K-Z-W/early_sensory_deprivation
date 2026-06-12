import os, sys
import numpy as np
import nibabel as nib
import pycircstat as circ
import networkx as nx
import hcp_utils as hcp
import scipy.stats as ss
from v_tfce_server import v_tfce_labeling, v_tfce_calc

def v_perm_tfce(data, n_perm, angle=False, parametric=False):

    tfce_max = np.zeros((2,n_perm))

    mask = np.ones(60, dtype=bool)
    mask[[17,52]] = False
    data = data[mask,:]
        
    n_sub, n_ver = np.shape(data)

    for i in range(n_perm):
        sub_order = np.arange(n_sub)
        np.random.shuffle(sub_order)
        data_perm = data[sub_order,:]

        data_g1 = data_perm[:19,:]
        data_g2 = data_perm[19:39,:]
        data_g3 = data_perm[39:,:]
        
        if angle:
            if parametric:
                _, tab_perm = circ.watson_williams(data_g1, data_g2, data_g3, axis=0)
                s_perm = [tab_perm[j].iloc[0,3] for j in range(len(tab_perm))]
                s_perm = np.asarray(s_perm)
            else:
                _, s_perm = circ.cmtest(data_g1, data_g2, data_g3, axis=0)

        else:
            if parametric:
                s_perm, _ = ss.f_oneway(data_g1, data_g2, data_g3, axis=0)
            else:
                s_perm, _ = ss.kruskal(data_g1, data_g2, data_g3, axis=0)
            
        s_perm[np.isnan(s_perm)] = 0
        data_stat = hcp.cortex_data(s_perm)
     
        tfce_map = v_tfce_calc(data_stat)
        tfce_max[0,i] = tfce_map[:32492].max() # left hemisphere
        tfce_max[1,i] = tfce_map[32492:].max() # right hemisphere

    return tfce_max

data_all = np.load(str(sys.argv[1]))
dir_save = str(sys.argv[2])
n_perm   = int(sys.argv[3])
metric_fix  = str(sys.argv[4])
params_fix  = str(sys.argv[5])
perm_fix = str(sys.argv[6])

if metric_fix=='angle':
    if params_fix=='parametric':
        tfce_max = v_perm_tfce(data_all, n_perm, angle=True, parametric=True)
    else:
        tfce_max = v_perm_tfce(data_all, n_perm, angle=True, parametric=False)
else:
    if params_fix=='parametric':
        tfce_max = v_perm_tfce(data_all, n_perm, angle=False, parametric=True)
    else:
        tfce_max = v_perm_tfce(data_all, n_perm, angle=False, parametric=False)
    
np.save(dir_save + '/Deaf_stat_'+ metric_fix +'_'+ params_fix +'_'+ perm_fix+ '.npy', tfce_max)

