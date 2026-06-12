#!/bin/bash 

#SBATCH -J QC_deaf
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/QC_deaf.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/QC_deaf.err 
#SBATCH -c 4

img_mriqc=/gpfs3/well/margulies/users/anw410/conts/my_imgs/mriqc_v24.0.1.simg
dir_bids=/gpfs3/well/margulies/users/anw410/data/Deafness/bids
dir_work=/gpfs3/well/margulies/users/anw410/data/Deafness/wd
dir_qc=/gpfs3/well/margulies/users/anw410/data/Deafness/QC

singularity run --cleanenv --writable-tmpfs --containall \
    -B ${dir_bids}:/bids \
    -B ${dir_qc}:/out \
    -B ${dir_work}:/wd \
    ${img_mriqc} /bids /out participant -w /wd