import os, glob
import numpy as np 
import v_model_hsv as vmod 

dir_rgba = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/rgba_reg_unconstrained/'
dir_hsv  = r'/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/hsv_reg_unconstrained/'
tx0 = ['d2', 'd2', 'd3', 'd3', 'd4', 'd4']
tx1 = ['blnd', 'ctrl', 'eb', 'sc', 'blind', 'sight']

for i in range(len(tx0)):
    rgba = np.load(dir_rgba+'rgba_'+ tx0[i]+'_' + tx1[i] +'_regout.npy')
    print(rgba.shape)
    th_ind, rd_ind, th_grp, rd_grp, colors = vmod.v_hsv_model_rgba_indiv(rgba)
    print(th_ind.shape)
    np.save(dir_hsv + 'th_ind_' + tx0[i] + '_' + tx1[i] + '_reg_unconstrained.npy', th_ind)
    np.save(dir_hsv + 'th_grp_' + tx0[i] + '_' + tx1[i] + '_reg_unconstrained.npy', th_grp)
    np.save(dir_hsv + 'rd_ind_' + tx0[i] + '_' + tx1[i] + '_reg_unconstrained.npy', rd_ind)
    np.save(dir_hsv + 'rd_grp_' + tx0[i] + '_' + tx1[i] + '_reg_unconstrained.npy', rd_grp)
    np.save(dir_hsv + 'color_'  + tx0[i] + '_' + tx1[i] + '_reg_unconstrained.npy', colors)
    