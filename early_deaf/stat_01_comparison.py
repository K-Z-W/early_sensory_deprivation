import os, sys
import numpy as np
import nibabel as nib
import pycircstat as circ
import networkx as nx
import hcp_utils as hcp
import scipy.stats as ss

dir_surf = '/gpfs3/well/margulies/users/anw410/data/surfs'
lh = nib.load(dir_surf + '/S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii')
rh = nib.load(dir_surf + '/S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii')
lh_vert, lh_face = lh.agg_data()
rh_vert, rh_face = rh.agg_data()

def v_cluster_labeling(data, thres, neg = False, mask = False):

    if mask:
        data_msk = np.load('/gpfs3/well/margulies/users/anw410/data/Deafness/stat/deaf_mask_surf_RAW-clean.npy').squeeze()
        data_lr  = np.zeros(32492*2)
        data_lr[data_msk!=0] = data
    else:
        data_lr = hcp.cortex_data(data)

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


def v_perm_clus(data, n_perm, angle=False, parametric=False, exclude = False):
    
    clus_max = np.zeros((3,n_perm))

    if exclude:
        mask = np.ones(60, dtype=bool)
        mask[[17,52]] = False
        data = data[mask,:]

    n_sub, n_ver = np.shape(data)
    
    for i in range(n_perm):
        sub_order = np.arange(n_sub)
        np.random.shuffle(sub_order)
        data_perm = data[sub_order,:]

        data_g1 = data_perm[:18,:]
        data_g2 = data_perm[18:39,:]
        data_g3 = data_perm[39:,:]

        if angle:
            if parametric:
                p_perm, _ = circ.watson_williams(data_g1, data_g2, data_g3, axis=0)
            else:
                p_perm, _ = circ.cmtest(data_g1, data_g2, data_g3, axis=0)

        else:
            if parametric:
                _, p_perm = ss.f_oneway(data_g1, data_g2, data_g3, axis=0)
            else:
                _, p_perm = ss.kruskal(data_g1, data_g2, data_g3, axis=0)

        p_use = p_perm.copy()
        p_use[np.isnan(p_perm)] = 1
        _, lh_clusize, _, rh_clusize = v_cluster_labeling(p_use, 0.001, neg=True, mask = True)
        
        clus_max[0,i] = v_clus_max(lh_clusize, rh_clusize)

        if (len(lh_clusize) > 0) & (len(rh_clusize) > 0):
            clus_max[1,i] = lh_clusize.max()
            clus_max[2,i] = rh_clusize.max()
        elif (len(lh_clusize) > 0) & (len(rh_clusize) == 0): 
            clus_max[1,i] = lh_clusize.max()
            clus_max[2,i] = 0
        elif (len(lh_clusize) == 0) & (len(rh_clusize) > 0): 
            clus_max[1,i] = 0
            clus_max[2,i] = rh_clusize.max()
        else:
            clus_max[1:,i] = 0

    return clus_max
            
data_all = np.load(str(sys.argv[1]))
dir_save = str(sys.argv[2])
n_perm   = int(sys.argv[3])
metric_fix  = str(sys.argv[4])
params_fix  = str(sys.argv[5])
perm_fix = str(sys.argv[6])

ex = False
if metric_fix=='angle':
    if params_fix=='parametric':
        clus_max = v_perm_clus(data_all, n_perm, angle=True, parametric=True, exclude = ex)
    else:
        clus_max = v_perm_clus(data_all, n_perm, angle=True, parametric=False, exclude = ex)
else:
    if params_fix=='parametric':
        clus_max = v_perm_clus(data_all, n_perm, angle=False, parametric=True, exclude = ex)
    else:
        clus_max = v_perm_clus(data_all, n_perm, angle=False, parametric=False, exclude = ex)

np.save(dir_save + '/Deaf_clean-sm6_stat_'+ metric_fix +'_'+ params_fix +'_'+ perm_fix+ '.npy', clus_max)

















