#!/bin/bash 

img_mica=/gpfs3/well/margulies/users/anw410/conts/my_imgs/micapipe-v0.2.2.simg
sigma=2.548 # FWHM = 6mm

lab=Deafness
dir_data=/gpfs3/well/margulies/users/anw410/data/${lab}/output

dir_stat=/gpfs3/well/margulies/users/anw410/data/${lab}/stat/
img_msk=deaf_mask_RAW-clean.dscalar.nii

dir_surf=/gpfs3/well/margulies/users/anw410/data/surfs
slh=S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii
srh=S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii

for s in $(seq 60)
do
    if [ ${s} -lt 10 ]; then sjname=sub-0${s}; else sjname=sub-${s}; fi
    echo ${sjname}
    img_use=${sjname}/func/${sjname}_bold_fsLR-32k_cleaned.dtseries.nii
    img_out=${sjname}/func/${sjname}_bold_fsLR-32k_cleaned_sm6.dtseries.nii
    singularity exec -C --no-home \
        -B ${dir_data}:/mnt/data \
        -B ${dir_stat}:/mnt/stat \
        -B ${dir_surf}:/mnt/surf \
        $img_mica \
        wb_command -cifti-smoothing /mnt/data/${img_use} ${sigma} 0 COLUMN /mnt/data/${img_out} -left-surface /mnt/surf/${slh} -right-surface /mnt/surf/${srh} -cifti-roi /mnt/stat/${img_msk} -fix-zeros-surface -fix-zeros-volume

done