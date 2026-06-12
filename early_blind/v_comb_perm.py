import os, glob, sys
import numpy as np

dir_perm = str(sys.argv[1])
pre_perm = str(sys.argv[2])
dir_save = str(sys.argv[3])
pos_perm = str(sys.argv[4])
lis_perm = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(dir_perm, pre_perm + '*')))]

clus_max = np.zeros((3, 1))
for i in range(len(lis_perm)):
    clus_perm = np.load(os.path.join(dir_perm, lis_perm[i]))
    if clus_perm.shape[0] == 3:
        clus_max  = np.hstack((clus_max, clus_perm))
print(clus_max[:,1:].shape)

np.save(os.path.join(dir_save, pre_perm + pos_perm + '_comb5000.npy'), clus_max[:,1:])