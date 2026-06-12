#!/bin/bash 

#SBATCH -J fast_deaf
#SBATCH -D /gpfs3/well/margulies/users/anw410/data/Deafness/scps/wd
#SBATCH -p short
#SBATCH -o /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/fast_deaf.out 
#SBATCH -e /gpfs3/well/margulies/users/anw410/data/Deafness/scps/logs/fast_deaf.err 
#SBATCH -c 1
#SBATCH -a 1-60

echo "------------------------------------------------" 
echo "Slurm Job ID: $SLURM_JOB_ID" 
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "------------------------------------------------" 

ml use -a /apps/eb/2020b/skylake/modules/all
ml load FSL/6.0.5.1-foss-2021a


if [ ${SLURM_ARRAY_TASK_ID} -lt 10 ]; then sjname=sub-0${SLURM_ARRAY_TASK_ID}; else sjname=sub-${SLURM_ARRAY_TASK_ID}; fi

dir_data=/gpfs3/well/margulies/users/anw410/data/Deafness/bids
dir_fast=/gpfs3/well/margulies/users/anw410/data/Deafness/T1_fast

mkdir -p ${dir_fast}/${sjname}
mv ${dir_data}/${sjname}/anat/${sjname}_T1w.nii.gz ${dir_fast}/${sjname}/
fast -b -B -p -o ${sjname}_T1w_fast ${dir_fast}/${sjname}/${sjname}_T1w.nii.gz
cp ${dir_fast}/${sjname}/${sjname}_T1w_fast_restore.nii.gz ${dir_data}/${sjname}/anat/
mv ${dir_data}/${sjname}/anat/${sjname}_T1w.json ${dir_data}/${sjname}/anat/${sjname}_T1w_fast_restore.json
