#!/bin/bash 

#SBATCH -J smooth_deaf
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/sm_deaf.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/sm_deaf.err 
#SBATCH -c 1
#SBATCH -a 1-60

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then sjname=sub-0${SLURM_ARRAY_TASK_ID}; else sjname=sub-${SLURM_ARRAY_TASK_ID}; fi

img_mica=/gpfs3/well/margulies/users/anw410/conts/my_imgs/micapipe-v0.2.2.simg
# sigma=1.699 # FWHM = 4mm
sigma=2.548 # FWHM = 6mm

dir_data=/gpfs3/well/margulies/users/anw410/data/Deafness/output
img_use=${sjname}/func/${sjname}_bold_fsLR-32k_cleaned.dtseries.nii
img_out=${sjname}/func/${sjname}_bold_fsLR-32k_cleaned_sm6.dtseries.nii

dir_stat=/gpfs3/well/margulies/users/anw410/data/Deafness/stat/
img_msk=deaf_mask_RAW-clean.dscalar.nii

dir_surf=/gpfs3/well/margulies/users/anw410/data/surfs
slh=S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii
srh=S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii

singularity exec -C --no-home \
    -B ${dir_data}:/mnt/data \
    -B ${dir_stat}:/mnt/stat \
    -B ${dir_surf}:/mnt/surf \
    $img_mica \
    wb_command -cifti-smoothing /mnt/data/${img_use} ${sigma} 0 COLUMN /mnt/data/${img_out} -left-surface /mnt/surf/${slh} -right-surface /mnt/surf/${srh} -cifti-roi /mnt/stat/${img_msk} -fix-zeros-surface -fix-zeros-volume