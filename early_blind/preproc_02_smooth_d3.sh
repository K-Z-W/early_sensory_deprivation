#!/bin/bash 

#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/sm_sc_output.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/sm_sc_error.err 
#SBATCH -c 1
#SBATCH -a 1-22,24

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

label1=SC
label2=sc
label3=desc-se_task-resting_bold_470vls_noFIX
if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then sjname=${label2}0${SLURM_ARRAY_TASK_ID}; else sjname=${label2}${SLURM_ARRAY_TASK_ID}; fi

img_mica=/gpfs3/well/margulies/users/anw410/conts/my_imgs/micapipe-v0.2.2.simg
sigma=1.699

dir_data=/well/margulies/users/anw410/data/blindness/dataset_3/outputs/${label1}/micapipe_v0.2.0/sub-${sjname}/func/${label3}/surf
dir_surf=/gpfs3/well/margulies/users/anw410/data/blindness/dataset_3/outputs/${label1}/micapipe_v0.2.0/sub-${sjname}/surf
dir_mask=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask
# msk_sflh=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/lh.4grp_mask_470vls.func.gii
# msk_sfrh=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask/rh.4grp_mask_470vls.func.gii

# singularity exec -C --no-home $img_mica \
#     wb_command -gifti-convert BASE64_BINARY \
#        ${dir_data}/sub-${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii \
#        ${dir_data}/sub-${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii
    
# singularity exec -C --no-home $img_mica \
#     wb_command -gifti-convert BASE64_BINARY \
#        ${dir_data}/sub-${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii \
#        ${dir_data}/sub-${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii    
    
singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -metric-smoothing /mnt/surf/sub-${sjname}_hemi-L_space-nativepro_surf-fsLR-32k_label-midthickness.surf.gii /mnt/data/sub-${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii ${sigma} /mnt/data/noFIX_sm4_sub-${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii -roi /mnt/mask/lh.4grp_mask_470vls.func.gii -fix-zeros
    
singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -metric-smoothing /mnt/surf/sub-${sjname}_hemi-R_space-nativepro_surf-fsLR-32k_label-midthickness.surf.gii /mnt/data/sub-${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii ${sigma} /mnt/data/noFIX_sm4_sub-${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii -roi /mnt/mask/rh.4grp_mask_470vls.func.gii -fix-zeros