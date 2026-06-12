import os, sys 
import numpy as np
import nibabel as nib 
import hcp_utils as hcp 
import scipy.stats as ss
import networkx as nx

# TFCE
def v_tfce_labeling(data, thres, neg = False):

    dir_surf = '/gpfs3/well/margulies/users/anw410/data/blindness/serious/material'

    lh = nib.load(dir_surf + '/S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii')
    rh = nib.load(dir_surf + '/S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii')
    lh_vert, lh_face = lh.agg_data()
    rh_vert, rh_face = rh.agg_data()

    
    data_lr = data.copy()

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
    

def v_tfce_calc(data, E=1.0, H=2.0): # data: 32492 * 2 vertices

    data_tfce = data.copy()
    data_tfce[data<0] = data_tfce[data<0] * -1
    data_tfce_min = data_tfce[data_tfce>0].min()
    data_tfce_max = data_tfce[data_tfce>0].max()
    dh = (data_tfce_max - data_tfce_min)/100

    tfce_map = np.zeros(32492 * 2)
    for h in np.arange(data_tfce_min, data_tfce_max, step = dh):
        lh_clus, lh_clusize, rh_clus, rh_clusize = v_tfce_labeling(data_tfce, h)
        e_lh = np.zeros(32492)
        e_rh = np.zeros(32492)
        for c in range(len(lh_clus)):
            e_lh[lh_clus[c]] = lh_clusize[c]
        for c in range(len(rh_clus)):
            e_rh[rh_clus[c]] = rh_clusize[c]

        e_lr = np.concatenate((e_lh, e_rh))
        tfce = (pow(h, H) * dh) * np.power(e_lr, E)
        tfce[data<0] = tfce[data<0] * -1
        tfce_map += tfce

    return tfce_map
