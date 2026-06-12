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

dir_surf = '/gpfs3/well/margulies/users/anw410/data/surfs'
dir_mask = '/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask'

msk_lh = nib.load(dir_mask + '/lh.4grp_mask_470vls.func.gii').agg_data()
msk_rh = nib.load(dir_mask + '/rh.4grp_mask_470vls.func.gii').agg_data()
msk    = np.concatenate((msk_lh, msk_rh))

lh = nib.load(dir_surf + '/S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii')
rh = nib.load(dir_surf + '/S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii')
lh_vert, lh_face = lh.agg_data()
rh_vert, rh_face = rh.agg_data()

def v_cluster_labeling(data, thres, neg = False):

    data_lr = np.zeros(32492*2)
    data_lr[msk!=0] = data

    if neg:
        data_lr[data_lr > thres] = 0
    else:
        data_lr[data_lr < thres] = 0
    
    lr_mask = np.array(data_lr!=0, dtype=int)
    lh_mask = lr_mask[:32492]
    rh_mask = lr_mask[32492:]

    # left hemis 
    lh_mask_indices = np.where(lh_mask==1)[0]
    lh_mask_vertice = lh_vert[lh_mask_indices,:]

    G = nx.Graph()
    for i, vertex in enumerate(lh_vert):
        if i in lh_mask_indices:
            G.add_node(i, coords=vertex)
    for face in lh_face:
        if all(v in lh_mask_indices for v in face):
            G.add_edge(face[0], face[1])
            G.add_edge(face[1], face[2])
            G.add_edge(face[2], face[0])

    ccsL  = nx.connected_components(G) 
    lh_clus = []
    lh_clusize = []
    for ccl in ccsL:
        lh_clus.append(list(ccl))
        lh_clusize.append(len(ccl))
    lh_clusize = np.asarray(lh_clusize)

    # right hemis 
    rh_mask_indices = np.where(rh_mask==1)[0]
    rh_mask_vertice = rh_vert[rh_mask_indices,:]

    G = nx.Graph()
    for i, vertex in enumerate(rh_vert):
        if i in rh_mask_indices:
            G.add_node(i, coords=vertex)
    for face in rh_face:
        if all(v in rh_mask_indices for v in face):
            G.add_edge(face[0], face[1])
            G.add_edge(face[1], face[2])
            G.add_edge(face[2], face[0])

    ccsR  = nx.connected_components(G) 
    rh_clus = []
    rh_clusize = []
    for ccr in ccsR:
        rh_clus.append(list(ccr))
        rh_clusize.append(len(ccr))
    rh_clusize = np.asarray(rh_clusize)   

    return lh_clus, lh_clusize, rh_clus, rh_clusize

def v_clus_max(lh_clusize, rh_clusize):

    if (len(lh_clusize) > 0) & (len(rh_clusize) > 0):
        v_max = np.max((lh_clusize.max(), rh_clusize.max()))
    elif (len(lh_clusize) > 0) & (len(rh_clusize) == 0): 
        v_max = lh_clusize.max()
    elif (len(lh_clusize) == 0) & (len(rh_clusize) > 0): 
        v_max = rh_clusize.max()
    else:
        v_max = 0

    return v_max

def v_perm_clus(data, n_perm, angle=False):

    if angle:
        clus_max = np.zeros((3,n_perm))
    else:
        clus_max = np.zeros((3,n_perm))
        
    n_sub, n_ver = np.shape(data)

    for i in range(n_perm):
        sub_order = np.arange(n_sub)
        np.random.shuffle(sub_order)
        data_perm = data[sub_order,:]
        
        if angle:
            _, p_perm, _ = v_hkt(data_perm, factor_A, factor_B, chi_only=True, f_only=False)

            _, lh_clusize1, _, rh_clusize1 = v_cluster_labeling(p_perm[0,:], 0.001, neg=True)
            _, lh_clusize2, _, rh_clusize2 = v_cluster_labeling(p_perm[1,:], 0.001, neg=True)
            _, lh_clusize3, _, rh_clusize3 = v_cluster_labeling(p_perm[2,:], 0.001, neg=True)
            
            clus_max[0,i] = v_clus_max(lh_clusize1, rh_clusize1)
            clus_max[1,i] = v_clus_max(lh_clusize2, rh_clusize2)
            clus_max[2,i] = v_clus_max(lh_clusize3, rh_clusize3)
        
            
        else:

            _, p_perm = v_anova2_bs(data_perm, factor_A, factor_B, Covs, factor_names)
            
            _, lh_clusize1, _, rh_clusize1 = v_cluster_labeling(p_perm[0,:], 0.001, neg=True)
            _, lh_clusize2, _, rh_clusize2 = v_cluster_labeling(p_perm[1,:], 0.001, neg=True)
            _, lh_clusize3, _, rh_clusize3 = v_cluster_labeling(p_perm[2,:], 0.001, neg=True)
            
            clus_max[0,i] = v_clus_max(lh_clusize1, rh_clusize1)
            clus_max[1,i] = v_clus_max(lh_clusize2, rh_clusize2)
            clus_max[2,i] = v_clus_max(lh_clusize3, rh_clusize3)

    return clus_max


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
    clus_max = v_perm_clus(data_all, n_perm, angle=True)
else:    
    clus_max = v_perm_clus(data_all, n_perm, angle=False)
    
np.save(dir_save+'/aov_'+pre_fix+'_clus_perm_'+pos_fix+'_6grps.npy', clus_max)



