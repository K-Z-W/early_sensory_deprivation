#!/bin/bash 

#SBATCH -D /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/sm_sight_output.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/scps/log/sm_sight_error.err 
#SBATCH -c 1
#SBATCH -a 4,5,6,8,9,11,12,13,14,15,16,18,19

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

sjname=sub-S${SLURM_ARRAY_TASK_ID}

img_mica=/gpfs3/well/margulies/users/anw410/conts/my_imgs/micapipe-v0.2.2.simg
sigma=1.699
dir_mask=/gpfs3/well/margulies/users/anw410/data/blindness/serious_3rd/data/mask

label1=sight
label2=ses-01
label3=desc-se_task-rest_acq-AP_bold_235vls_st

dir_data=/gpfs3/well/margulies/users/anw410/data/blindness/dataset_4/output/${label1}/micapipe_v0.2.0/${sjname}/${label2}/func/${label3}/surf
dir_surf=/gpfs3/well/margulies/users/anw410/data/blindness/dataset_4/output/${label1}/micapipe_v0.2.0/${sjname}/${label2}/surf

# convert to BASE64 GIFTI
singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -gifti-convert BASE64_BINARY /mnt/data/${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii /mnt/data/${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii

singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -gifti-convert BASE64_BINARY /mnt/data/${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii /mnt/data/${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii

# set structure for GIFTI files
singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -set-structure /mnt/data/${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii CORTEX_LEFT

singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -set-structure /mnt/data/${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii CORTEX_RIGHT


# smooth GIFTI file using FWHM-4 (sigma=1.699)
singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -metric-smoothing /mnt/surf/${sjname}_${label2}_hemi-L_space-nativepro_surf-fsLR-32k_label-midthickness.surf.gii /mnt/data/${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii ${sigma} /mnt/data/sm4_msk_${sjname}_hemi-L_surf-fsLR-32k_clean.func.gii -roi /mnt/mask/lh.4grp_mask_470vls.func.gii -fix-zeros

singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_surf}:/mnt/surf \
    -B ${dir_mask}:/mnt/mask \
    $img_mica \
    wb_command -metric-smoothing /mnt/surf/${sjname}_${label2}_hemi-R_space-nativepro_surf-fsLR-32k_label-midthickness.surf.gii /mnt/data/${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii ${sigma} /mnt/data/sm4_msk_${sjname}_hemi-R_surf-fsLR-32k_clean.func.gii -roi /mnt/mask/rh.4grp_mask_470vls.func.gii -fix-zeros