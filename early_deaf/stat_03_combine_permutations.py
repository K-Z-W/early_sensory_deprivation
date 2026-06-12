import os, glob
import numpy as np

data_lab = 'Deafness'
dir_comb = '/gpfs3/well/margulies/users/anw410/data/' + data_lab + '/stat/perm_clean'
# dir_stat = ['th_param', 'th_nonparam', 'rd', 'grad']
dir_stat = ['fc']

for i in range(len(dir_stat)):
     
    if dir_stat[i] == 'grad':
        for j in range(3):
            dir_perm = os.path.join(dir_comb, dir_stat[i], 'g'+str(j+1))
            lis_perm = [os.path.basename(x) for x in sorted(glob.glob(dir_perm + '/*.npy'))]

            clus_max = np.zeros((3, 1))
            for k in range(len(lis_perm)):
                clus_perm = np.load(os.path.join(dir_perm, lis_perm[k]))
                clus_max  = np.hstack((clus_max, clus_perm))
                
            np.save(os.path.join(dir_comb, data_lab + '_clean-sm6_clus-perm5000_g' + str(j+1) + '.npy'), clus_max[:,1:])
            
    elif dir_stat[i] == 'fc':
        for j in range(3):
            dir_perm = os.path.join(dir_comb, dir_stat[i], 'fc'+str(j+1))
            lis_perm = [os.path.basename(x) for x in sorted(glob.glob(dir_perm + '/*.npy'))]

            clus_max = np.zeros((3, 1))
            for k in range(len(lis_perm)):
                clus_perm = np.load(os.path.join(dir_perm, lis_perm[k]))
                clus_max  = np.hstack((clus_max, clus_perm))
                
            np.save(os.path.join(dir_comb, data_lab + '_clean-sm6_clus-perm5000_fc' + str(j+1) + '.npy'), clus_max[:,1:])
    else:
        dir_perm = os.path.join(dir_comb, dir_stat[i])
        lis_perm = [os.path.basename(x) for x in sorted(glob.glob(dir_perm + '/*.npy'))]

        clus_max = np.zeros((3, 1))
        for k in range(len(lis_perm)):
            clus_perm = np.load(os.path.join(dir_perm, lis_perm[k]))
            clus_max  = np.hstack((clus_max, clus_perm))
            
        np.save(os.path.join(dir_comb, data_lab + '_clean-sm6_clus-perm5000_' + dir_stat[i] + '.npy'), clus_max[:,1:])