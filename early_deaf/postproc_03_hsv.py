import os, glob
import numpy as np 
import v_model_hsv as vmod 

dir_rgba = r'/gpfs3/well/margulies/users/anw410/data/Deafness/stat/rgba'
dir_hsv  = r'/gpfs3/well/margulies/users/anw410/data/Deafness/stat/hsv'


rgba = np.load(dir_rgba+'/RGBA_deaf_cleaned_sm6.npy')
print(rgba.shape)

sj_msk = np.zeros(60)
sj_msk[:17] = 1
sj_msk[18]  = 1
sj_msk[19:40]=2
sj_msk[40:52]=3
sj_msk[53:] = 3

rgba_D = rgba[sj_msk==1,:,:]
rgba_H = rgba[sj_msk==2,:,:]
rgba_C = rgba[sj_msk==3,:,:]

print('D: {}'.format(np.shape(rgba_D)[0]))
print('H: {}'.format(np.shape(rgba_H)[0]))
print('C: {}'.format(np.shape(rgba_C)[0]))

th_ind_C, rd_ind_C, th_grp_C, rd_grp_C, colors_C = vmod.v_hsv_model_rgba_indiv(rgba_C)
th_ind_H, rd_ind_H, th_grp_H, rd_grp_H, colors_H = vmod.v_hsv_model_rgba_indiv(rgba_H)
th_ind_D, rd_ind_D, th_grp_D, rd_grp_D, colors_D = vmod.v_hsv_model_rgba_indiv(rgba_D)

np.save(dir_hsv + '/deaf_clean-sm6_th_ind_C.npy', th_ind_C)
np.save(dir_hsv + '/deaf_clean-sm6_th_grp_C.npy', th_grp_C)
np.save(dir_hsv + '/deaf_clean-sm6_rd_ind_C.npy', rd_ind_C)
np.save(dir_hsv + '/deaf_clean-sm6_rd_grp_C.npy', rd_grp_C)
np.save(dir_hsv + '/deaf_clean-sm6_colors_C.npy', colors_C)

np.save(dir_hsv + '/deaf_clean-sm6_th_ind_H.npy', th_ind_H)
np.save(dir_hsv + '/deaf_clean-sm6_th_grp_H.npy', th_grp_H)
np.save(dir_hsv + '/deaf_clean-sm6_rd_ind_H.npy', rd_ind_H)
np.save(dir_hsv + '/deaf_clean-sm6_rd_grp_H.npy', rd_grp_H)
np.save(dir_hsv + '/deaf_clean-sm6_colors_H.npy', colors_H)

np.save(dir_hsv + '/deaf_clean-sm6_th_ind_D.npy', th_ind_D)
np.save(dir_hsv + '/deaf_clean-sm6_th_grp_D.npy', th_grp_D)
np.save(dir_hsv + '/deaf_clean-sm6_rd_ind_D.npy', rd_ind_D)
np.save(dir_hsv + '/deaf_clean-sm6_rd_grp_D.npy', rd_grp_D)
np.save(dir_hsv + '/deaf_clean-sm6_colors_D.npy', colors_D)
    